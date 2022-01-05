# -*- coding: utf-8 -*-

"""CRD507_server.py:
This module provides web RESTful API for
a remote linear stage or rotator
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220105"

import json
from flask import Flask, Response

from CRD507 import stage

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'CRD507'
    res['methods'] = ["moveabs", "autohome", "rotateabs"]
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    stage.moveabs(pos)
    res = dict()
    res['success'] = True
    res['message'] = "Moved to target position"
    res['target'] = pos
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/rotateabs/<deg>")
def rotateabs(deg):
    deg = float(deg)
    stage.rotateabs(deg)
    res = dict()
    res['success'] = True
    res['message'] = "Rotated to target position"
    res['target'] = deg
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

