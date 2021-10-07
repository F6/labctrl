# -*- coding: utf-8 -*-

"""linear_stage.py:
This module provides the Bokeh UI widgets for 
testing and controlling the linear stage parameters
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import base64
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput

from remoteAPIs.linear_stage import remote_stage_online, remote_stage_moveabs
from expmsg import expmsg
from unitconversion import ps_to_mm

from labconfig import lcfg


def __callback_stage_test_button():
    try:
        response = remote_stage_online()
        expmsg(response)
    except Exception as inst:
        print(type(inst), inst.args)
        expmsg("Nothing from remote, stage server is probably down.")


button_test_stage_online = Button(label='Test IR Stage Server')
button_test_stage_online.on_click(__callback_stage_test_button)


def __callback_move_stage_text_input(attr, old, new):
    try:
        delay = float(ti_move_stage.value)
        lcfg.delay_line["ManualPos"] = lcfg.delay_line["ZeroAbsPos"] + \
            ps_to_mm(delay)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_move_stage = TextInput(title='Manually set delay to (ps)', value="")
ti_move_stage.on_change('value', __callback_move_stage_text_input)


def __callback_move_stage_button():
    try:
        response = remote_stage_moveabs(lcfg.delay_line["ManualPos"])
        expmsg(response)
    except Exception as inst:
        print(type(inst), inst.args)
        expmsg("Nothing from remote, stage server is probably down.")


button_move_stage = Button(label='Move stage', button_type='warning')
button_move_stage.on_click(__callback_move_stage_button)


def __callback_zero_delay_text_input(attr, old, new):
    try:
        lcfg.delay_line["ZeroAbsPos"] = float(
            ti_zero_delay.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_zero_delay = TextInput(
    title='Zero delay position (mm)', value=str(lcfg.delay_line["ZeroAbsPos"]))
ti_zero_delay.on_change(
    'value', __callback_zero_delay_text_input)


def __callback_delay_mode_rbg(attr, old, new):
    mode = int(rbg_delay_mode.active)
    lcfg.delay_line["Mode"] = lcfg.scan_modes[mode]
    if mode == 0:
        ti_delay_start.visible = False
        ti_delay_step.visible = False
        ti_delay_stop.visible = False
        fi_delay_list.visible = False
    elif mode == 1:
        ti_delay_start.visible = True
        ti_delay_step.visible = True
        ti_delay_stop.visible = True
        fi_delay_list.visible = False
    elif mode == 2:
        ti_delay_start.visible = False
        ti_delay_step.visible = False
        ti_delay_stop.visible = False
        fi_delay_list.visible = True
    lcfg.refresh_config()


#title="Delay Scan Mode",
rbg_delay_mode = RadioButtonGroup(
    labels=['Manual', 'Range', 'Ext File'], active=(lcfg.scan_modes.index(lcfg.delay_line["Mode"])))
rbg_delay_mode.on_change('active', __callback_delay_mode_rbg)


def __callback_delay_range_start_text_input(attr, old, new):
    try:
        lcfg.delay_line["Start"] = float(
            ti_delay_start.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_delay_start = TextInput(
    title='Scan range: Start (ps)', value=str(lcfg.delay_line["Start"]))
ti_delay_start.on_change(
    'value', __callback_delay_range_start_text_input)


def __callback_delay_range_stop_text_input(attr, old, new):
    try:
        lcfg.delay_line["Stop"] = float(
            ti_delay_stop.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_delay_stop = TextInput(
    title='Scan range: Stop (ps)', value=str(lcfg.delay_line["Stop"]))
ti_delay_stop.on_change(
    'value', __callback_delay_range_stop_text_input)


def __callback_delay_range_step_text_input(attr, old, new):
    try:
        lcfg.delay_line["Step"] = float(
            ti_delay_step.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_delay_step = TextInput(
    title='Scan range: Step (ps)', value=str(lcfg.delay_line["Step"]))
ti_delay_step.on_change(
    'value', __callback_delay_range_step_text_input)


def __callback_delay_list_file_input(attr, old, new):
    expmsg("Delay list inputed")
    fcontent = base64.b64decode(fi_delay_list.value).decode()
    # print(fcontent)
    lcfg.delay_line["Mode"] = "ExtFile"
    rbg_delay_mode.active = lcfg.scan_modes.index(lcfg.delay_line["Mode"])
    lcfg.delay_line["ExternalList"] = list(map(float, fcontent.split()))
    lcfg.refresh_config()


fi_delay_list = FileInput(accept=".txt")
fi_delay_list.on_change('value', __callback_delay_list_file_input)
