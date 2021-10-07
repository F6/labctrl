# -*- coding: utf-8 -*-

"""andor_camera.py:
This module provides the Bokeh UI widgets for 
testing and controlling the Andor SOLIS EMCCD parameters
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


from functools import partial
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, TextInput
from tornado import gen

import time
import numpy as np

from remoteAPIs.andor_camera import remote_CCD_test_online, remote_CCD_take_signal, remote_CCD_check_signal, remote_CCD_convert_latest, RemoteCCDConnectionError
from expmsg import expmsg
from labconfig import lcfg
from main_doc import doc


ANDOR_CCD_PIXELS_WIDTH = 1600
spectrum_tools = "box_zoom,undo,redo,reset,save,crosshair,hover"
figure_andor_camera = figure(title="Andor SOLIS Camera", x_axis_label="Detector Pixel",
                             y_axis_label="Intensity", plot_width=500, plot_height=310, tools=spectrum_tools)

intensities = np.zeros(ANDOR_CCD_PIXELS_WIDTH)
rawdata_x = np.array(range(ANDOR_CCD_PIXELS_WIDTH))

waveform_data_source = ColumnDataSource(
    data=dict(rawdata_x=rawdata_x, intensities=intensities))

rawdata_waveform = figure_andor_camera.line('rawdata_x', 'intensities',
                                            line_width=1, source=waveform_data_source)


@gen.coroutine
def callback_update_figure_andor_camera(latest_signal):
    new_data = dict()
    new_data['intensities'] = latest_signal
    new_data['rawdata_x'] = rawdata_x
    waveform_data_source.data = new_data


def __callback_CCD_test_button():
    # test CCD online
    try:
        response = remote_CCD_test_online()
        expmsg(response)
    except Exception as inst:
        print(type(inst), inst.args)
        expmsg("Nothing from remote, CCD server is probably down.")


button_test_CCD_online = Button(label='Test CCD Server')
button_test_CCD_online.on_click(__callback_CCD_test_button)


def __callback_take_signal_button():
    lcfg.andor_camera["ManualSignalNo"] += 1
    signo = lcfg.andor_camera["ManualSignalNo"]
    while remote_CCD_check_signal('manual_{}'.format(signo), 3):
        signo = signo + 1
    try:
        response = remote_CCD_take_signal('manual_{}'.format(signo), 1)
        expmsg(response)
    except RemoteCCDConnectionError:
        expmsg("Nothing from remote, CCD server is probably down.")
    for i in range(int(lcfg.andor_camera["ExposureTime"]) + 1):
        time.sleep(1)
    try:
        latest_signal = remote_CCD_convert_latest("manual", 3)
        expmsg("Adding latest signal to dataset...")
        doc.add_next_tick_callback(
            partial(callback_update_figure_andor_camera, latest_signal))
    except RemoteCCDConnectionError:
        print("Cannot connect to remote CCD at converting stage, be careful with sync!")
        raise RemoteCCDConnectionError


take_signal_button = Button(label='CCD Take Signal', button_type='warning')
take_signal_button.on_click(__callback_take_signal_button)


def __callback_exposure_text_input(attr, old, new):
    try:
        lcfg.andor_camera["ExposureTime"] = float(
            ti_exposure_time.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_exposure_time = TextInput(
    title='Exposure time (each sample, s)', value=str(lcfg.andor_camera["ExposureTime"]))
ti_exposure_time.on_change(
    'value', __callback_exposure_text_input)
