# -*- coding: utf-8 -*-

"""topas_proxy.py:
This module proxies the web API for
a remote topas.

A proxy is required because the original Topas API requires authentication
for network devices, and cannot be easily accessed from virtual subnets.

Arbitrary code execution is possible for such proxy app, so do not use the
proxy on public network
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"

import json
from flask import Flask, Response

from .topas_REST import Topas4Controller
from .utils import *

serial_number = 17627
interaction_used = 2

print("Connecting to topas server" + str(serial_number))
topas = Topas4Controller(serial_number)
if topas.baseAddress == None:
    print("Cannot connect to Topas! Is the topas server program running?")
    input()
topas.getCalibrationInfo()
print("Topas found at " + str(topas.baseAddress) + ", " +
               "I'm using interaction " + str(topas.interactions[interaction_used]['Type']))

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The proxy is ONLINE"
    res['name'] = 'psTopas'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/set/wavelength/nm/<i>")
def set_wavelength_nm(i):
    i = float(i)
    topas.setWavelength(topas.interactions[interaction_used], i)
    res = dict()
    res['success'] = True
    res['message'] = "Wavelength set to target"
    res['target_nm'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/set/wavelength/cm-1/<i>")
def set_wavelength_wn(i):
    i = float(i)
    target = wavenumber_to_nanometer(i)
    topas.setWavelength(topas.interactions[interaction_used], target)
    res = dict()
    res['success'] = True
    res['message'] = "Wavelength set to target"
    res['target_nm'] = target
    res['target_cm-1'] = i
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
