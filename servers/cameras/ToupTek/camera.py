# -*- coding: utf-8 -*-

"""camera.py:
This module implements the ToupCamera class for controlling
touptek cameras.

toupcam.py and toupcam.dll are required libraries and must
be put in path or the same directory of this file.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import toupcam
from PIL import Image

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
        # toupcam.Toupcam.put_Temperature(self.hcam, 0)

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


camera = ToupCamera()
camera.run()
camera.stop()