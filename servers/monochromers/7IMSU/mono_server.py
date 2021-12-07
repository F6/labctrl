# -*- coding: utf-8 -*-

"""monosvr.py:
This module provides web API for
a remote monochromer 7IMSU
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import json
from flask import Flask, Response
from mono import mono

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "7IMSU"
    res['methods'] = ['getpos', 'setpos', 'stop']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getpos")
def getpos():
    pos = mono.getpos()
    pos = "{:.3f}".format(pos)
    res = dict()
    res['success'] = True
    res['message'] = "pos:.3f"
    res['pos'] = pos
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/setpos/<tpos>")
def setpos(tpos):
    res = mono.setpos(int(tpos))
    res = dict()
    res['success'] = True
    res['message'] = "Monochromer moved to target wavelength"
    res['target'] = tpos
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/stop")
def stop():
    mono.stopmoving()
    res = dict()
    res['success'] = True
    res['message'] = "Monochromer stopped moving"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
