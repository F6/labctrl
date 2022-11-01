import serial
import time
import struct
import numpy as np
from threading import Thread

class SerialADC:
    def __init__(self) -> None:
        self.packet_len = 4096
        self.data_len = self.packet_len // 2
        self.com = serial.Serial('COM12', baudrate=114500, timeout=1)
        self.data = None
        self.data_flushed_flag = False # used when a flush is in place
        self.data_updated_since_flush_flag = False
        self.time = time.time_ns()
        self.th = Thread(target=self.data_reading_task)
        self.th.start()

    def parse_data(self, buffer):
        return np.asarray(struct.unpack('<{}H'.format(self.data_len), buffer))

    def flush_data(self):
        self.data_flushed_flag = True # when active, the user knows that this data has not been updated yet, and need to wait for the flag deactived to get updated data

    def data_buffer_handler(self, buffer):
        y = self.parse_data(buffer)
        self.data = y
        self.time = time.time_ns()
        if self.data_updated_since_flush_flag:
            # the data is updated now, ready to be read by user
            self.data_updated_since_flush_flag = False
            self.data_flushed_flag = False
        if self.data_flushed_flag:
            # this round of data is flushed! When next round data is in, the data is updated
            self.data_updated_since_flush_flag = True

    
    def data_reading_task(self):
        while True:
            time.sleep(0.01)  # this is here to prevent pyserial eating up all cpu
            if self.com.in_waiting:
                databuffer = self.com.read_all()
                if len(databuffer) == self.packet_len:
                    self.data_buffer_handler(databuffer)
                else:
                    print("corrupted data!")


serial_adc = SerialADC()

