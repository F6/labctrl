from threading import Thread

from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
import TLPM
import time
import serial
import sys
import numpy as np


class CyclicBuffer:
    def __init__(self) -> None: 
        self.length = 16384 # 64kB
        self.data = np.zeros(self.length, dtype=np.float64)
        self.current_data_index = 0

    def append(self, value):
        self.current_data_index += 1
        if self.current_data_index >= self.length:
            self.current_data_index = 0
            np.savetxt(str(time.time()) + '.txt', self.data)
        if self.current_data_index % 1000 == 0:
            print("!")
        self.data[self.current_data_index] = value

    def get_current(self):
        # print(self.data)
        return self.data[self.current_data_index]
    
    def get_slice(self, istart, istop):
        # overflow!
        assert abs(istop - istart) <= self.length
        # recursive: put istart and istop between 0 - length
        if istop > self.length:
            return self.get_slice(istart, istop - self.length)
        if istart > self.length:
            return self.get_slice(istart - self.length, istop)
        if istart < 0:
            return self.get_slice(istart + self.length, istop)
        if istop < 0:
            return self.get_slice(istart, istop + self.length)
        # if stop is larger, it's just normal slice. if stop is smaller, we need to cat tail and head
        if istop > istart:
            return self.data[istart:istop]
        elif istop == istart:
            return np.array([])
        else:
            buf1 = self.data[istart:self.length]
            buf2 = self.data[0:istop]
            return np.concatenate((buf1, buf2))


class PM400:
    def __init__(self, wavelength, range_to_measure) -> None:
        self.wavelength = wavelength
        self.range_to_measure = range_to_measure
        self.__init_TLPM()
        # create a cyclic buffer to store measured data
        self.buf = CyclicBuffer()
        # signal flag to exit data reading thread
        self.halt = False
        # open device and start data reading task
        self.__open_TLPM(self.wavelength, self.range_to_measure)
        self.data_thread = Thread(target=self.reading_task)
        self.data_thread.start()

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
        time.sleep(0.5)
        self.tlPM.setWavelength(c_double(wavelength))
        time.sleep(0.5)
        self.tlPM.setPowerAutoRange(TLPM.TLPM_AUTORANGE_CURRENT_OFF)
        time.sleep(0.5)
        self.tlPM.setPowerRange(c_double(range_to_measure))
        time.sleep(3)
        

    def reading_task(self):
        while not self.halt:
            try:
                power = c_double()
                self.tlPM.measPower(byref(power))
                # print(power.value)
                self.buf.append(power.value)
                time.sleep(0.01)
            except NameError as e:
                # probably lost connection, let's try reconnect
                print(e, e.args)
                # self.__open_TLPM(self.wavelength, self.range_to_measure)

    def close_TLPM(self):
        self.halt = True
        self.tlPM.close()

pm = PM400(800, 0.03)

try:
    while True:
        pass
except KeyboardInterrupt:
    pm.close_TLPM()