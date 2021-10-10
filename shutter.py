# -*- coding: utf-8 -*-

"""shutter.py:
This module provides the Bokeh UI widgets for 
testing and controlling shutter mode
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"

from labconfig import lcfg
from bokeh.models.widgets import RadioButtonGroup, Button

from expmsg import expmsg
from remoteAPIs.shutter import remote_shutter_set_state


def __callback_rgb(attr, old, new):
    lcfg.shutter["UseShutterBackground"] = [True, False][int(
        rbg_shutter_background.active)]
    lcfg.refresh_config()


rbg_shutter_background = RadioButtonGroup(
    labels=['Use shutter to take background', 'Do not use'], active=(0 if lcfg.shutter["UseShutterBackground"] else 1))
rbg_shutter_background.on_change('active', __callback_rgb)


def __callback_turn_on_shutter_button():
    try:
        response = remote_shutter_set_state(1)
        expmsg(response)
    except Exception as inst:
        print(type(inst), inst.args)
        expmsg("Nothing from remote, shutter server is probably down.")


button_turn_on_shutter = Button(label='Turn on shutter')
button_turn_on_shutter.on_click(__callback_turn_on_shutter_button)


def __callback_turn_off_shutter_button():
    try:
        response = remote_shutter_set_state(0)
        expmsg(response)
    except Exception as inst:
        print(type(inst), inst.args)
        expmsg("Nothing from remote, shutter server is probably down.")


button_turn_off_shutter = Button(label='Turn off shutter')
button_turn_off_shutter.on_click(__callback_turn_off_shutter_button)

sht_no = 0


def __callback_change_shutter_button():
    global sht_no
    sht_no += 1
    try:
        response = remote_shutter_set_state(sht_no % 2)
        expmsg(response)
    except Exception as inst:
        print(type(inst), inst.args)
        expmsg("Nothing from remote, shutter server is probably down.")


button_change_shutter = Button(label='Change shutter')
button_change_shutter.on_click(__callback_change_shutter_button)


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
