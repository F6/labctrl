# -*- coding: utf-8 -*-

"""ir_topas.py:
This module provides the Bokeh UI widgets for 
testing and controlling the IR(ps) topas parameters
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import base64
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput

from expmsg import expmsg

from labconfig import lcfg
from remoteAPIs.topas_REST import Topas4Emulator, Topas4Controller
from remoteAPIs.configs import ir_topas_serial_number
from configs import DEV_TEST

if DEV_TEST:
    irtopas = Topas4Emulator(ir_topas_serial_number)
else:
    irtopas = Topas4Controller(ir_topas_serial_number)


def __callback_check_ir_topas():
    irtopas = Topas4Controller(ir_topas_serial_number)
    if irtopas.baseAddress is None:
        expmsg("Error: Topas cannot be found, is Topas Server running?")
    else:
        irtopas.getCalibrationInfo()
        expmsg("ir Topas found at " + str(irtopas.baseAddress) + ", " +
               "I'm using interaction " + str(irtopas.interactions[11]['Type']))


button_check_ir_topas = Button(label='Check ir topas status')
button_check_ir_topas.on_click(__callback_check_ir_topas)


def __callback_ir_topas_mode_rbg(attr, old, new):
    mode = int(rbg_ir_topas_mode.active)
    lcfg.ir_topas["Mode"] = lcfg.scan_modes[mode]
    if mode == 0:
        ti_ir_topas_start.visible = False
        ti_ir_topas_step.visible = False
        ti_ir_topas_stop.visible = False
        fi_ir_topas_list.visible = False
    elif mode == 1:
        ti_ir_topas_start.visible = True
        ti_ir_topas_step.visible = True
        ti_ir_topas_stop.visible = True
        fi_ir_topas_list.visible = False
    elif mode == 2:
        ti_ir_topas_start.visible = False
        ti_ir_topas_step.visible = False
        ti_ir_topas_stop.visible = False
        fi_ir_topas_list.visible = True
    lcfg.refresh_config()



#title="ir_topas Scan Mode",
rbg_ir_topas_mode = RadioButtonGroup(
    labels=['Manual', 'Range', 'Ext File'], active=(lcfg.scan_modes.index(lcfg.ir_topas["Mode"])))
rbg_ir_topas_mode.on_change('active', __callback_ir_topas_mode_rbg)


def __callback_ir_topas_range_start_text_input(attr, old, new):
    try:
        lcfg.ir_topas["Start"] = float(
            ti_ir_topas_start.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_ir_topas_start = TextInput(
    title='Scan range: Start (cm-1)', value=str(lcfg.ir_topas["Start"]))
ti_ir_topas_start.on_change(
    'value', __callback_ir_topas_range_start_text_input)


def __callback_ir_topas_range_stop_text_input(attr, old, new):
    try:
        lcfg.ir_topas["Stop"] = float(
            ti_ir_topas_stop.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_ir_topas_stop = TextInput(
    title='Scan range: Stop (cm-1)', value=str(lcfg.ir_topas["Stop"]))
ti_ir_topas_stop.on_change(
    'value', __callback_ir_topas_range_stop_text_input)


def __callback_ir_topas_range_step_text_input(attr, old, new):
    try:
        lcfg.ir_topas["Step"] = float(
            ti_ir_topas_step.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_ir_topas_step = TextInput(
    title='Scan range: Step (cm-1)', value=str(lcfg.ir_topas["Step"]))
ti_ir_topas_step.on_change(
    'value', __callback_ir_topas_range_step_text_input)


def __callback_ir_topas_list_file_input(attr, old, new):
    expmsg("ir topas list inputed")
    fcontent = base64.b64decode(fi_ir_topas_list.value).decode()
    # print(fcontent)
    lcfg.ir_topas["Mode"] = "ExtFile"
    rbg_ir_topas_mode.active = lcfg.scan_modes.index(lcfg.ir_topas["Mode"])
    lcfg.ir_topas["ExternalList"] = list(map(float, fcontent.split()))
    lcfg.refresh_config()


fi_ir_topas_list = FileInput(accept=".txt")
fi_ir_topas_list.on_change('value', __callback_ir_topas_list_file_input)
