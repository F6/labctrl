
import struct
import time
import numpy as np
from serial_adc import serial_adc


class DelayUnit2CH:
    """
    2 methods to implement delay unit is possible in STM32F401CDU6, 
     the first is to use 2 16-bit timers, for example timer 3 and 4,
     set them to be reseted in slave mode, set up one pulse mode and
     PWM generation CH2, and trigs them by input at TI1FP1, then arr
     and ccr registers of the timers can be used to set the delay and
     duration of the pulse. Because the timers work in 84MHz and only
     have 16-bit (max 65536 < 84000), max pulse delay is below 65536/
     84000 ms, around 0.78 ms, which is not enough for our laser repe-
     tition rate 1kHz, which may require delay between 0-1 ms. So we
     have to set timer prescaler to 1 (the actual scaler is 1+1=2), so
     that we can get to 1.56 ms max delay. But we can only step the
     delay at 1/42 ms = 23.8 us now, instead of 11.9 us before. This 
     is OK for our boxcar because the charge transfer from PD to inte-
     grator capacitor requires at least several periods, since both
     are quite large capacitors.
    The second way is to use timer 2 as base timer because it has 32-bit
     max, that is 4294967296/84000000 = 51.13 s max delay, sufficient for
     anything. Timer 3 and 4 are configured to be trigged by ITR1, which is
     internally connected to TIM2 TRGO. They are responsible for generating
     boxcar switching signal after timer 2 elapsed. This has the advantage
     of very large delay range, but the TRGO signal requires some time to 
     get to ITR1, so the timer will not be very pricise when used in small
     delays. The setup is also more complicated because you need to calculate
     the total delay and assign them to TIM2 and TIM3, 4 arr, ccr registers,
     respectively.
    Here we use the first type of delay unit setup, because it is more easy
     to set up and fit our needs better. The drawback of first type also 
     includes that you will have to wire up both timer inputs to the same input
     terminal, to make the 2 channels get the same input simultaneously and keep
     them synchronized. 
    """
    def __init__(self) -> None:
        self.com = serial_adc.com
        self.SET_DELAY_CH_1 = b'\x01' # cmd to set delay of the first channel pulse since trigger pulse in
        self.SET_PULSE_CH_1 = b'\x02' # cmd to set duration of the first channel pulse since pulse start
        self.SET_DELAY_CH_2 = b'\x03' # second channel, same as above
        self.SET_PULSE_CH_2 = b'\x04'
        self.CLOCK_FREQUENCY = 84000000
        self.MICROSECOND = 1000000

    
    def set_delay_ch1(self, delay_us, duration_us):
        arr = (delay_us + duration_us) * self.CLOCK_FREQUENCY / self.MICROSECOND
        ccr = duration_us * self.CLOCK_FREQUENCY / self.MICROSECOND
        arr = int(arr)
        ccr = int(ccr)
        assert 0 < arr < 65536
        assert 0 < ccr < 65536
        # CMD LENGTH: 3 (1 for cmd, 2 for 16-bit data)
        self.com.write(self.SET_DELAY_CH_1 + struct.pack('>H', int(arr)))
        self.com.write(self.SET_PULSE_CH_1 + struct.pack('>H', int(ccr)))

    def set_delay_ch2(self, delay_us, duration_us):
        arr = (delay_us + duration_us) * self.CLOCK_FREQUENCY / self.MICROSECOND
        ccr = duration_us * self.CLOCK_FREQUENCY / self.MICROSECOND
        arr = int(arr)
        ccr = int(ccr)
        assert 0 < arr < 65536
        assert 0 < ccr < 65536
        # CMD LENGTH: 3 (1 for cmd, 2 for 16-bit data)
        self.com.write(self.SET_DELAY_CH_2 + struct.pack('>H', int(arr)))
        self.com.write(self.SET_PULSE_CH_2 + struct.pack('>H', int(ccr)))




class BoxcarController:
    def __init__(self) -> None:
        self.adc = serial_adc
        self.du = DelayUnit2CH()
    
    def get_value(self):
        return self.adc.data
    
    def get_statistical_quantities(self):
        sq = dict()
        sq['average'] = np.average(self.adc.data)
        # we use unbiased estimator of standard deviation here, but it should be trivial because we have in general >100 samples for each data point (for 1kHz laser, that is just 0.1s scan time, typical scans use >0.5s scan time to balance between laser drifting and time cost to move linear stages, shutters, etc., to get best total experiment efficiency)
        sq['sample standard deviation'] = np.std(self.adc.data, ddof=np.size(self.adc.data) - 1)

        return sq
    
    def wait_for_flush(self):
        self.adc.flush_data()
        while not self.adc.data_flushed_flag:
            time.sleep(0.01)
    
    def get_interlaced_subtraction_average(self):
        sum = 0
        n = len(self.adc.data)
        assert n % 2 == 0
        for i in range(n):
            if i % 2:
                sum = sum + self.adc.data[i]
            else:
                sum = sum - self.adc.data[i]
        average = sum / n / 2
        return average

boxcar = BoxcarController()
