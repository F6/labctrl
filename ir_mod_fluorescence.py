# -*- coding: utf-8 -*-

"""ir_mod_fluorescence.py:
This module implements the IR Modulated Fluorescence multiple dimensional spectroscopy technic

In such experiments, a sample is illuminated with a sequence of 
ultrafast IR pulses and Visible pulses. The delay between these
pulses, the wavelength of these pulses are varied during the 
experiment scan. The fluorescence emitting from the sample after
the pulse excitations are collected and sent to spectrometer.

In our lab, we use TOPAS to generate IR(ps) pulses and Visible(fs)
pulses. The delay line is a retroreflector type delay line
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import time
import numpy as np
from functools import partial
from threading import Thread
from bokeh.models.widgets import Button

from ir_topas import irtopas
from visible_topas import vistopas
from remoteAPIs.shutter import remote_shutter_set_state
from remoteAPIs.andor_camera import remote_CCD_clear_list, remote_CCD_take_signal, remote_CCD_convert_latest
from remoteAPIs.linear_stage import remote_stage_moveabs
from remoteAPIs.photodiode import remote_PD_read_signal, remote_PD_take_signal
from unitconversion import ps_to_mm, wavenumber_to_nanometer
from expmsg import expmsg
from expdata import ExpData
from labconfig import lcfg
from main_doc import doc
from photodiode import callback_update_pd_data
from andor_camera import callback_update_figure_andor_camera


def scan_rounds(func, meta=''):
    """scan rounds for func"""
    def iterate(meta=dict()):
        for i, rd in enumerate(range(lcfg.scan_rounds)):
            expmsg("Scanning Round No.{}".format(rd))
            meta["Round"] = rd
            meta["iRound"] = i
            func(meta=meta)

    return iterate


def scan_delay(func, meta=''):
    """scan delays for func"""
    def iterate(meta=dict()):
        if lcfg.delay_line["Mode"] == "Range" or lcfg.delay_line["Mode"] == "ExtFile":
            for i, dl in enumerate(lcfg.delay_line["ScanList"]):
                expmsg("Setting delay to {dl} ps".format(dl=dl))
                target_abs_pos = lcfg.delay_line["ZeroAbsPos"] + ps_to_mm(dl)
                response = remote_stage_moveabs(target_abs_pos)
                expmsg("Stage Remote: " + response)
                expmsg("Waiting for remote to change delay...")
                # the delay line is set to move at 20mm/s
                time.sleep(abs(ps_to_mm(dl)/20) + 0.1)
                meta["Delay"] = dl
                meta["iDelay"] = i
                func(meta=meta)
        else:
            expmsg(
                "Delay is set manually, so no action has been taken")
            meta["Delay"] = "ManualDelay"
            meta["iDelay"] = 0
            func(meta=meta)

    return iterate


def scan_visible(func):
    """scan visibles for func"""
    def iterate(meta=dict()):
        if lcfg.visible_topas["Mode"] == "Range" or lcfg.visible_topas["Mode"] == "ExtFile":
            for i, wl in enumerate(lcfg.visible_topas["ScanList"]):
                expmsg("Setting wavelength to {wl} nm".format(wl=wl))
                vistopas.setWavelength(vistopas.interactions[11], wl)
                meta["Visible"] = wl
                meta["iVisible"] = i
                func(meta=meta)
        else:
            expmsg(
                "Visible wavelength is set manually, so no action has been taken")
            meta["Visible"] = "ManualVisible"
            meta["iVisible"] = 0
            func(meta=meta)

    return iterate


def scan_ir(func):
    """scan ir for func"""
    def iterate(meta=dict()):
        if lcfg.ir_topas["Mode"] == "Range" or lcfg.ir_topas["Mode"] == "ExtFile":
            for i, wn in enumerate(lcfg.ir_topas["ScanList"]):
                expmsg("Setting wavelength to {wn} cm-1".format(wn=wn))
                irtopas.setWavelength(
                    irtopas.interactions[2], wavenumber_to_nanometer(wn))
                meta["IR"] = wn
                meta["iIR"] = i
                func(meta=meta)
        else:
            expmsg(
                "IR wavelength is set manually, so no action has been taken")
            meta["IR"] = "ManualIR"
            meta["iIR"] = 0
            func(meta=meta)

    return iterate


def shutter_background(func):
    """if use shutter background, then the same thing is done twice with
     shutter open and closed. If do not use shutter background, then
     just leave the shutter status as is but mark shutter status as ON
     for our convenience.
     """
    def iterate(meta=dict()):
        if lcfg.shutter["UseShutterBackground"]:
            expmsg("Background is required, turning OFF shutter")
            response = remote_shutter_set_state(False)
            expmsg("Shutter Remote: " + response)
            meta["Shutter"] = "ShutterOff"
            func(meta=meta)
            expmsg("Background is taken, turning ON shutter")
            response = remote_shutter_set_state(True)
            expmsg("Shutter Remote: " + response)
            meta["Shutter"] = "ShutterOn"
            func(meta=meta)
        else:
            # this is wrong, because the shutter can be manually closed
            #  and we did not varify that before this assertion.
            # But this is fine because if the shutter is closed manually,
            #  then it is intentional for optical component tweaking.
            # The main task will always make sure that shutter is open
            #  before the experiment begins.
            meta["Shutter"] = "ShutterOn"
            func(meta=meta)

    return iterate


@scan_rounds
@scan_delay
@scan_visible
@scan_ir
@shutter_background
def __imfs_take_sample(meta=dict()):
    edata = meta["ExpData"]
    expmsg("Calling remote CCD to take signal...")
    response = remote_CCD_take_signal(
        "{rd}_{wl}_{wn}_{dl}_{sht}".format(rd=meta["Round"], wl=meta["Visible"], wn=meta["IR"], dl=meta["Delay"], sht=meta["Shutter"]))
    expmsg("CCD Remote: " + response + ", waiting for remote to take signal...")
    if lcfg.photodiode["TakePhotodiodeReference"]:
        expmsg(
            "Reference signal is required, calling remote PD to take reference while CCD is integrating")
        response = remote_PD_take_signal(
            lcfg.andor_camera["ExposureTime"])
        expmsg("PD Remote: " + response)
    time.sleep(lcfg.andor_camera["ExposureTime"] + 0.5)
    expmsg("Calling remote CCD to convert signal...")
    latest_signal = remote_CCD_convert_latest(
        "{fstm}round_{rd}".format(fstm=lcfg.file_stem, rd=meta["Round"]))
    if lcfg.photodiode["TakePhotodiodeReference"]:
        expmsg("Fetching remote PD data for reference")
        latest_ref = remote_PD_read_signal()
        doc.add_next_tick_callback(
            partial(callback_update_pd_data, latest_ref))
        avg = np.average(latest_ref)
        if meta["Shutter"] == "ShutterOn":
            edata.sig[meta["iDelay"], meta["iVisible"], meta["iIR"]] = avg
            edata.sigrefsum[meta["iDelay"],
                            meta["iVisible"], meta["iIR"]] += avg
        else:
            edata.bgref[meta["iDelay"], meta["iVisible"], meta["iIR"]] = avg
            edata.bgrefsum[meta["iDelay"],
                           meta["iVisible"], meta["iIR"]] += avg
    expmsg("Adding latest signal to dataset...")
    if meta["Shutter"] == "ShutterOn":
        edata.sig[meta["iDelay"], meta["iVisible"],
                  meta["iIR"]] = latest_signal
        edata.sigsum[meta["iDelay"], meta["iVisible"],
                     meta["iIR"]] += latest_signal
    else:
        edata.bg[meta["iDelay"], meta["iVisible"],
                 meta["iIR"]] = latest_signal
        edata.bgsum[meta["iDelay"], meta["iVisible"],
                    meta["iIR"]] += latest_signal
    # todo: add bg subtraction and other meta
    doc.add_next_tick_callback(
        partial(callback_update_figure_andor_camera, latest_signal))
    # if this the end of IR scan, call export
    if meta["iIR"] + 1 == len(lcfg.ir_topas["ScanList"]):
        edata.export("scandata/" + lcfg.file_stem +
                     "-Round{rd}".format(rd=meta["iRound"]))


def __imfs_task():
    """
    Implements the thread task for IR Modulated Fluorescence spectroscopy
    """
    max_retry = 3
    irtopas.getCalibrationInfo()
    expmsg("ps Topas found at " + str(irtopas.baseAddress) + ", " +
           "I'm using interaction " + str(irtopas.interactions[2]['Type']))
    vistopas.getCalibrationInfo()
    expmsg("visible Topas found at " + str(vistopas.baseAddress) + ", " +
           "I'm using interaction " + str(vistopas.interactions[11]['Type']))
    expmsg("Turning ON shutter before mapping")
    response = remote_shutter_set_state(True, max_retry)
    expmsg("Shutter Remote: " + response)

    # reallocate space for experiment data
    edata = ExpData(lcfg)

    expmsg(
        "Sync: Clearing remote signal list to reset sync for a new scan")
    response = remote_CCD_clear_list(max_retry)
    expmsg("CCD Remote: " + response)

    meta = dict()
    meta["ExpData"] = edata
    __imfs_take_sample(meta=meta)


def __callback_start_imfs_button():

    vis_shutter_is_open = vistopas.checkShutterStatus()
    if not vis_shutter_is_open:
        expmsg(
            "Error: Visible Shutter is closed! Program halted, please open the shutter and reclick the button to continue.")
        return
    ir_shutter_is_open = irtopas.checkShutterStatus()
    if not ir_shutter_is_open:
        expmsg(
            "Error: ps topas shutter is closed! Program halted, please open the shutter and reclick the button to continue.")
        return

    lcfg.experiment_type = "IMFS"
    thread = Thread(target=__imfs_task)
    thread.start()


button_start_imfs = Button(label='Start IMFS', button_type='success')
button_start_imfs.on_click(__callback_start_imfs_button)
