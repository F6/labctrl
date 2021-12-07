# -*- coding: utf-8 -*-

"""ccd_emulator.py:
This module provides web API for
development emulation of Andor SOLIS EMCCD.

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real enviroment, and that they return fabricated
data
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


import base64
import numpy as np
import sif_reader
import random

import json
from flask import Flask, Response


app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'AndorSolisEMCCD'
    res['methods'] = ['takesignal']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/takesignal")
def takesignal():
    dfname = 'sample/1.sif'
    data, info = sif_reader.np_open(dfname)
    data = data[0][0]
    calib = info['Calibration_data']
    wl = np.zeros(len(data), dtype=np.float64)
    for i in range(len(data)):
        calx = i+1
        calibrated_wl = calib[0] + calib[1] * calx + calib[2] * \
            (calx**2) + calib[3] * (calx ** 3)
        wl[i] = calibrated_wl
        # EMULATOR: add random fluctuations to data
        data[i] = data[i] * (random.random() * 0.1 + 0.95)

    res = dict()
    res['success'] = True
    res['message'] = "Signal taken"
    res['wavelength'] = base64.b64encode(wl)
    res['data'] = base64.b64encode(data)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')