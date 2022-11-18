import time
import serial
from contextlib import contextmanager


class CDHD2:
    def __init__(self, com) -> None:
        self.comport = com
        self.delta_pos = 0
        self.curr_pos = 0
        self.driving_speed = 50.0  # mm/s
        self.ser = serial.Serial(self.comport, baudrate=115200, timeout=1)

    # @contextmanager
    # def getser(self, *args, **kwds):
    #     ser = serial.Serial(self.comport, timeout=1)
    #     try:
    #         yield ser
    #     finally:
    #         ser.close()

    def cmd(self, s: str):
        # with self.getser() as ser:
        #     ser.write(s.encode('ascii'))
        #     res = ser.readline()
        self.ser.write(s.encode('ascii'))
        response = self.ser.readline().decode()
        print(response)
        return response

    def enable_stage(self):
        self.cmd('ENABLE\r')
    
    def hardware_position(self):
        self.cmd("HWPOS\r")

    def set_driving_speed(self, new_speed:float):
        self.driving_speed = float(new_speed)
        print("Updated driving speed to {}".format(self.driving_speed))

    def moveabs(self, pos: float, block=True):
        """move to abs position of x axis, but use milimeter as unit"""
        res = self.cmd('MOVEABS {pos} {speed}\r'.format(
            pos=pos, speed=self.driving_speed))
        self.delta_pos = abs(pos - self.curr_pos)
        if block:
            time.sleep(self.delta_pos/self.driving_speed)
        self.curr_pos = pos
        return res

    def autohome(self, block=True):
        self.delta_pos = abs(0 - self.curr_pos)
        if block:
            time.sleep(self.delta_pos/20)
        self.curr_pos = 0
        res = self.cmd('HOMECMD\r')
        return res


comport = 'COM12'

cdhd2 = CDHD2(comport)
