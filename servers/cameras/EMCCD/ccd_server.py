# -*- coding: utf-8 -*-

"""ccd_server.py:
This module provides web API for
a remote Andor SOLIS EMCCD.

Since the andor camera's official APIs are quite complex and
hard to understand, this server simply mimics human behaviour
to control the camera.

Before starting the server app, make sure Andor SOLIS application
is open and auta-save is enabled. The directory for auto-save need
to be 'raw' in this folder.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


import base64

import json
from flask import Flask, Response

from andor_solis import camera

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'AndorSolisEMCCD'
    res['methods'] = ['takesignal']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/takesignal")
def takesignal():
    wl, data = camera.take_signal()
    res = dict()
    res['success'] = True
    res['message'] = "Signal taken"
    res['wavelength'] = base64.b64encode(wl)
    res['data'] = base64.b64encode(data)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')