# -*- coding: utf-8 -*-

"""mono.py:
This module implements the class MonoController to communicate
with the 7IMSU monochromer in our lab.

the monochromer is the very heavy, half-gray and half-black one 
now installed at A304. Note that the stepper motor driver in the 
monochromer needs 24 volt power supply.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


import serial
import struct
from contextlib import contextmanager
import json
import numpy as np
import matplotlib.pyplot as plt
import time

class MonoController():
    def __init__(self, com:str) -> None:
        self.comport = com
        with open('calibration.json', 'r') as f:
            cal = json.load(f)
        print("Loaded calibration info from calibration.json")
        raw = cal['raw']
        raw = np.array(raw)
        wavelength = cal['wavelength']
        wavelength = np.array(wavelength)
        # reverse fit to get raw from given wavelength
        print("Using 3rd order polynomial fitting for calibration")
        fit = np.polyfit(wavelength, raw, 3)
        print("    calibration: {}".format(fit))
        self.calibration = np.poly1d(fit)
        print("    calibration curve figure saved in calibration.png, check the figure to ensure goodness of fitting")
        rawmin = np.min(raw)
        rawmax = np.max(raw)
        pltx = np.linspace(rawmin, rawmax, 1000)
        plty = self.calibration(pltx)
        plt.plot(pltx, plty, '-', raw, wavelength, 'o')
        plt.savefig('calibration.png', dpi=600)

    @contextmanager
    def getser(self, *args, **kwds):
        ser = serial.Serial(self.comport, timeout=1)
        try:
            yield ser
        finally:
            ser.close()

    def get_type(self):
        cmd = 't'.encode()
        with self.getser() as ser:
            ser.write(cmd)
            bytes_buffer = ser.read(5)
        fmt = 'B'
        res = bytes_buffer[1:]
        return struct.unpack(fmt, res)[0]

    def stopmoving(self):
        with self.getser() as ser:
            cmd = 'k'.encode()
            ser.write(cmd)

    def getabs(self):
        cmd = 'w'.encode()
        with self.getser() as ser:
            ser.write(cmd)
            bytes_buffer = ser.read(5)
        fmt = '>I'
        res = bytes_buffer[1:]
        return struct.unpack(fmt, res)[0]
    
    def setabs(self, stp:int):
        cmd = 'W'.encode()
        fmt = '>I'
        cmd = cmd + struct.pack(fmt, stp)
        with self.getser() as ser:
            ser.write(cmd)
            bytes_buffer = ser.read(5)
        res = bytes_buffer[:-1]
        return struct.unpack(fmt, res)[0]

    def getpos(self):
        raw = self.getabs()
        return (self.calibration - raw).roots
    
    def setpos(self, wavelength:float, block=True):
        raw = self.calibration(wavelength)
        raw = int(raw)
        self.setabs(raw)
        if block:
            while self.getabs() - raw:
                time.sleep(0.1)

mono = MonoController('COM3')