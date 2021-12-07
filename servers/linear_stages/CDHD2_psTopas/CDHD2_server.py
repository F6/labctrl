# -*- coding: utf-8 -*-

"""CDHD2_server.py:
This module provides web API for
a remote linear servo stage

the servo is the flat one now installed at A304, the driver
for the servo is servotronix CDHD2. See their manual for other
commands.

for manual tweaking and param adjustments, use the official
ServoStudio software. Disconnect COM port from servostudio 
before starting this app
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"

import json
from flask import Flask, Response

from CDHD2 import cdhd2 as stage

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'psTopas'
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

