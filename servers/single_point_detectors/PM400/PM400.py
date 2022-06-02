from threading import Thread

from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
import TLPM
import time
import serial
import sys
import numpy as np


class PM400:
    def __init__(self, wavelength, range_to_measure) -> None:
        self.wavelength = wavelength
        self.range_to_measure = range_to_measure
        self.__init_TLPM()
        # create a cyclic buffer to store measured data
        self.current_data_index = 0
        self.data_index_max = 1024
        self.data = np.zeros(self.data_index_max, dtype=np.float64)
        # signal flag to exit data reading thread
        self.halt = False
        # open device and start data reading task
        self.__open_TLPM(self.wavelength, self.range_to_measure)

    def __init_TLPM(self):
        self.tlPM = TLPM.TLPM()
        deviceCount = c_uint32()
        self.tlPM.findRsrc(byref(deviceCount))

        print("devices found: " + str(deviceCount.value))

        self.resourceName = create_string_buffer(1024)

        for i in range(0, deviceCount.value):
            self.tlPM.getRsrcName(c_int(i), self.resourceName)
            print(c_char_p(self.resourceName.raw).value)
            break

        self.tlPM.close()

    def __open_TLPM(self, wavelength, range_to_measure):
        self.tlPM = TLPM.TLPM()
        #resourceName = create_string_buffer(b"COM1::115200")
        #print(c_char_p(resourceName.raw).value)
        self.tlPM.open(self.resourceName, c_bool(True), c_bool(True))

        message = create_string_buffer(1024)
        self.tlPM.getCalibrationMsg(message)
        print(c_char_p(message.raw).value)

        self.tlPM.setWavelength(c_double(wavelength))
        self.tlPM.setCurrentRange(c_double(range_to_measure))
        self.tlPM.setCurrentAutoRange(TLPM.TLPM_AUTORANGE_CURRENT_OFF)

        time.sleep(3)
        
        data_thread = Thread(target=self.reading_task)
        data_thread.start()

    def reading_task(self):
        while not self.halt:
            try:
                if self.current_data_index < self.data_index_max - 1:
                    self.current_data_index += 1
                else:
                    self.current_data_index = 0
                power = c_double()
                self.tlPM.measPower(byref(power))
                # print(power.value)
                self.data[self.current_data_index] = power.value
                time.sleep(0.01)
            except NameError as e:
                # probably lost connection, let's try reconnect
                print(e, e.args)
                self.__open_TLPM(self.wavelength, self.range_to_measure)

    def close_TLPM(self):
        self.halt = True
        self.tlPM.close()