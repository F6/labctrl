# -*- coding: utf-8 -*-

"""ziUHF_sync_server.py:
This module provides web API for
a remote ziUHF
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221122"

import json
import base64
import numpy as np
from flask import Flask, Response
from ziUHF_sync import uhf

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "ziUHF"
    res['methods'] = ['getValue', 'getNewData']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getValue/<sample_count>")
def get_value(sample_count):
    sample_count = int(sample_count)
    value = uhf.get_value(sample_count=sample_count)
    res = dict()
    res['success'] = True
    res['message'] = "value:float"
    res['value'] = value
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getNewData/<sample_count>")
def get_new_data(sample_count):
    # makes sure you can get new results every query
    sample_count = int(sample_count)
    try:
        r = uhf.get_new_data(sample_count=sample_count)
        res = dict()
        res['success'] = True
        res['message'] = "Boxcar data retrived"
        res['result'] = base64.b64encode(r).decode()
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')
    except TimeoutError:
        r = np.array([])
        res = dict()
        res['success'] = False
        res['message'] = "Timeout waiting for {} samples! Check trigger or other connection issues.".format(
            sample_count)
        res['result'] = base64.b64encode(r).decode()


@app.route("/setDelayBackgroundSampling/<delay>")
def set_delay_background_sampling(delay: str):
    res = dict()
    res['success'] = False
    res['message'] = "Background Sampling Delay not implemented for ziUHF"
    res['param_bounce_back'] = delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setDelayIntegrate/<delay>")
def set_delay_integrate(delay: str):
    res = dict()
    res['success'] = False
    res['message'] = "Integrate Delay not implemented for ziUHF"
    res['param_bounce_back'] = delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setDelayHold/<delay>")
def set_delay_hold(delay: str):
    res = dict()
    res['success'] = False
    res['message'] = "Hold Delay not implemented for ziUHF"
    res['param_bounce_back'] = delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setDelaySignalSampling/<delay>")
def set_delay_signal_sampling(delay: str):
    res = dict()
    res['success'] = False
    res['message'] = "Signal Sampling Delay not implemented for ziUHF"
    res['param_bounce_back'] = delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setDelayReset/<delay>")
def set_delay_reset(delay: str):
    res = dict()
    res['success'] = False
    res['message'] = "Reset Delay not implemented for ziUHF"
    res['param_bounce_back'] = delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setWorkingMode/<mode>")
def set_working_mode(mode: str):
    res = dict()
    res['success'] = False
    res['message'] = "No need to set working mode for ziUHF, both modes are already active"
    res['param_bounce_back'] = mode
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
