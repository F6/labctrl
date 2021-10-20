# -*- coding: utf-8 -*-

"""USB1020.py:
This module implements class USB1020 to access
Beijing ART Tech USB1020 stepper motor controllers

The board tested is USB1020 V7.01

Only the X axis is controlled and only 1 card is installed.
For more complicated controls, use functions in USB1020_64.py
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"

import time
import USB1020_64 as lib


class USB1020:
    def __init__(self) -> None:
        self.hdevice = None
        self.home = 0
        self.device_pos = 0
        with open('curr_pos.txt', 'r') as f:
            self.device_pos = int(f.read())
        self.steps_per_mm = 37500
        self.soft_max = 3000000
        self.__init_param()

    def __init_param(self):
        """set up basic working modes and params"""
        self.dl = lib.USB1020_PARA_DataList()
        self.dl.Multiple = 30
        self.dl.StartSpeed = 100
        self.dl.DriveSpeed = 5000
        self.dl.Acceleration = 3000
        self.dl.Deceleration = 3000
        self.dl.AccIncRate = 1000
        self.dl.DecIncRate = 1000
        self.lc = lib.USB1020_PARA_LCData()
        self.lc.AxisNum = lib.USB1020_XAXIS
        self.lc.LV_DV = lib.USB1020_DV
        self.lc.DecMode = 0
        self.lc.PulseMode = lib.USB1020_CWCCW
        self.lc.PLSLogLever = 1
        self.lc.DIRLogLever = 1
        self.lc.Line_Curve = lib.USB1020_LINE
        self.lc.Direction = lib.USB1020_MDIRECTION
        self.lc.nPulseNum = 10000


    def createDevice(self):
        if self.hdevice == None:
            self.hdevice = lib.USB1020_CreateDevice(0)
            print(
                "Automatically selected the first USB1020 card installed, hdevice is ", self.hdevice)

    def setp(self, pos: int, block=False) -> None:
        """move to abs position of x axis"""
        if pos > self.soft_max:
            pos = self.soft_max
            print("[Error] Reached software max step limit {}!".format(self.soft_max))
            print("Is the home currect? Consider autohome to reset home position.")
        delta = pos - self.device_pos
        self.device_pos = pos
        if delta > 0:
            self.lc.nPulseNum = delta
            self.lc.Direction = lib.USB1020_PDIRECTION
        elif delta < 0:
            self.lc.nPulseNum = -delta
            self.lc.Direction = lib.USB1020_MDIRECTION
        else:
            return
        r = lib.USB1020_InitLVDV(self.hdevice, self.dl, self.lc)
        r = lib.USB1020_StartLVDV(self.hdevice, self.lc.AxisNum)
        with open('curr_pos.txt', 'w') as f:
            f.write(str(self.device_pos))
        # block until movement done if block
        if block:
            rr0para = lib.USB1020_PARA_RR0()
            lib.USB1020_GetRR0Status(self.hdevice, rr0para)
            while rr0para.XDRV == 1:
                time.sleep(0.1)
                lib.USB1020_GetRR0Status(self.hdevice, rr0para)

    def autohome(self) -> None:
        """emulate autohome with XIN0"""
        rr3para = lib.USB1020_PARA_RR3()
        lib.USB1020_GetRR3Status(self.hdevice, rr3para)
        while rr3para.XIN0 == 0:
            # XIN0 is the home switch, fast backward movement
            self.setp(self.device_pos - 50000, block=True)
            lib.USB1020_GetRR3Status(self.hdevice, rr3para)
        while rr3para.XIN0 == 1:
            # slow forward until enter working range
            self.setp(self.device_pos + 1000, block=True)
            lib.USB1020_GetRR3Status(self.hdevice, rr3para)
        self.device_pos = 0


    def moveabs(self, pos: float) -> None:
        """move to abs position of x axis, but use milimeter as unit"""
        self.setp(int(pos*self.steps_per_mm), block=True)

    def releaseDevice(self):
        if self.hdevice is not None:
            lib.USB1020_ReleaseDevice(self.hdevice)
            self.hdevice = None
