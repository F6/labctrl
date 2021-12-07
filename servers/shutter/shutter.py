

import serial
from contextlib import contextmanager


class ShutterController:
    def __init__(self, com) -> None:
        self.comport = com
        self.shutter_status = dict()
        for i in range(16): # at most 16 shutters for one controller
            self.shutter_status[str(i)] = False

    @contextmanager
    def getser(self, *args, **kwds):
        ser = serial.Serial(self.comport, timeout=1, baudrate=115200)
        try:
            yield ser
        finally:
            ser.close()

    def cmd(self, s):
        with self.getser() as ser:
            ser.write(s.encode('ascii'))
            res = ser.readline()
        return res

    def shutter_off(self, shutter_name='1'):
        r = self.cmd('SHT{i}:OFF\n'.format(i=shutter_name))
        self.shutter_status[shutter_name] = False
        return r
    
    def shutter_on(self, shutter_name='1'):
        r = self.cmd('SHT{i}:ON\n'.format(i=shutter_name))
        self.shutter_status[shutter_name] = True
        return r

    def switch_shutter(self, shutter_name='1'):
        if self.shutter_status[shutter_name]:
            r = self.shutter_off(shutter_name)
        else:
            r = self.shutter_on(shutter_name)
        return r


sht = ShutterController('COM5')
