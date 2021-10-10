# -*- coding: utf-8 -*-

"""toupcamsvr.py:
This module provides web API for
a remote touptek camera

this camera is placed behind the 7IMUS monochromer
as the spectral detector
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


from flask import Flask

import toupcam
from PIL import Image
import numpy as np
import base64


class ToupCamera:
    def __init__(self):
        self.hcam = None
        self.buf = None
        self.total = 0
        self.width = 0
        self.height = 0
        self.mode = "Video"
        self.exposure = 100000

    # the vast majority of callbacks come from toupcam.dll/so/dylib internal threads
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == toupcam.TOUPCAM_EVENT_IMAGE:
            ctx.CameraCallback(nEvent)

    def CameraCallback(self, nEvent):
        if nEvent == toupcam.TOUPCAM_EVENT_IMAGE:
            try:
                self.hcam.PullImageV2(self.buf, 24, None)
                self.total += 1
                print('pull image ok, total = {}'.format(self.total))
            except toupcam.HRESULTException:
                print('pull image failed')
        else:
            print('event callback: {}'.format(nEvent))

    def configureCamera(self):
        # set image size to max (2592 * 1944)
        toupcam.Toupcam.put_eSize(self.hcam, 0)
        # disable auto expo
        toupcam.Toupcam.put_AutoExpoEnable(self.hcam, 0)
        # set camera mode
        if self.mode == "Trigger":
            self.setTrigMode()
        else:
            self.setVideoMode()
        # set camera temp to 0
        toupcam.Toupcam.put_Temperature(self.hcam, 0)

        self.setExposureTime(self.exposure)
        # use raw data mode
        # toupcam.Toupcam.put_Option(toupcam.TOUPCAM_OPTION_RAW, 1)
        # use highest bit depth
        # toupcam.Toupcam.put_Option(toupcam.TOUPCAM_OPTION_BITDEPTH, 1)

    def setExposureTime(self, t: int):
        toupcam.Toupcam.put_ExpoTime(self.hcam, t)

    def setTrigMode(self):
        # set camera mode to Software Trigger
        toupcam.Toupcam.put_Option(
            self.hcam, toupcam.TOUPCAM_OPTION_TRIGGER, 1)

    def setVideoMode(self):
        # set camera mode to Video Mode, no Trigger
        toupcam.Toupcam.put_Option(
            self.hcam, toupcam.TOUPCAM_OPTION_TRIGGER, 0)

    def prepareBuffer(self):
        self.width, self.height = self.hcam.get_Size()
        bufsize = ((self.width * 24 + 31) // 32 * 4) * self.height
        print('image size: {} x {}, bufsize = {}'.format(
            self.width, self.height, bufsize))
        self.buf = bytes(bufsize)

    def run(self):
        a = toupcam.Toupcam.EnumV2()
        if len(a) > 0:
            caminfo = '{}: flag = {:#x}, preview = {}, still = {}'.format(
                a[0].displayname, a[0].model.flag, a[0].model.preview, a[0].model.still)
            print(caminfo)
            for r in a[0].model.res:
                print('\t = [{} x {}]'.format(r.width, r.height))
            self.hcam = toupcam.Toupcam.Open(a[0].id)
            if self.hcam:
                try:
                    self.configureCamera()
                    self.prepareBuffer()

                    # start pull mode, once image is ready, cameraCallback is responsible for reading the image from camera buffer and post processing
                    if self.buf:
                        try:
                            self.hcam.StartPullModeWithCallback(
                                self.cameraCallback, self)
                        except toupcam.HRESULTException:
                            print('failed to start camera')
                    # input('press ENTER to exit')
                finally:
                    pass
                #     self.hcam.Close()
                #     self.hcam = None
                #     self.buf = None
            else:
                print('failed to open camera')
        else:
            caminfo = 'no camera found'
            print(caminfo)
        return caminfo

    def stop(self):
        self.hcam.Close()

    def trig(self):
        toupcam.Toupcam.Trigger(self.hcam, 1)

    def getimg(self):
        img = Image.frombuffer('RGB', (self.width, self.height), self.buf)
        return img


cam = ToupCamera()
cam.run()
cam.stop()
counter = 0

app = Flask(__name__)


@app.route('/')
def online():
    return "[OK] ToupTek Camera server is ONLINE"


@app.route('/open')
def opencam():
    global cam
    caminfo = cam.run()
    return "[OK] " + caminfo


@app.route('/close')
def closecam():
    global cam
    cam.stop()
    return "[OK] Closed camera"


@app.route('/trig')
def trigcamera():
    cam.trig()
    return "[OK] Trigged camera"


@app.route('/g')
def get_image():
    return cam.buf


@app.route('/gs/<b>')
def get_signal(b):
    siglower, sigupper, reflower, refupper = map(int, b.split())
    img = cam.getimg()
    rgbsum = np.sum(np.asarray(img), axis=2)
    sig = np.sum(rgbsum[siglower:sigupper], axis=0)
    ref = np.sum(rgbsum[reflower:refupper], axis=0)
    return base64.b64encode(np.array((sig, ref), dtype=np.uint32))


@app.route('/settrig')
def settrig():
    cam.stop()
    cam.mode = "Trigger"
    return "[OK] Camera set to software trigger mode"


@app.route('/setvid')
def setvid():
    cam.stop()
    cam.mode = "Video"
    return "[OK] Camera set to video mode"


@app.route('/t/<t>')
def set_exposure_time(t):
    cam.stop()
    t = int(t)
    cam.exposure = t
    return "[OK] Camera set Exposure Time to {} us".format(t)
