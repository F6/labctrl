# -*- coding: utf-8 -*-

"""servosvr.py:
This module provides web API for
a remote linear servo stage

the servo is the flat one now installed at A304, the driver
for the servo is servotronix CDHD2. See their manual for other
commands.

for manual tweaking and param adjustments, use the official
ServoStudio software. Disconnect COM port from servostudio 
before starting this app
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

from flask import Flask
import serial

comport = 'COM6'

zero_delay = -129.808


def getser(ser):
    return serial.Serial(ser, baudrate=115200, timeout=1)


def cmd(ser, s):
    ser.write(s.encode('ascii'))
    print(ser.readline())


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
    # poslist.append(pos)

    print("[OK] Moving to {pos}".format(pos=pos))
    ser = getser(comport)
    cmd(ser, 'MOVEABS {pos} 20\r'.format(pos=pos))
    ser.close()
    return "[OK] Moving to {pos}".format(pos=pos)


@app.route("/clearposlist")
def clearposlist():
    poslist.clear()
    return "[OK] Position list has been cleared, be careful with the sync!"


@app.route("/home")
def home():
    ser = getser(comport)
    cmd(ser, 'HOMECMD\r')
    ser.close()
    return "[OK] Automatically returning to home..."
