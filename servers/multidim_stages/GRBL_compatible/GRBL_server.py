# -*- coding: utf-8 -*-

"""server.py:
This module provides web API for
a remote GRBL compatible G-Code controller
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220601"


import json
from flask import Flask, Response
from GRBL_streamer import grbl

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "GRBL"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/g/<gcode>")
def send_gcode(gcode):
    r = grbl.send_gcode(gcode)
    res = dict()
    res['success'] = True
    res['message'] = "Command streamed to controller"
    res['result'] = r
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/g1blocking/<gcode>")
def autohome(gcode):
    r = grbl.blocking_g1_command(gcode)
    res = dict()
    res['success'] = True
    res['message'] = "Command streamed to controller"
    res['result'] = r
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
