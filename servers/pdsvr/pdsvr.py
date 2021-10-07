# -*- coding: utf-8 -*-

"""pd_svr.py:
This module provides web API for
a remote photodiode hooked to a oscilloscope.

the oscilloscope is the black one (RIGOL), connect PD to CH2
and set auto trigger mode. Set measurement on CH2 to be AREA,
and adjust the waveform until a single pulse is on the screen

RIGOL oscilloscopes need UltraSigma be installed to access,
the resource name string can also be found in UltraSigma. 
Download it from RIGOL official support website.
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

import pyvisa as visa
rm = visa.ResourceManager()
# reslist = rm.list_resources()
inst = rm.open_resource('USB0::0x1AB1::0x0515::MS5A222002010::INSTR')

inst.write(":MEASure:SOURce CHANnel2")
inst.write(":MEASure:SOURce?")
print(inst.read())

inst.write(":MEASure:STATistic:ITEM MARea,CHANnel2")

import time

data = np.zeros(1)
data_ready_flag = False

app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] PD Server is ONLINE"


def pdtask(exposure_time):
    global data, data_ready_flag
    ms = list()
    exposure_time = float(exposure_time)
    zero = time.time()
    while True:
        try:
            if time.time() - zero > exposure_time:
                break
            inst.write(":MEASure:STATistic:ITEM? CURRent,MARea")
            ms.append(inst.read())

        except visa.errors.VisaIOError:
            pass
    data = np.array([float(i) for i in ms], dtype=np.float32)
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

