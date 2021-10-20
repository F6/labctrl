# -*- coding: utf-8 -*-

"""pumpprobe.py:
This module implements the IR Pump Visible Probe experiment procedure.

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
from linear_stage import scan_delay
from spectrometer import remote_ToupCam_open, remote_ToupCam_close, remote_ToupCam_trig, scan_monochromer

from spectrometer import monocalib


@scan_rounds
@scan_monochromer
@scan_delay
def __ipvp_take_sample(meta=dict()):
    edata = meta["ExpData"]
    expmsg("Calling remote ToupCam to take signal...")
    response = remote_ToupCam_trig()
    expmsg("ToupCam Remote: " + response +
           ", waiting for remote to take signal...")
    time.sleep(lcfg.toupcamera["ExposureTime"]/1000000 + 0.3)
    expmsg("Calling remote ToupCam to convert signal...")
    expmsg("Retriving signal from remote ToupTek Camera")
    sig, ref = remote_ToupCam_get_signal(
        lcfg.toupcamera["SignalLower"],
        lcfg.toupcamera["SignalUpper"],
        lcfg.toupcamera["ReferenceLower"],
        lcfg.toupcamera["ReferenceUpper"]
    )

    expmsg("Adding latest signal to dataset...")

    edata.sig[meta["iMono"], meta["iDelay"]] = sig
    edata.sigsum[meta["iMono"], meta["iDelay"]] += sig
    edata.ref[meta["iMono"], meta["iDelay"]] = ref
    edata.refsum[meta["iMono"], meta["iDelay"]] += ref

    # todo: add bg subtraction and other meta
    doc.add_next_tick_callback(
        partial(callback_update_toupcam_figure, sig, ref))
    # if this the end of delay scan, call export
    if meta["iDelay"] + 1 == len(lcfg.delay_line["ScanList"]):
        edata.export("scandata/" + lcfg.file_stem +
                     "-Round{rd}".format(rd=meta["iRound"]))


def __ipvp_task():
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


    meta = dict()
    meta["ExpData"] = edata
    __ipvp_take_sample(meta=meta)

    expmsg("Scanning done. Closing remote toupcam")
    response = remote_ToupCam_close(max_retry)
    expmsg("ToupCam Remote: " + response)


def __callback_start_ipvp_button():
    lcfg.experiment_type = "IPVP"
    thread = Thread(target=__ipvp_task)
    thread.start()


button_start_ipvp = Button(label='Start PumpProbe', button_type='success')
button_start_ipvp.on_click(__callback_start_ipvp_button)


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
