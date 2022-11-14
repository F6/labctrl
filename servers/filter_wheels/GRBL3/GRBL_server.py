# -*- coding: utf-8 -*-

"""server.py:
This module provides web API for
a remote GRBL compatible G-Code controller
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221109"


import json
from flask import Flask, Response
from grbl_controller import GRBLController

grbl = GRBLController('COM14')

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "GRBL2"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/moveabs/<xyz>")
def moveabs(xyz:str):
    xyz = xyz.split(',')
    x, y, z = list(map(float, xyz))
    grbl.blocking_moveabs(x, y, z)
    res = dict()
    res['success'] = True
    res['name'] = 'GRBL2'
    res['message'] = "Moved to target position"
    res['target'] = [x, y, z]
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
