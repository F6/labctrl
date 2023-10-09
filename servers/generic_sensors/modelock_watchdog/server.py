# -*- coding: utf-8 -*-

"""server.py:
This module provides web API for
a remote modelock watchdog module
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221227"

import json
import base64
import numpy as np
from flask import Flask, Response

from modelock_watchdog_HAL import ModelockWatchdog
from unit_conversions import rh_to_ah
watchdog = ModelockWatchdog(com="COM3")
watchdog.start_continuous_read()

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "ModelockWatchdog"
    res['methods'] = ['getSensorData', 'setSensorConfig']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getSensorData")
def get_sensor_data():
    res = dict()
    res['success'] = True
    res['message'] = "data:dict"
    data = watchdog.status.copy()
    # ============ BEGIN TEMPORARY ============
    # This part should be put into HAL
    # Intensity = 0 for now because adc is not enabled in
    # firmware yet.
    data['Intensity'] = 0
    data['AbsoluteHumidity1'] = rh_to_ah(
        data['Temperature1'] + 273.15,
        data["Humidity1"],
        )
    data['AbsoluteHumidity2'] = rh_to_ah(
        data['Temperature2'] + 273.15,
        data["Humidity2"],
        )
    # ============ END TEMPORARY ============
    res['data'] = data
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setSensorConfig/<config>")
def set_sensor_config(config):
    config = base64.urlsafe_b64decode(config).decode()
    config = json.loads(config)
    res = dict()
    res['success'] = True
    res['message'] = "Sensor config updated"
    # [TODO]: Implementation
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
