# -*- coding: utf-8 -*-

"""camera.py:
This module implements the ToupCamera class for controlling
touptek cameras.

This camera is used as as a beam analyzer, so default mode
is software trigger mode.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221029"

import toupcam
from PIL import Image


class ToupCamera:
    def __init__(self):
        # default params
        self.hcam = None
        self.buf = None
        self.total = 0
        self.width = 0
        self.height = 0
        self.mode = "Trig"
        self.exposure = 100000 # 100ms default
        self.new_image_in_buffer = False

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
                print(
                    'Received TOUPCAM_EVENT_IMAGE, pull image ok, total = {}'.format(self.total))
                self.new_image_in_buffer = True
            except toupcam.HRESULTException:
                print('Received TOUPCAM_EVENT_IMAGE, pull image failed')
        else:
            print('event callback: {}'.format(nEvent))

    def configureCamera(self):
        # set image size to maximum
        toupcam.Toupcam.put_eSize(self.hcam, 0)
        # disable auto expo
        toupcam.Toupcam.put_AutoExpoEnable(self.hcam, 0)
        # set camera mode
        if self.mode == "Trig":
            self.setTrigMode()
        elif self.mode == "Video":
            self.setVideoMode()
        else:
            self.setTrigMode()
        # set camera temperature to 0
        # toupcam.Toupcam.put_Temperature(self.hcam, 0)
        # set camera exposure time to default value
        self.setExposureTime(self.exposure)
        # use raw data mode
        # toupcam.Toupcam.put_Option(toupcam.TOUPCAM_OPTION_RAW, 1)
        # use highest bit depth
        # toupcam.Toupcam.put_Option(toupcam.TOUPCAM_OPTION_BITDEPTH, 1)

    def setExposureTime(self, t: int):
        self.exposure = t
        toupcam.Toupcam.put_ExpoTime(self.hcam, self.exposure)

    def setTrigMode(self):
        # set camera mode to Software Trigger
        toupcam.Toupcam.put_Option(
            self.hcam, toupcam.TOUPCAM_OPTION_TRIGGER, 1)
        self.mode = "Trig"

    def setVideoMode(self):
        # set camera mode to Video Mode, no Trigger
        toupcam.Toupcam.put_Option(
            self.hcam, toupcam.TOUPCAM_OPTION_TRIGGER, 0)
        self.mode = "Video"

    def prepareBuffer(self):
        self.width, self.height = self.hcam.get_Size()
        bufsize = ((self.width * 24 + 31) // 32 * 4) * self.height
        print('image size: {} x {}, bufsize = {}'.format(
            self.width, self.height, bufsize))
        self.buf = bytes(bufsize)

    def run(self):
        """Enumerates all touptek cameras on device, 
        automatically opens the first camera and put the camera to 
        working mode.
        """
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

    def getImage(self):
        img = Image.frombuffer('RGB', (self.width, self.height), self.buf)
        # because image is retrived and used, flag current buffer as old
        self.new_image_in_buffer = False
        return img
    
    def getBuffer(self):
        # because image is retrived and used, flag current buffer as old
        self.new_image_in_buffer = False
        return self.buf


camera = ToupCamera()
camera.run()
# camera.stop()
