# -*- coding: utf-8 -*-

"""andor_solis.py:
This module provides hooking for
 Andor SOLIS EMCCD.

Since the andor camera's official APIs are quite complex and
hard to understand, this server simply mimics human behaviour
to control the camera.

Before starting the server app, make sure Andor SOLIS application
is open and auta-save is enabled. The directory for auto-save need
to be 'raw' in this folder.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


import win32gui
import win32con
import win32api
import re
import os
import time

import numpy as np

import sif_reader

auto_process_path = './raw/'
rs = re.compile(r'''(auto_\d+\.sif)''')


class AndorSolisHooker:
    def __init__(self) -> None:
        self.siglist = list()
        self.hwndMain = win32gui.FindWindow(
            None, "Andor SOLIS for Spectroscopy: CCD-08824")
        if self.hwndMain:
            print("Andor SOLIS found, hwndMain is", self.hwndMain)
        else:
            print("Warning: Andor SOLIS not found, is the program running?")
        self.hwndChild = win32gui.GetWindow(self.hwndMain, win32con.GW_CHILD)
        if self.hwndChild:
            print("hwndChild found at", self.hwndChild)
        else:
            print("Cannot found child for Andor SOLIS program main app, is the program dead? consider restart Andor SOLIS")

    def find_auto_files(self):
        file_l = list()
        for filename in os.listdir(auto_process_path):
            match_result = rs.match(filename)
            if match_result:
                file_l.append(filename)

        return file_l

    def take_signal(self):
        # clean autoprocess directory
        for filename in self.find_auto_files():
            os.remove(auto_process_path + '/' + filename)

        temp = win32api.PostMessage(
            self.hwndChild, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
        time.sleep(0.05)
        # print("Sent message F5, return code is", temp)
        temp = win32api.PostMessage(
            self.hwndChild, win32con.WM_KEYUP, win32con.VK_F5, 0)
        # print("Sent message F5 keyup, return code is", temp)

        # wait until file appears
        fl = self.find_auto_files()
        while len(fl) < 1:
            time.sleep(0.1)
            fl = self.find_auto_files()

        # convert the .sif to our format and apply calibration
        dfname = auto_process_path + '/' + fl[-1]
        data, info = sif_reader.np_open(dfname)
        data = data[0][0]
        calib = info['Calibration_data']
        wl = np.zeros(len(data), dtype=np.float64)
        for i in range(len(data)):
            calx = i+1
            calibrated_wl = calib[0] + calib[1] * calx + calib[2] * \
                (calx**2) + calib[3] * (calx ** 3)
            wl[i] = calibrated_wl

        return wl, data


camera = AndorSolisHooker()
