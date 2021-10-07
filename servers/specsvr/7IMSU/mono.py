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
__version__ = "20211003"


import serial
import struct
from contextlib import contextmanager


class MonoController():
    def __init__(self, com:str) -> None:
        self.comport = com

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

    def moveto(self, stp:int):
        cmd = 'W'.encode()
        fmt = '>I'
        cmd = cmd + struct.pack(fmt, stp)
        with self.getser() as ser:
            ser.write(cmd)
            bytes_buffer = ser.read(5)
        res = bytes_buffer[:-1]
        return struct.unpack(fmt, res)[0]

    def stopmoving(self):
        with self.getser() as ser:
            cmd = 'k'.encode()
            ser.write(cmd)

    def getpos(self):
        cmd = 'w'.encode()
        with self.getser() as ser:
            ser.write(cmd)
            bytes_buffer = ser.read(5)
        fmt = '>I'
        res = bytes_buffer[1:]
        return struct.unpack(fmt, res)[0]

