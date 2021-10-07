# -*- coding: utf-8 -*-

"""sht_emulator.py:
This module provides web API for
development emulation of shtsvr.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real environment, and that they return fabricated
data
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


from flask import Flask
# import serial

comport = 'COM7'


app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] The Shutter Emulator is ONLINE"


@app.route("/off/<no>")
def shtoff(no):
    no = int(no)

    print("Turn off shutter {no}".format(no=no))

    return "[OK] Emulator Turning off shutter {no}".format(no=no)


@app.route("/on/<no>")
def shton(no):
    no = int(no)

    print("Turn on shutter {no}".format(no=no))

    return "[OK] Emulator Turning on shutter {no}".format(no=no)


@app.route("/q/<no>")
def shtq(no):
    no = int(no)

    print(" shutter {no}".format(no=no))

    return "shutter {no} r".format(no=no)
