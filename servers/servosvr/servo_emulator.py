# -*- coding: utf-8 -*-

"""servo_emulator.py:
This module provides web API for
development emulation of servosvr.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real enviroment, and that they return fabricated
data
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

from flask import Flask
# import serial

comport = 'COM6'

zero_delay = -129.808


def getser(ser):
    return ser
    # return serial.Serial(ser, baudrate=115200, timeout=1)


def cmd(ser, s):
    # ser.write(s.encode('ascii'))
    # print(ser.readline())
    print(s)


app = Flask(__name__)

poslist = []


@app.route("/")
def online():
    return "[OK] The Servo Server is ONLINE"


@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)

    # if pos in poslist:
    #     return "<p>Warning: You have moved to {pos} previously, which should not happen in a single run, please check the sync! No action has been taken.</p>".format(pos=pos)

    poslist.append(pos)

    print("Moving to {pos}".format(pos=pos))

    return "[OK] Moving to {pos}".format(pos=pos)


@app.route("/clearposlist")
def clearposlist():
    poslist.clear()
    return "[OK] Position list has been cleared, be careful with the sync!"


@app.route("/home")
def home():

    return "[OK] Automatically returning to home..."
