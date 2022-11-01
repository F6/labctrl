# -*- coding: utf-8 -*-

"""toupcamsvr.py:
This module provides web API for
a remote touptek camera

this camera is placed behind the 7IMUS monochromer
as the spectral detector
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

from flask import Flask

from PIL import Image
import numpy as np
import base64

import json
from flask import Flask, Response

from camera import camera

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'ToupTekCamera'
    res['methods'] = ['open', 'close', 'trig', 'getbuffer', 'getsignal', 'settrig', 'setvid', 'setexposuretime']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/openCamera')
def opencam():
    caminfo = camera.run()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Opened"
    res['info'] = str(caminfo)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/closeCamera')
def closecam():
    camera.stop()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Closed"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/triggerCamera')
def trigcam():
    camera.trig()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Trigged"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/getCurrentBuffer')
def get_image():
    res = dict()
    res['success'] = True
    res['message'] = "buffer:b64"
    res['buffer'] = base64.b64encode(camera.buf)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route('/triggerAndGetBuffer')

@app.route('/setTriggerMode')
def settrig():
    camera.stop()
    camera.mode = "Trigger"
    res = dict()
    res['success'] = True
    res['message'] = "Camera set to software trigger mode"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/setVideoMode')
def setvid():
    camera.stop()
    camera.mode = "Video"
    res = dict()
    res['success'] = True
    res['message'] = "Camera set to video mode"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/setExposureTime/<t>')
def set_exposure_time(t):
    camera.stop()
    t = int(t)
    camera.exposure = t
    res = dict()
    res['success'] = True
    res['message'] = "Camera Exposure Time has been set"
    res['target'] = str(t)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
