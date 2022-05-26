# -*- coding: utf-8 -*-

"""FX_server.py:
This module provides web API for
linear image sensor emulator (for dev)
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220525"


import json
import time
import base64
import numpy as np
from flask import Flask, Response

app = Flask(__name__)


def fake_data_generator():
    xmin = 0
    xmax = 4 * np.pi
    phases = np.linspace(xmin, xmax, 64)
    while True:
        for i in phases:
            if i > xmax:
                i = xmin
            i = i + 0.5 * np.pi
            x = np.sin(np.linspace(xmin + i, xmax + i, 2048)) + np.random.rand(2048) * 0.2
            yield x


fake_data = fake_data_generator()

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "IdeaOptics_FX2000"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getImage")
def get_image():
    """
    All spectrometers are essentially linear image sensors from the program's perspective.
    To unify dev, getImage method is implemented for all linear image sensor like devices.
    You may have heard of ducks.
    """
    spectrum = next(fake_data)
    time.sleep(0.1)
    res = dict()
    res['success'] = True
    res['message'] = "Spectrum Taken"
    res['image'] = base64.b64encode(np.array(spectrum, dtype=np.float64)).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getspectrum")
def getspectrum():
    wavelengths = np.linspace(185.2, 1302.3, 2048)
    spectrum = next(fake_data)
    time.sleep(0.1)
    # print(wavelengths)
    # print(spectrum)
    res = dict()
    res['success'] = True
    res['message'] = "Spectrum Taken"
    res['wavelengths'] = base64.b64encode(np.array(wavelengths, dtype=np.float64)).decode()
    res['spectrum'] = base64.b64encode(np.array(spectrum, dtype=np.float64)).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setIntegrationTime/<t>")
def set_integration_time(t):
    t = int(t)
    res = dict()
    res['success'] = True
    res['message'] = "Integration Time Set"
    res['target'] = t
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setAverageTimes/<n>")
def set_average_times(n):
    n = int(n)
    res = dict()
    res['success'] = True
    res['message'] = "Average Times Set"
    res['target'] = n
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setBoxcarWidth/<n>")
def set_boxcar_width(n):
    n = int(n)
    res = dict()
    res['success'] = True
    res['message'] = "Boxcar Width Set"
    res['target'] = n
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')