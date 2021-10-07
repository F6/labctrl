# -*- coding: utf-8 -*-

"""visible_topas.py:
This module provides the Bokeh UI widgets for 
testing and controlling the visible(fs) topas parameters
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import base64
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput

from expmsg import expmsg

from labconfig import lcfg
from remoteAPIs.topas_REST import Topas4Emulator, Topas4Controller
from remoteAPIs.configs import vis_topas_serial_number
from configs import DEV_TEST


if DEV_TEST:
    vistopas = Topas4Emulator(vis_topas_serial_number)
else:
    vistopas = Topas4Controller(vis_topas_serial_number)


def __callback_check_topas_vis():
    vistopas = Topas4Controller(vis_topas_serial_number)
    if vistopas.baseAddress is None:
        expmsg("Error: Topas cannot be found, is Topas Server running?")
    else:
        vistopas.getCalibrationInfo()
        expmsg("visible Topas found at " + str(vistopas.baseAddress) + ", " +
               "I'm using interaction " + str(vistopas.interactions[11]['Type']))


button_check_topas_vis = Button(label='Check visible topas status')
button_check_topas_vis.on_click(__callback_check_topas_vis)


def __callback_visible_topas_mode_rbg(attr, old, new):
    mode = int(rbg_visible_topas_mode.active)
    lcfg.visible_topas["Mode"] = lcfg.scan_modes[mode]
    if mode == 0:
        ti_visible_topas_start.visible = False
        ti_visible_topas_step.visible = False
        ti_visible_topas_stop.visible = False
        fi_visible_topas_list.visible = False
    elif mode == 1:
        ti_visible_topas_start.visible = True
        ti_visible_topas_step.visible = True
        ti_visible_topas_stop.visible = True
        fi_visible_topas_list.visible = False
    elif mode == 2:
        ti_visible_topas_start.visible = False
        ti_visible_topas_step.visible = False
        ti_visible_topas_stop.visible = False
        fi_visible_topas_list.visible = True
    lcfg.refresh_config()


#title="visible_topas Scan Mode",
rbg_visible_topas_mode = RadioButtonGroup(
    labels=['Manual', 'Range', 'Ext File'], active=(lcfg.scan_modes.index(lcfg.visible_topas["Mode"])))
rbg_visible_topas_mode.on_change('active', __callback_visible_topas_mode_rbg)


def __callback_visible_topas_range_start_text_input(attr, old, new):
    try:
        lcfg.visible_topas["Start"] = float(
            ti_visible_topas_start.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_visible_topas_start = TextInput(
    title='Scan range: Start (nm)', value=str(lcfg.visible_topas["Start"]))
ti_visible_topas_start.on_change(
    'value', __callback_visible_topas_range_start_text_input)


def __callback_visible_topas_range_stop_text_input(attr, old, new):
    try:
        lcfg.visible_topas["Stop"] = float(
            ti_visible_topas_stop.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_visible_topas_stop = TextInput(
    title='Scan range: Stop (nm)', value=str(lcfg.visible_topas["Stop"]))
ti_visible_topas_stop.on_change(
    'value', __callback_visible_topas_range_stop_text_input)


def __callback_visible_topas_range_step_text_input(attr, old, new):
    try:
        lcfg.visible_topas["Step"] = float(
            ti_visible_topas_step.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_visible_topas_step = TextInput(
    title='Scan range: Step (nm)', value=str(lcfg.visible_topas["Step"]))
ti_visible_topas_step.on_change(
    'value', __callback_visible_topas_range_step_text_input)


def __callback_visible_topas_list_file_input(attr, old, new):
    expmsg("visible topas list inputed")
    fcontent = base64.b64decode(fi_visible_topas_list.value).decode()
    # print(fcontent)
    lcfg.visible_topas["Mode"] = "ExtFile"
    rbg_visible_topas_mode.active = lcfg.scan_modes.index(
        lcfg.visible_topas["Mode"])
    lcfg.visible_topas["ExternalList"] = list(map(float, fcontent.split()))
    lcfg.refresh_config()


fi_visible_topas_list = FileInput(accept=".txt")
fi_visible_topas_list.on_change(
    'value', __callback_visible_topas_list_file_input)
