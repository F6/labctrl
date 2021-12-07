# -*- coding: utf-8 -*-

"""PMC48MT6_server.py:
This module provides web API for
a remote stepper motor stage

The controller is from Ningbo Adhon, no document or information
of their product can be found online, so not sure if the driver
works for all their devices.

The company seems to be closed years ago, so this will probably
be replaced soon.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"

import json
from flask import Flask, Response
from PMC48MT6 import PMC48MT6


# on creation of the server, the serial port is open and then never
# released, not sure if this will cause any strange behaviour, so be
# cautious for this
stage = PMC48MT6()

app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'fsTopas'
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

