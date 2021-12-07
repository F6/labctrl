# -*- coding: utf-8 -*-

"""shutter_server.py:
This module provides web API for
a remote shutter controller

the shutter controller is the self-made one (gray aluminum box)
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"

import json
from flask import Flask, Response

from shutter import sht

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
    sht.shutter_off(i)
    res = dict()
    res['success'] = True
    res['message'] = "Turned OFF shutter"
    res['shutter_name'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/on/<i>")
def on(i):
    sht.shutter_on(i)
    res = dict()
    res['success'] = True
    res['message'] = "Turned ON shutter"
    res['shutter_name'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/switch/<i>")
def switch(i):
    sht.switch_shutter(i)
    res = dict()
    res['success'] = True
    if sht.shutter_status[i]:
        res['message'] = "Turned ON shutter"
    else:
        res['message'] = "Turned OFF shutter"
    res['shutter_name'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
