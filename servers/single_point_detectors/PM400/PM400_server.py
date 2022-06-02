# -*- coding: utf-8 -*-

"""server.py:
This module provides web API for
a remote PM400 optical powermeter
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220601"


import json
import time
import base64
import numpy as np
from flask import Flask, Response
from PM400 import pm

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = "PM400"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getValue")
def get_value():
    r = pm.buf.get_current()
    res = dict()
    res['success'] = True
    res['message'] = "Current value retrived"
    res['result'] = r
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/getSample/<count>")
def get_sample(count):
    count = int(count)
    assert count < pm.buf.length
    istart = pm.buf.current_data_index
    istop = istart + count
    if istop > pm.buf.length:
        istop = istop - pm.buf.length

    ci = pm.buf.current_data_index
    if istop > istart:
        while ci <= istop and ci >= istart:
            ci = pm.buf.current_data_index
            time.sleep(0.01)
    else:
        while ci >= istop or ci <= istart:
            ci = pm.buf.current_data_index
            time.sleep(0.01)

    r = pm.buf.get_slice(istart, istop)
    res = dict()
    res['success'] = True
    res['message'] = "Sample retrived"
    res['sample'] = base64.b64encode(r).decode()
    res['average'] = np.average(r)
    # we use unbiased estimator of stddev here, also known as sample stddev
    res['sample standard deviation'] = np.std(r, ddof=count-1)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
