# -*- coding: utf-8 -*-

"""emulator.py:
This module provides web API for
development emulation of server.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real enviroment, and that they return fabricated
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
    res['name'] = "ETHGASN"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    res = dict()
    res['success'] = True
    res['message'] = "Moved to target position"
    res['target'] = pos
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/autohome")
def autohome():
    res = dict()
    res['success'] = True
    res['message'] = "Moved to Home and reset Home position via limit switch"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


