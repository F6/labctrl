# -*- coding: utf-8 -*-

"""FX_server.py:
This module provides web API for
a remote FX(ideaoptics) spectrometer
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220522"


import json
import base64
import numpy as np
from flask import Flask, Response
from FX import spectrometer

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "IdeaOptics_FX2000"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getspectrum")
def getspectrum():
    wavelengths = spectrometer.wavelengths
    spectrum = spectrometer.get_spectrum()
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
    spectrometer.set_integration_time(t)
    res = dict()
    res['success'] = True
    res['message'] = "Integration Time Set"
    res['target'] = t
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setAverageTimes/<n>")
def set_average_times(n):
    n = int(n)
    spectrometer.set_average_times(n)
    res = dict()
    res['success'] = True
    res['message'] = "Average Times Set"
    res['target'] = n
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setBoxcarWidth/<n>")
def set_boxcar_width(n):
    n = int(n)
    spectrometer.set_boxcar_width(n)
    res = dict()
    res['success'] = True
    res['message'] = "Boxcar Width Set"
    res['target'] = n
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')