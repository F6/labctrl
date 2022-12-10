# -*- coding: utf-8 -*-

"""emulator.py:
This module provides web API emulator for
a remote DRV2665 high voltage signal generator

The signal generator is the self-made black one
used to control piezo actuators.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221208"

import json
import time
import base64

import numpy as np
from flask import Flask, Response


app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'DRV2665'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/updateWaveform/<waveform_json>")
def update_waveform(waveform_json):
    """
    [TODO] add device abstraction and change direct update buffer to handle
    other params.
    For now this is nearly identical to RAW update_buffer, need to handle other
    params such as gain, frequency.
    """
    waveform_json = json.loads(waveform_json)
    waveform = waveform_json["waveform"]
    # drv2665.update_buffer(waveform)
    print("Update Waveform:", waveform)
    res = dict()
    res['success'] = True
    res['message'] = "Buffer Updated"
    res['name'] = 'DRV2665'
    res['waveform_length'] = len(waveform)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


# =========== BEGIN RAW COMMANDS =============

@app.route("/updateBuffer/<buffer_json>")
def update_buffer(buffer_json: str):
    buffer_json = json.loads(buffer_json)
    buffer = buffer_json["buffer"]
    # drv2665.update_buffer(buffer)
    print("Update Buffer:", buffer)
    res = dict()
    res['success'] = True
    res['message'] = "Buffer Updated"
    res['name'] = 'DRV2665'
    res['buffer_length'] = len(buffer)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/readStatus")
def read_status():
    # drv2665.read_status()
    status = {
        "ChipID": "UNKNOWN",
        "FIFO": "Empty",
        "Gain": "25Vpp",
        "Input": "Digital",
        "OverrideEnable": False,
        "Standby": False,
        "Reset": False,
        "Timeout": "20ms"
    }
    res = dict()
    res['success'] = True
    res['message'] = "Local status cache updated"
    res['name'] = 'DRV2665'
    res['status'] = status
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setGain/<gain_option>")
def set_gain(gain_option: str):
    try:
        # drv2665.set_gain(gain_option)
        pass
    except ValueError:
        res = dict()
        res['success'] = False
        res['message'] = "Unsupported gain option"
        res['name'] = 'DRV2665'
        res['gain_option'] = gain_option
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')
    res = dict()
    res['success'] = True
    res['message'] = "Gain set"
    res['name'] = 'DRV2665'
    res['gain_option'] = gain_option
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setInputType/<input_type>")
def set_input_type(input_type: str):
    try:
        # drv2665.set_input_type(input_type)
        pass
    except ValueError:
        res = dict()
        res['success'] = False
        res['message'] = "Unsupported input type option"
        res['name'] = 'DRV2665'
        res['input_type'] = input_type
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')
    res = dict()
    res['success'] = True
    res['message'] = "Input type set"
    res['name'] = 'DRV2665'
    res['input_type'] = input_type
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/overideEnable")
def override_enable():
    # drv2665.override_enable()
    res = dict()
    res['success'] = True
    res['message'] = "Set enable control mode to Override Enable"
    res['name'] = 'DRV2665'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/useDeviceLogicEnable")
def use_device_logic_enable():
    # drv2665.use_device_logic_enable()
    res = dict()
    res['success'] = True
    res['message'] = "Set enable control mode to Use Device Logic Enable"
    res['name'] = 'DRV2665'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setTimeout/<timeout_option>")
def set_timeout(timeout_option: str):
    try:
        # drv2665.set_timeout(timeout_option)
        pass
    except ValueError:
        res = dict()
        res['success'] = False
        res['message'] = "Unsupported timeout option"
        res['name'] = 'DRV2665'
        res['input_type'] = timeout_option
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')
    res = dict()
    res['success'] = True
    res['message'] = "Timeout set"
    res['name'] = 'DRV2665'
    res['input_type'] = timeout_option
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/activate")
def activate():
    # drv2665.activate()
    res = dict()
    res['success'] = True
    res['message'] = "Device activated"
    res['name'] = 'DRV2665'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/standby")
def standby():
    # drv2665.standby()
    res = dict()
    res['success'] = True
    res['message'] = "Device standby"
    res['name'] = 'DRV2665'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/reset")
def reset():
    # drv2665.reset()
    res = dict()
    res['success'] = True
    res['message'] = "Device reset"
    res['name'] = 'DRV2665'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/readChipID")
def read_chip_id():
    # drv2665.read_chip_id()
    status = {
        "ChipID": "UNKNOWN",
        "FIFO": "Empty",
        "Gain": "25Vpp",
        "Input": "Digital",
        "OverrideEnable": False,
        "Standby": False,
        "Reset": False,
        "Timeout": "20ms"
    }
    res = dict()
    res['success'] = True
    res['message'] = "Device chip ID read"
    res['name'] = 'DRV2665'
    res['chip_id'] = status["ChipID"]
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
