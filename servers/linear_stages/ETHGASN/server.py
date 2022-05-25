# -*- coding: utf-8 -*-

"""server.py:
This module provides web API for
a remote linear stepper stage

"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"


import json
from flask import Flask, Response
from ETHGASN import stage


SOFTMIN = -220
SOFTMAX = 150

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
    if pos < SOFTMIN or pos > SOFTMAX:
        res = dict()
        res['success'] = False
        res['message'] = "Cannot move to target because it exceeds software limit!"
        res['target'] = pos
        res['software_min'] = SOFTMIN
        res['software_max'] = SOFTMAX
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')
    stage.moveabs(pos)
    res = dict()
    res['success'] = True
    res['message'] = "Moved to target position"
    res['target'] = pos
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/autohome")
def autohome():
    stage.autohome()
    res = dict()
    res['success'] = True
    res['message'] = "Moved to Home and reset Home position via limit switch"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
