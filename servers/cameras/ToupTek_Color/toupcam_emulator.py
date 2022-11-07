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
import time
import json
import random
from flask import Flask, Response

# from camera import camera


def get_fake_image_buffer():
    image_lists = ["examples/0001.jpg", "examples/0002.jpg",
                   "examples/0003.jpg", "examples/0004.jpg", 
                   "examples/0005.jpg"]
    random_image_i = random.randint(0, 4)
    img_f = image_lists[random_image_i]
    with Image.open(img_f) as im:
        fakebuffer = im.tobytes()
    return fakebuffer


app = Flask(__name__)


@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'ToupTekCamera Full-Color (Emulator)'
    res['methods'] = []
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/openCamera')
def opencam():
    # caminfo = camera.run()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Opened"
    res['info'] = str("touptek camera emulator")
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/closeCamera')
def closecam():
    # camera.stop()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Closed"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/triggerCamera')
def trigcam():
    # camera.trig()
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
    res['buffer'] = base64.b64encode(get_fake_image_buffer()).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/trigAndGetBuffer')
def trig_and_get_buffer():
    res = dict()
    res['success'] = True
    res['message'] = "buffer:b64"
    res['width'] = 3584
    res['height'] = 2748
    res['buffer'] = base64.b64encode(get_fake_image_buffer()).decode()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/setTriggerMode')
def settrig():
    res = dict()
    res['success'] = True
    res['message'] = "Camera set to software trigger mode"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/setVideoMode')
def setvid():
    res = dict()
    res['success'] = True
    res['message'] = "Camera set to video mode"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route('/setExposureTime/<t>')
def set_exposure_time(t):
    t = int(t)
    res = dict()
    res['success'] = True
    res['message'] = "Camera Exposure Time has been set"
    res['target'] = str(t)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
