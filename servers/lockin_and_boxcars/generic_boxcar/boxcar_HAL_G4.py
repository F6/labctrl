# -*- coding: utf-8 -*-

"""boxcar_HAL_G4.py:
Hardware Abstraction Layer for boxcar controller made with STM32G431CBT6 series controller.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220809"


import serial
import struct
import time
from threading import Thread

import numpy as np
np.set_printoptions(precision=5, suppress=True)

""" 
Sets the delay of events after the trigger signal is in
    background sampling: this can be done before integrate, or after reset
    signal sampling: this must be done after hold, but before reset
    integrate: this starts just before the pulsed light comes in
    hold: this starts just after the pulsed signal decays
    reset: this starts when signal sampling is over

    T:               0ms -----|----------|----------------------|--------------|---------|------------------|---------- 1ms
                              Trig In    Background Sampling    Integrate      Hold      Signal Sampling    Reset
    Laser Trigger       :_____----_____________________________________________________________________________________ f=1kHz
    Signal Pulse        :___________________________________________------_____________________________________________
    Boxcar Output       :_______________________________________-___-----------=-----------------------------__________
    Charge Injection    :_______________________________________-______________-_______________________________________ (1mV for 100pF)
    TIM4 CH4 (ADC TRIG) :_____|__________------------------------------------------------______________________________ (ADC2 trigs on rising and falling edge)
                              TIM4 EN    CCR4                                            ARR
    Sync In (Chopper)   :_____?---_____________________________________________________________________________________ f=1kHz/N
    TIM3 CH1 (SYNC IN)  :_____?________________________________________________________________________________________
    TIM2 CH2 (S2)       :_____|__________________________________--------------------------------------------__________
    TIM2 CH3 (S1)       :_____|_________________________________________________-----------------------------__________
                              TIM2 RESET                         CCR2           CCR3                         ARR
    TIM5 CH1 (PWACLK)   :_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- f=2MHz
    TIM9 CH2 (TEST1K)   :_____----_____________________________________________________________________________________ f=1kHz

    Note:
        For STM32G431CBT6, only TIM2 is 32-bit, which means the integrate and hold time can be varied in a very
        large range, but the sampling delay etc cannot, however, since the sampling delays does not need to be
        very precise for a boxcar type integrator, they are implemented with NVICs and can be switched to software
        delay (HAL_Delay) easily. This enables the 16-bit TIMs to work with longer (>1ms) delays. Prescaler can
        also be used with TIM3 and TIM4 for longer delays, too.

        In working mode, 256x oversampling is enabled to achieve higher ADC ENOB, this degrades the ADC sampling rate to
        below 156 kS/s. Thus, it is necessary to disable oversampling in PWA mode. Data remap is required since when over-
        sampling is enabled, data range is 0-65535 (16bit), while when oversampling is disabled, data range is 0-4096 (12bit)

        An op amp PGA and bias net is placed before the ADC. The bias is generated from on-chip DAC.
        Higher dynamic range is available by adjusting the DAC output and PGA gain.
        The PGA works in inverting mode.

        Sync In is a special port used when modulations on the pulse train is used. For example, if the user uses a chopper
        to chop the laser pulses from 1kHz to 500Hz to measure the pumped and not-pumped signal, and the chopper generates a 500Hz
        Sync trigger, it is in general favorable to know which data points are in-phase with the 500Hz sync trigger, and which
        are out-of-phase. The same applies to higher modulation orders, for example 3 choppers are used in series to generate
        a 125Hz sync trigger, splitting the original 1kHz pulse train into 8 different signals. The Sync In port works by counting
        how many 1kHz trigger pulses has been elapsed since the Sync In port rising edge, cleans and restarts the counter on the 
        next rising edge, and attach the count to the data packet right before the data packet is sent.
"""
CMD_SET_DELAY_BACKGROUND_SAMPLING = 0x01
CMD_SET_DELAY_INTEGRATE = 0x02
CMD_SET_DELAY_HOLD = 0x03
CMD_SET_DELAY_SIGNAL_SAMPLING = 0x04
CMD_SET_DELAY_RESET = 0x05

# units in us
DEFAULT_DELAY_BACKGROUND_SAMPLING = 10
DEFAULT_DELAY_INTEGRATE = 20
DEFAULT_DELAY_HOLD = 900
DEFAULT_DELAY_SIGNAL_SAMPLING = 920
DEFAULT_DELAY_RESET = 950


"""
Sets the working mode of boxcar
PWA (Periodic Waveform Analyzer): basically oscilloscope, useful for finding suitable delays
Boxcar: main working mode, switches to high resolution ADC for sample taking
"""
CMD_SET_WORKING_MODE = 0x08
MODE_PWA = 0x01
MODE_BOXCAR = 0x02
DEFAULT_WORKING_MODE = MODE_BOXCAR


"""
Meta params

File Format:
    [0:4] : uint32_t : packet total length
    [5:8] : uint32_t : metadata
     
