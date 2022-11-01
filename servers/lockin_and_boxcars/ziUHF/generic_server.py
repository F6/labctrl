# -*- coding: utf-8 -*-

"""ziUHF_proxy.py:
This module provides web proxy for
a remote ziUHF
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

import json
import base64
import numpy as np
from flask import Flask, Response
from ziUHF import uhf

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The proxy is ONLINE"
    res['name'] = "ziUHF"
    res['methods'] = ['get_value']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/get_value")
def get_value():
    value = uhf.get_value()
    res = dict()
    res['success'] = True
    res['message'] = "value:float"
    res['value'] = value
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getBoxcarData")
def get_boxcar_data():
    # makes sure you can get new results every query
    for i in range(100): # retry times
        r = uhf.get_data()
        if np.size(r) != 0:
            break
    if np.size(r) % 2:
        r = r[:-1]
    res = dict()
    res['success'] = True
    res['message'] = "Boxcar data retrived"
    res['result'] = base64.b64encode(r).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getPWAData")
def get_PWA_data():
    # PWA updates rapidly and only used in monitor, so do not need to block in general
    res = dict()
    res['success'] = True
    res['message'] = "PWA data retrived"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayBackgroundSampling/<delay>")
def set_delay_background_sampling(delay):
    delay = float(delay)
    actual_delay = delay
    res = dict()
    res['success'] = True
    res['message'] = "Background Sampling Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayIntegrate/<delay>")
def set_delay_integrate(delay):
    delay = float(delay)
    actual_delay = delay
    res = dict()
    res['success'] = True
    res['message'] = "Integrate Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayHold/<delay>")
def set_delay_hold(delay):
    delay = float(delay)
    actual_delay = delay
    res = dict()
    res['success'] = True
    res['message'] = "Hold Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelaySignalSampling/<delay>")
def set_delay_signal_sampling(delay):
    delay = float(delay)
    actual_delay = delay
    res = dict()
    res['success'] = True
    res['message'] = "Signal Sampling Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayReset/<delay>")
def set_delay_reset(delay):
    delay = float(delay)
    actual_delay = delay
    res = dict()
    res['success'] = True
    res['message'] = "Reset Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setADCSamplingInterval/<delay>")
def set_adc_sampling_interval(delay):
    delay = float(delay)
    actual_delay = delay
    res = dict()
    res['success'] = True
    res['message'] = "ADC Sampling Interval Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setADCSampleNumber/<n_sample>")
def set_adc_sample_number(n_sample):
    n_sample = int(n_sample)
    res = dict()
    res['success'] = True
    res['message'] = "ADC Sample Number Set"
    res['target'] = n_sample
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setWorkingMode/<mode>")
def set_working_mode(mode):
    res = dict()
    res['success'] = True
    res['message'] = "Working Mode Set"
    res['target'] = mode
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

