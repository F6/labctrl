# -*- coding: utf-8 -*-

"""server.py:
This module provides web API for
a remote linear servo stage

the servo is the silver one now installed at A304, the driver
for the servo is Autonics KR-55MC and the controller is Beijing
ART Technology USB1020.

for manual tweaking and param adjustments, use the official
ART software.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"


import json
from flask import Flask, Response
from USB1020 import USB1020

stage = USB1020()
# the device is never released! but this is ok because when the
#  user shuts down the server, the resources are automatically
#  released by the os
# this can interfere with other programs trying to
#  control the device, so just close the server before tweaking
stage.createDevice()

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "IRPumpVisProbe"
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


@app.route("/autohome")
def autohome():
    stage.autohome()
    res = dict()
    res['success'] = True
    res['message'] = "Moved to Home and reset Home position via limit switch"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
