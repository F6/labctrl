import time
import serial
from contextlib import contextmanager


class CDHD2:
    def __init__(self, com) -> None:
        self.comport = com
        self.delta_pos = 0
        self.curr_pos = 0

    @contextmanager
    def getser(self, *args, **kwds):
        ser = serial.Serial(self.comport, timeout=1)
        try:
            yield ser
        finally:
            ser.close()

    def cmd(self, s):
        with self.getser() as ser:
            ser.write(s.encode('ascii'))
            res = self.ser.readline()
        return res

    def moveabs(self, pos: float, block=True):
        """move to abs position of x axis, but use milimeter as unit"""
        res = self.cmd('MOVEABS {pos} 20\r'.format(pos=pos)) # fixed speed at 20mm/s
        self.delta_pos = abs(pos - self.curr_pos)
        if block:
            time.sleep(self.delta_pos/20)
        self.curr_pos = pos
        return res

    def autohome(self, block=True):
        self.delta_pos = abs(0 - self.curr_pos)
        if block:
            time.sleep(self.delta_pos/20)
        self.curr_pos = 0
        res = self.cmd('HOMECMD\r')
        return res



comport = 'COM6'

cdhd2 = CDHD2(comport)