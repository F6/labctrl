import serial
import struct
import time

ser = serial.Serial("COM10", baudrate=115200, timeout=1)

MCU_BASE_FREQ_HZ = 120000000
TIM1_ARR = 2400

USB_CDC_CMD_SET_TIM1_CCR1 = 0x01
USB_CDC_CMD_SET_TIM1_ARR  = 0x02


def write_command(command, payload):
    if USB_CDC_CMD_SET_TIM1_CCR1 == command:
        to_send = struct.pack('1B', command) + struct.pack('>1H', payload)
    ser.write(to_send)

def set_duty_cycle(duty):
    """
    duty: float, 0.0 - 1.0
    """
    assert 0.0 <= duty <= 1.0
    ccr = int(duty * TIM1_ARR)
    write_command(USB_CDC_CMD_SET_TIM1_CCR1, ccr)

while True:
    for i in range(10, 100, 1):
        time.sleep(0.01)
        set_duty_cycle(i/1000)
    for i in range(100, 10, -1):
        time.sleep(0.01)
        set_duty_cycle(i/1000)