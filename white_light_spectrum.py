# -*- coding: utf-8 -*-

"""white_light_spectrum.py:
This module implements the white light spectrum test procedure.

In such experiments, a "white" laser pulse is prepared via
 supercontinuum generation. The pulse spectrum spans over
 a broad range of uv-visible-ir light. The pulse is sent to
 a monochromer and measured with camera to determine its
 spectrum, and the monochromer scans over and over again for
 for several hours to check the stability of the generated 
 white light.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"

import matplotlib.pyplot as plt
from remoteAPIs.touptek_camera import remote_ToupCam_settrigmode
from main_doc import doc
from spectrometer import callback_update_toupcam_figure
from remoteAPIs.touptek_camera import remote_ToupCam_setExposureTime, remote_ToupCam_get_signal

import time
import numpy as np
from functools import partial
from threading import Thread
from bokeh.models.widgets import Button

from labconfig import lcfg
from expmsg import expmsg
from expdata import ExpData
from general_setting import scan_rounds

from spectrometer import remote_ToupCam_open, remote_ToupCam_close, remote_ToupCam_trig, scan_monochromer

from spectrometer import monocalib


@scan_rounds
@scan_monochromer
def __wls_take_sample(meta=dict()):
    edata = meta["ExpData"]
    expmsg("Calling remote ToupCam to take signal...")
    response = remote_ToupCam_trig()
    expmsg("ToupCam Remote: " + response +
           ", waiting for remote to take signal...")
    time.sleep(lcfg.toupcamera["ExposureTime"]/1000000 + 1)
    expmsg("Calling remote ToupCam to convert signal...")
    expmsg("Retriving signal from remote ToupTek Camera")
    sig, ref = remote_ToupCam_get_signal(
        lcfg.toupcamera["SignalLower"],
        lcfg.toupcamera["SignalUpper"],
        lcfg.toupcamera["ReferenceLower"],
        lcfg.toupcamera["ReferenceUpper"]
    )

    expmsg("Adding latest signal to dataset...")

    edata.sig[meta["iMono"]] = sig
    edata.simsum[meta["iMono"]] += sig
    edata.ref[meta["iMono"]] = ref
    edata.refsum[meta["iMono"]] += ref

    # todo: add bg subtraction and other meta
    doc.add_next_tick_callback(
        partial(callback_update_toupcam_figure, sig, ref))
    # if this the end of IR scan, call export
    if meta["iMono"] + 1 == len(lcfg.monochromer["ScanList"]):
        edata.export("scandata/" + lcfg.file_stem +
                     "-Round{rd}".format(rd=meta["iRound"]))


def __wls_task():
    """
    Implements the thread task for IR Modulated Fluorescence spectroscopy
    """
    max_retry = 3

    # reallocate space for experiment data
    edata = ExpData(lcfg)

    expmsg(remote_ToupCam_settrigmode())
    expmsg(remote_ToupCam_setExposureTime(lcfg.toupcamera["ExposureTime"]))

    expmsg("Opening remote toupcam")
    response = remote_ToupCam_open(max_retry)
    expmsg("ToupCam Remote: " + response)

    time.sleep(1)

    time.sleep(3)

    meta = dict()
    meta["ExpData"] = edata
    __wls_take_sample(meta=meta)

    expmsg("Scanning done. Closing remote toupcam")
    response = remote_ToupCam_close(max_retry)
    expmsg("ToupCam Remote: " + response)


def __callback_start_wls_button():
    lcfg.experiment_type = "WLS"
    thread = Thread(target=__wls_task)
    thread.start()


button_start_wls = Button(label='Start WLS', button_type='success')
button_start_wls.on_click(__callback_start_wls_button)


def ass_spectrum(edata: ExpData):
    """assemble full spectrum from segmented spectrum"""
    for i, spec in enumerate(edata.sig):
        wl = lcfg.monochromer["ScanList"][i]
        xlen = len(spec)
        xwidth = lcfg.toupcamera["SpectralWidth"]
        xleft = wl - xwidth/2
        xright = wl + xwidth/2
        x = np.linspace(xleft, xright, xlen)
        plt.plot(x, spec)

    plt.savefig("spectrum.jpg", dpi=600)
