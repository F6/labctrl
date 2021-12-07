# -*- coding: utf-8 -*-

"""shutter_emulator.py:
This module provides web API for
development emulation of shutter_server.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real environment, and that they return fabricated
data
"""


__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"

import json
from flask import Flask, Response


app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'shutter'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/off/<i>")
def off(i):
    res = dict()
    res['success'] = True
    res['message'] = "Turned OFF shutter"
    res['shutter_name'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/on/<i>")
def on(i):
    res = dict()
    res['success'] = True
    res['message'] = "Turned ON shutter"
    res['shutter_name'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


sht_status = 0

@app.route("/switch/<i>")
def switch(i):
    res = dict()
    res['success'] = True
    global sht_status
    sht_status += 1
    if sht_status%2:
        res['message'] = "Turned ON shutter"
    else:
        res['message'] = "Turned OFF shutter"
    res['shutter_name'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
