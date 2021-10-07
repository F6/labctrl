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


from remoteAPIs.touptek_camera import remote_ToupCam_settrigmode
from main_doc import doc
from spectrometer import callback_update_toupcam_figure
from remoteAPIs.touptek_camera import remote_ToupCam_setExposureTime, remote_ToupCam_get_signal
__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import time
import numpy as np
from functools import partial
from threading import Thread
from bokeh.models.widgets import Button

from labconfig import lcfg
from expmsg import expmsg
from expdata import ExpData

from spectrometer import remote_ToupCam_open, remote_ToupCam_close, remote_ToupCam_trig, callback_update_monochromer_pos_div
from remoteAPIs.monochromer import remote_monochromer_get_position, remote_monochromer_moveto
from spectrometer import monocalib
from ir_mod_fluorescence import scan_delay


def scan_rounds(func, meta=''):
    """scan rounds for func"""
    def iterate(meta=dict()):
        for i, rd in enumerate(range(lcfg.scan_rounds)):
            expmsg("Scanning Round No.{}".format(rd))
            meta["Round"] = rd
            meta["iRound"] = i
            func(meta=meta)

    return iterate


def scan_monochromer(func, meta=''):
    """scan monochromer for func"""
    def iterate(meta=dict()):
        if lcfg.monochromer["Mode"] == "Range" or lcfg.monochromer["Mode"] == "ExtFile":
            for i, wl in enumerate(lcfg.monochromer["ScanList"]):
                expmsg("Setting monochromer to {} nm".format(wl))
                target_abs_pos = monocalib.lut(wl)
                response = remote_monochromer_moveto(target_abs_pos)
                expmsg("Monochromer Remote: " + response)
                expmsg("Waiting for remote to change wavelength...")
                # the delay line is set to move at 20mm/s
                while True:
                    time.sleep(0.2)
                    response = remote_monochromer_get_position()
                    doc.add_next_tick_callback(
                        partial(callback_update_monochromer_pos_div, response))
                    if response == target_abs_pos + lcfg.monochromer["ZeroAbsPos"]:
                        break
                expmsg("Monochromer wavelength setting done")
                meta["Mono"] = wl
                meta["iMono"] = i
                func(meta=meta)
        else:
            expmsg(
                "Monochromer wavelength is set manually, so no action has been taken")
            meta["Mono"] = "ManualMono"
            meta["iMono"] = 0
            func(meta=meta)

    return iterate


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
