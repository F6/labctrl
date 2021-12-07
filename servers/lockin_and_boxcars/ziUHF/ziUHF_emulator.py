# -*- coding: utf-8 -*-

"""ziUHF_emulator.py:
This module provides emulator for
a remote ziUHF
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

import json
from flask import Flask, Response
import random
import time

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
    value = random.random()
    time.sleep(0.1)
    res = dict()
    res['success'] = True
    res['message'] = "value:float"
    res['value'] = value
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

