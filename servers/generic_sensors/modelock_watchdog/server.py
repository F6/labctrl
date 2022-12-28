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
watchdog = ModelockWatchdog(com="COM6")
watchdog.start_continuous_read()

app = Flask(__name__)

counter_values = [0] * 10
times = [0.0] * 10

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
    # ========= TEMPORARY =========
    counter_values_last = watchdog.status["Counter"]
    timestamp_last = watchdog.status["Timestamp"]
    counter_values.append(counter_values_last)
    times.append(timestamp_last)
    counter_values_first = counter_values.pop(0)
    timestamp_first = times.pop(0)
    frequency = (counter_values_last - counter_values_first) / (timestamp_last - timestamp_first)
    # print("Calculated Frequency: {} kHz".format(frequency/1000))
    # ========= END TEMPORARY =========
    res = dict()
    res['success'] = True
    res['message'] = "data:dict"
    res['data'] = watchdog.status
    res['data']['Frequency'] = frequency
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
