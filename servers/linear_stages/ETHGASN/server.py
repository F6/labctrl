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
from ETHGASN import controller

# SOFTMIN = -40
# SOFTMAX = 135

SOFTMIN = -999
SOFTMAX = 999

LEISAI_SOFTMIN = -268
LEISAI_SOFTMAX = 135

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "ETHGASN"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')



@app.route("/reset")
def reset():
    res = dict()
    res['success'] = True
    res['message'] = "Reset ETHGASN controller board, all stored position info are lost!"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/yaskawa/moveabs/<pos>")
def yaskawa_moveabs(pos):
    SOFTMIN = -100
    SOFTMAX = 160
    pos = float(pos)
    if pos < SOFTMIN or pos > SOFTMAX:
        res = dict()
        res['success'] = False
        res['message'] = "Cannot move to target because it exceeds software limit!"
        res['target'] = pos
        res['software_min'] = SOFTMIN
        res['software_max'] = SOFTMAX
        res['linear_stage'] = "Yaskawa"
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')
    controller.yaskawa.moveabs(pos)
    res = dict()
    res['success'] = True
    res['message'] = "Moved to target position"
    res['target'] = pos
    res['linear_stage'] = "Yaskawa"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/yaskawa/disable")
def yaskawa_disable():
    controller.yaskawa.diasble()
    res = dict()
    res['success'] = True
    res['message'] = "The linear stage is DISABLED"
    res['name'] = "ETHGASN.yaskawa"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/leisai/moveabs/<pos>")
def leisai_moveabs(pos):
    pos = float(pos)
    if pos < LEISAI_SOFTMIN or pos > LEISAI_SOFTMAX:
        res = dict()
        res['success'] = False
        res['message'] = "Cannot move to target because it exceeds software limit!"
        res['target'] = pos
        res['software_min'] = LEISAI_SOFTMIN
        res['software_max'] = LEISAI_SOFTMAX
        res['linear_stage'] = "LeiSai"
        res = json.dumps(res)
        return Response(res, status=200, mimetype='application/json')
    controller.leisai.moveabs(pos)
    res = dict()
    res['success'] = True
    res['message'] = "Moved to target position"
    res['target'] = pos
    res['linear_stage'] = "LeiSai"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

