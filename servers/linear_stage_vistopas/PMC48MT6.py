# -*- coding: utf-8 -*-

"""PMC48MT6.py:
This module implements class PMC48MT6 to access
Ningbo Adhon PMC 48MT6 stepper motor controllers

Only the X axis is controlled and only 1 card is installed.
For more complicated controls, use functions in Adhon_PMC_48MT6.py
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211020"

import time
import ctypes
import Adhon_PMC_48MT6 as lib



class PMC48MT6:
    def __init__(self) -> None:
        self.comport = 4
        print("Opening serial port ", self.comport)
        r = lib.PMC_OpenSericalPort(self.comport)
        print("Initializing PMC driver")
        r = lib.PMC_GlobalInit()
        self.addr = ctypes.c_ubyte()
        r = lib.PMC_GetControllerAddr(ctypes.byref(self.addr))
        print("Controller Address: ", self.addr.value)
        self.controller_version = ctypes.c_ulong()
        r = lib.PMC_GetControllerVersion(self.addr, ctypes.byref(self.controller_version))
        print("Controller Version: ", self.controller_version.value)
        # r = lib.PMC_SetMotorMaxSpeed(self.addr, lib.AXIS_X, 1000)

    def __del__(self) -> None:
        print("Releasing PMC driver")
        r = lib.PMC_GlobalRelease()
        print("Closing serial port")
        r = lib.PMC_CloseSericalPort()

    def setp(self, pos: float, block=False) -> None:
        """move to abs position of x axis"""
        lib.PMC_MotorGoPos(self.addr, lib.AXIS_X, pos)
        # block until movement done if block
        if block:
            cp = ctypes.c_float()
            r = lib.PMC_GetMotorPosition(
                self.addr, lib.AXIS_X, ctypes.byref(cp))
            while abs(cp.value - pos) > 0.1:
                time.sleep(0.1)
                r = lib.PMC_GetMotorPosition(
                    self.addr, lib.AXIS_X, ctypes.byref(cp))

    def autohome(self) -> None:
        """move to 0"""
        self.setp(0.0, block=True)

    def moveabs(self, pos: float) -> None:
        """move to abs position of x axis, but use milimeter as unit"""
        self.setp(pos, block=True)
