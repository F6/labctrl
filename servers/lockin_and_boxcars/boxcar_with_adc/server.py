# -*- coding: utf-8 -*-

"""boxcar_server.py:
This module provides web API for
a remote boxcar integrator
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220529"


import json
import base64
import numpy as np
from flask import Flask, Response
from boxcar import boxcar

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "Boxcar Controller"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getValue")
def get_value():
    """
    Boxcars read data in batch. The data is sequencial
    It is possible to read out a whole batch at once by get value
    """
    values = boxcar.get_value()
    res = dict()
    res['success'] = True
    res['message'] = "Values retrived"
    res['image'] = base64.b64encode(np.array(values, dtype=np.float64)).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getAverage")
def get_average():
    """
    Most of the times we do not the whole data batch.
    For single point detectors without reference, we typically only need it's statistics
    """
    average = boxcar.get_averaged_value()
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