# -*- coding: utf-8 -*-

"""shtsvr.py:
This module provides web API for
a remote shutter controller

the shutter controller is the self-made one (gray aluminum box)
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


from flask import Flask
import serial

comport = 'COM7'


def getser(ser):
    return serial.Serial(ser, baudrate=115200, timeout=1)


def cmd(ser, s):
    ser.write(s.encode('ascii'))
    return ser.readline()


app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] The Shutter Server is ONLINE"


@app.route("/off/<no>")
def shtoff(no):
    no = int(no)

    print("[OK] Turn off shutter {no}".format(no=no))
    ser = getser(comport)
    r = cmd(ser, 'SHT{no}:OFF\n'.format(no=no))
    ser.close()
    print(r)
    return "[OK] Turning off shutter {no}".format(no=no)


@app.route("/on/<no>")
def shton(no):
    no = int(no)

    print("[OK] Turn on shutter {no}".format(no=no))
    ser = getser(comport)
    r = cmd(ser, 'SHT{no}:ON\n'.format(no=no))
    ser.close()
    print(r)
    return "[OK] Turning on shutter {no}".format(no=no)


@app.route("/q/<no>")
def shtq(no):
    no = int(no)

    print(" shutter {no}".format(no=no))
    ser = getser(comport)
    r = cmd(ser, 'SHT{no}:?\n'.format(no=no))
    ser.close()
    r = str(r)
    print(r)
    return "shutter {no} {r}".format(no=no, r=r)
