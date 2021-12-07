# -*- coding: utf-8 -*-

"""Aerotech_server.py:
This module provides web RESTful API for
a remote linear stage

The linear stage is now installed at A304 for TR experiment
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

import json
from flask import Flask, Response

from Aerotech import stage

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'AeroTech_NView'
    res['methods'] = ["moveabs", "autohome"]
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


@app.route("/absolute")
def absolute():
    stage.set_absolute_mode()
    res = dict()
    res['success'] = True
    res['message'] = "Position mode switched to ABSOLUTE, be aware of limits!"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
