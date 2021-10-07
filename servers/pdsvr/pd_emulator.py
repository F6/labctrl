# -*- coding: utf-8 -*-

"""pd_emulator.py:
This module provides web API for
development emulation of pdsvr.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real enviroment, and that they return fabricated
data
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import re
import os
import base64
from threading import Thread

import numpy as np

from flask import Flask

# import pyvisa as visa
# rm = visa.ResourceManager()
# # reslist = rm.list_resources()
# inst = rm.open_resource('USB0::0x1AB1::0x0515::MS5A222002010::INSTR')

# inst.write(":MEASure:SOURce CHANnel2")
# inst.write(":MEASure:SOURce?")
# print(inst.read())

# inst.write(":MEASure:STATistic:ITEM MARea,CHANnel2")

import time

data = np.random.rand(10)
data_ready_flag = False

app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] PD Server is ONLINE"


def pdtask(exposure_time):
    global data, data_ready_flag

    exposure_time = float(exposure_time)

    time.sleep(exposure_time)
    data = np.random.rand(int(exposure_time * 10)) * 10
    data = np.array(data, dtype=np.float32)

    data_ready_flag = True


@app.route("/takesignal/<exposure_time>")
def takesignal(exposure_time):
    thread = Thread(target=pdtask, args=(exposure_time, ))
    thread.start()

    return "[OK] PD Taking Signal"


@app.route("/readsignal")
def readsignal():
    global data, data_ready_flag
    if data_ready_flag:
        data_ready_flag = False
        return base64.b64encode(data)
    else:
        return "[Error] Data Not Ready"