"""
MCU_BASE_FREQUENCY = 84
BOXCAR_DATA_BUFFER_SIZE = 512
BOXCAR_DATA_BYTES_LENGTH = 2
BOXCAR_DATA_BUFFER_SIZE_HALF = BOXCAR_DATA_BUFFER_SIZE // 2
PWA_DATA_BUFFER_SIZE = 1024
PWA_DATA_BYTES_LENGTH = 2  # 16 bit to store 12 bit data


class BoxcarController:
    def __init__(self) -> None:
        # self.baudrate = 921600
        self.baudrate = 115200
        self.ser = serial.Serial("COM6", baudrate=115200, timeout=1)
        self.set_delay_background_sampling(DEFAULT_DELAY_BACKGROUND_SAMPLING)
        self.set_delay_integrate(DEFAULT_DELAY_INTEGRATE)
        self.set_delay_hold(DEFAULT_DELAY_HOLD)
        self.set_delay_signal_sampling(DEFAULT_DELAY_SIGNAL_SAMPLING)
        self.set_delay_reset(DEFAULT_DELAY_RESET)
        self.set_working_mode(DEFAULT_WORKING_MODE)
        self.halt_flag = False
        self.boxcar_data = np.zeros(BOXCAR_DATA_BUFFER_SIZE, dtype=np.float64)
        self.PWA_data = np.zeros(PWA_DATA_BUFFER_SIZE, dtype=np.float64)
        self.working_mode = DEFAULT_WORKING_MODE
        self.t = Thread(target=self.data_reading_task)
        self.t.start()
        self.fpscounter = 0

    def set_delay_background_sampling(self, delay):
        # 16-bit value
        delay = delay * MCU_BASE_FREQUENCY
        delay = int(delay)
        cmd = struct.pack(
            '>1B', CMD_SET_DELAY_BACKGROUND_SAMPLING) + struct.pack('>1H', delay)
        self.ser.write(cmd)
        return delay

    def set_delay_integrate(self, delay):
        # 32-bit value
        delay = delay * MCU_BASE_FREQUENCY
        delay = int(delay)
        cmd = struct.pack('>1B', CMD_SET_DELAY_INTEGRATE) + \
            struct.pack('>1I', delay)
        self.ser.write(cmd)
        return delay

    def set_delay_hold(self, delay):
        # 32-bit value
        delay = delay * MCU_BASE_FREQUENCY
        delay = int(delay)
        cmd = struct.pack('>1B', CMD_SET_DELAY_HOLD) + \
            struct.pack('>1I', delay)
        self.ser.write(cmd)
        return delay

    def set_delay_signal_sampling(self, delay):
        # 16-bit value
        delay = delay * MCU_BASE_FREQUENCY
        delay = int(delay)
        cmd = struct.pack('>1B', CMD_SET_DELAY_SIGNAL_SAMPLING) + \
            struct.pack('>1H', delay)
        self.ser.write(cmd)
        return delay

    def set_delay_reset(self, delay):
        # 32-bit value
        delay = delay * MCU_BASE_FREQUENCY
        delay = int(delay)
        cmd = struct.pack('>1B', CMD_SET_DELAY_RESET) + \
            struct.pack('>1I', delay)
        self.ser.write(cmd)
        return delay

    def set_working_mode(self, mode):
        assert mode in (MODE_BOXCAR, MODE_PWA)
        cmd = struct.pack('>1B', CMD_SET_WORKING_MODE) + \
            struct.pack('>1B', mode)
        self.ser.write(cmd)
        self.working_mode = mode
        return mode

    def boxcar_buffer_handler(self, buffer):
        # data = struct.unpack('<{n}i'.format(n=USB_DATA_BUFFER_SIZE), buffer)
        # data = np.array(data)
        data = np.frombuffer(buffer, dtype=np.int32)
        for i in range(np.size(data)):
            self.boxcar_data[i] = data[i]/65536*2.048
        self.fpscounter += 1
        # print(self.boxcar_data)
        return data

    def PWA_buffer_handler(self, buffer):
        data = np.frombuffer(buffer, dtype=np.uint16)
        for i in range(np.size(data)):
            self.PWA_data[i] = data[i]/4096*2.048
        self.fpscounter += 1
        # print(self.PWA_data)
        return data

    def data_reading_task(self):
        while not self.halt_flag:
            if self.ser.in_waiting:
                buffer = self.ser.read_all()
                if MODE_BOXCAR == self.working_mode:
                    if 0 == len(buffer) % (BOXCAR_DATA_BUFFER_SIZE*BOXCAR_DATA_BYTES_LENGTH):
                        # print("buffer in", buffer)
                        for i in range(0, len(buffer), BOXCAR_DATA_BUFFER_SIZE*BOXCAR_DATA_BYTES_LENGTH):
                            self.boxcar_buffer_handler(
                                buffer[i:i+BOXCAR_DATA_BUFFER_SIZE*BOXCAR_DATA_BYTES_LENGTH])
                    else:
                        print("Non-data message or corrupted data: ",
                            buffer.decode(errors='replace'))
                elif MODE_PWA == self.working_mode:
                    if 0 == len(buffer) % (PWA_DATA_BUFFER_SIZE*PWA_DATA_BYTES_LENGTH):
                        # print("buffer in", buffer)
                        for i in range(0, len(buffer), PWA_DATA_BUFFER_SIZE*PWA_DATA_BYTES_LENGTH):
                            self.PWA_buffer_handler(
                                buffer[i:i+PWA_DATA_BUFFER_SIZE*PWA_DATA_BYTES_LENGTH])
                    else:
                        print("Non-data message or corrupted data: ",
                            buffer.decode(errors='replace'))
                else:
                    pass
            time.sleep(0.01)

    def halt(self):
        self.ser.close()
        self.halt_flag = True


t0 = time.time()
boxcar = BoxcarController()

# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     t1 = time.time()
#     print("FPS:", boxcar.fpscounter/(t1-t0))
#     boxcar.halt()
