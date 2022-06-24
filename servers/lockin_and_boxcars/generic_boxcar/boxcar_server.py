# -*- coding: utf-8 -*-

"""server.py:
This module provides web API for
a remote generic boxcar controller (self made)
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220624"


import json
import time
import base64
import numpy as np
from flask import Flask, Response
from boxcar_HAL import boxcar, MCU_BASE_FREQUENCY, MODE_PWA, MODE_BOXCAR

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "Generic Boxcar Controller"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


last_fps_counter = 0

@app.route("/getBoxcarData")
def get_boxcar_data():
    # makes sure you can get new results every query
    global last_fps_counter
    while boxcar.fpscounter == last_fps_counter:
        time.sleep(0.01)
    r = boxcar.boxcar_data
    last_fps_counter = boxcar.fpscounter
    res = dict()
    res['success'] = True
    res['message'] = "Boxcar data retrived"
    res['result'] = base64.b64encode(r).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getPWAData")
def get_PWA_data():
    # PWA updates rapidly and only used in monitor, so do not need to block in general
    r = boxcar.PWA_data
    res = dict()
    res['success'] = True
    res['message'] = "PWA data retrived"
    res['result'] = base64.b64encode(r).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayBackgroundSampling/<delay>")
def set_delay_background_sampling(delay):
    delay = float(delay)
    actual_delay = boxcar.set_delay_background_sampling(delay)
    actual_delay = actual_delay / MCU_BASE_FREQUENCY
    res = dict()
    res['success'] = True
    res['message'] = "Background Sampling Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayIntegrate/<delay>")
def set_delay_integrate(delay):
    delay = float(delay)
    actual_delay = boxcar.set_delay_integrate(delay)
    actual_delay = actual_delay / MCU_BASE_FREQUENCY
    res = dict()
    res['success'] = True
    res['message'] = "Integrate Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayHold/<delay>")
def set_delay_hold(delay):
    delay = float(delay)
    actual_delay = boxcar.set_delay_hold(delay)
    actual_delay = actual_delay / MCU_BASE_FREQUENCY
    res = dict()
    res['success'] = True
    res['message'] = "Hold Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelaySignalSampling/<delay>")
def set_delay_signal_sampling(delay):
    delay = float(delay)
    actual_delay = boxcar.set_delay_signal_sampling(delay)
    actual_delay = actual_delay / MCU_BASE_FREQUENCY
    res = dict()
    res['success'] = True
    res['message'] = "Signal Sampling Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setDelayReset/<delay>")
def set_delay_reset(delay):
    delay = float(delay)
    actual_delay = boxcar.set_delay_reset(delay)
    actual_delay = actual_delay / MCU_BASE_FREQUENCY
    res = dict()
    res['success'] = True
    res['message'] = "Reset Delay Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setADCSamplingInterval/<delay>")
def set_adc_sampling_interval(delay):
    delay = float(delay)
    actual_delay = boxcar.set_adc_sampling_interval(delay)
    actual_delay = actual_delay / MCU_BASE_FREQUENCY
    res = dict()
    res['success'] = True
    res['message'] = "ADC Sampling Interval Set"
    res['target'] = actual_delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setADCSampleNumber/<n_sample>")
def set_adc_sample_number(n_sample):
    n_sample = int(n_sample)
    boxcar.set_adc_sample_number(n_sample)
    res = dict()
    res['success'] = True
    res['message'] = "ADC Sample Number Set"
    res['target'] = n_sample
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/setWorkingMode/<mode>")
def set_working_mode(mode):
    res = dict()
    if "PWA" == mode:
        boxcar.set_working_mode(MODE_PWA)
    elif "Boxcar" == mode:
        boxcar.set_working_mode(MODE_BOXCAR)
    else:
        res['success'] = False
        res['message'] = "Unsupported Working Mode"
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')

    res['success'] = True
    res['message'] = "Working Mode Set"
    res['target'] = mode
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

