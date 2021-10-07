# -*- coding: utf-8 -*-

"""ccd_svr.py:
This module provides web API for
a remote Andor SOLIS EMCCD.

Since the andor camera's official APIs are quite complex and
hard to understand, this server simply mimics human behaviour
to control the camera.

Before starting the server app, make sure Andor SOLIS application
is open and auta-save is enabled. The directory for auto-save need
to be 'raw' in this folder.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import sif_reader
import re
import os
import base64

from flask import Flask

import win32gui
import win32con
import win32api
hwndMain = win32gui.FindWindow(None, "Andor SOLIS for Spectroscopy: CCD-08824")
if hwndMain:
    print("Andor SOLIS found, hwndMain is", hwndMain)
else:
    print("Warning: Andor SOLIS not found, is the program running?")
hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
if hwndChild:
    print("hwndChild found at", hwndChild)
else:
    print("Cannot found child for Andor SOLIS program main app, is the program dead? consider restart Andor SOLIS")


app = Flask(__name__)

siglist = []

auto_process_path = './raw/'
rs = re.compile(r'''(auto_\d+\.sif)''')


@app.route("/")
def online():
    return "[OK] The Server is ONLINE"


@app.route("/takesignal/<signal_id>")
def takesignal(signal_id):
    if signal_id in siglist:
        return "[SyncError] Signal {sid} has already been taken, possible poor connection, please check the sync! No action has been taken.".format(sid=signal_id)

    siglist.append(signal_id)

    print("[OK] Taking Signal {sid}".format(sid=signal_id))

    temp = win32api.PostMessage(
        hwndChild, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
    # print("Sent message F5, return code is", temp)
    temp = win32api.PostMessage(
        hwndChild, win32con.WM_KEYUP, win32con.VK_F5, 0)
    # print("Sent message F5 keyup, return code is", temp)

    return "[OK] Taking Signal {sid}".format(sid=signal_id)


@app.route("/clearsiglist")
def clearsiglist():
    siglist.clear()
    print("[OK] Signal list cleared, be careful with sync!")
    return "[OK] Signal list cleared, be careful with sync!"


@app.route("/convertlatest/<converted_path>")
def convertlatest(converted_path):
    if len(siglist) == 0:
        return "[SyncError] Signal list is empty, cannot determine how to rename the last file"

    file_l = list()
    for filename in os.listdir(auto_process_path):
        match_result = rs.match(filename)
        if match_result:
            file_l.append(filename)

    if len(file_l) == 0:
        print("[SyncError] Cannot find the required .sif file in automatic processing directory, did the CCD finish exposure?")
        return "[SyncError] Cannot find the required .sif file in automatic processing directory, did the CCD finish exposure?"

    if len(file_l) > 1:
        print("[Warning] more than one .sif file found in automatic processing directory! I'l use the last one")
        print(file_l)

    print("[OK] Converting latest .sif file according to signal list")
    dfname = auto_process_path + '/' + file_l[-1]
    data, info = sif_reader.np_open(dfname)
    data = data[0][0]

    calib = info['Calibration_data']

    sl = list()

    for i in range(len(data)):
        calx = i+1
        wl = calib[0] + calib[1] * calx + calib[2] * \
            (calx**2) + calib[3] * (calx ** 3)
        it = data[i]
        s = '{wl:.5f} {it}'.format(wl=wl, it=it)
        sl.append(s)

    cvtpath = '{cpt}/{sid}.txt'.format(cpt=converted_path, sid=siglist[-1])
    os.makedirs(os.path.dirname(cvtpath), exist_ok=True)

    with open(cvtpath, 'w') as f:
        f.write('\n'.join(sl))

    newdfname = '{cpt}/{sid}.sif'.format(cpt=converted_path, sid=siglist[-1])
    os.rename(dfname, newdfname)

    print("[OK] Convert done, file saved in {cvtpath}, sending back array to client".format(
        cvtpath=cvtpath))

    return base64.b64encode(data)


@app.route("/signaltaken/<signal_id>")
def signaltaken(signal_id):
    if signal_id in siglist:
        return "[True] Signal {sid} has already been taken".format(sid=signal_id)

    return "[False] Signal {sid} not taken yet".format(sid=signal_id)
