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


@app.route('/open')
def opencam():
    caminfo = camera.run()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Opened"
    res['info'] = str(caminfo)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/close')
def closecam():
    camera.stop()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Closed"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/trig')
def trigcam():
    camera.trig()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Trigged"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/getbuffer')
def get_image():
    res = dict()
    res['success'] = True
    res['message'] = "buffer:b64"
    res['buffer'] = base64.b64encode(camera.buf)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/getsignal/<b>')
def get_signal(b):
    siglower, sigupper, reflower, refupper = map(int, b.split())
    img = camera.getimg()
    rgbsum = np.sum(np.asarray(img), axis=2)
    print(rgbsum.max())
    sig = np.sum(rgbsum[siglower:sigupper], axis=0)
    ref = np.sum(rgbsum[reflower:refupper], axis=0)
    res = dict()
    res['success'] = True
    res['message'] = "signal:b64,uint32; reference:b64,uint32"
    res['signal'] = base64.b64encode(sig)
    res['reference'] = base64.b64encode(ref)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/settrig')
def settrig():
    camera.stop()
    camera.mode = "Trigger"
    res = dict()
    res['success'] = True
    res['message'] = "Camera set to software trigger mode"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/setvid')
def setvid():
    camera.stop()
    camera.mode = "Video"
    res = dict()
    res['success'] = True
    res['message'] = "Camera set to video mode"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/setexposuretime/<t>')
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
