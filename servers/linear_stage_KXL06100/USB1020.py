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

from contextlib import contextmanager
import USB1020_64 as lib


class USB1020:
    def __init__(self) -> None:
        self.hdevice = None
        self.home = 0
        self.device_pos = 0
        self.steps_per_mm = 80000
        self.__init_param()

    def __init_param(self):
        """set up basic working modes and params"""
        self.dl = lib.USB1020_PARA_DataList()
        self.dl.Multiple = 2
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

    def setp(self, pos: int) -> None:
        """move to abs position of x axis"""
        self.device_pos = lib.USB1020_ReadEP(self.hdevice, lib.USB1020_XAXIS)
        delta = pos - self.device_pos
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

    def sethome(self, pos: int) -> None:
        self.home = pos

    def moveabs(self, pos: float) -> None:
        """move to abs position of x axis, but use milimeter as unit"""
        self.setp(int(pos*self.steps_per_mm))

    def releaseDevice(self):
        if self.hdevice is not None:
            lib.USB1020_ReleaseDevice(self.hdevice)
            self.hdevice = None
