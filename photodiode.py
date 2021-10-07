# -*- coding: utf-8 -*-

"""photodiode.py:
This module provides the Bokeh UI widgets for 
testing and controlling the RIGOL Oscilloscope parameters

A photodiode is attached to the oscilloscope to read out
the reference values. The oscilloscope readings are from
visa instrument usb port and accessed from web API
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

import time
import numpy as np
from functools import partial
from tornado import gen
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import RadioButtonGroup, Button
from bokeh.plotting import figure

from expmsg import expmsg
from remoteAPIs.photodiode import remote_PD_take_signal, remote_PD_read_signal, RemotePDConnectionError
from labconfig import lcfg
from main_doc import doc


# define tools used
spectrum_tools = "box_select,box_zoom,lasso_select,pan,poly_select,tap,wheel_zoom,undo,redo,reset,save,crosshair,hover"


figure_photodiode = figure(title="Photodiode Signal", x_axis_label="Time over exposure",
                   y_axis_label="Intensity", plot_width=500, plot_height=310, tools=spectrum_tools)

intensities = np.zeros(50)
pd_x = np.array(range(50))

pd_data_source = ColumnDataSource(
    data=dict(pd_x=pd_x, intensities=intensities))

pd_waveform = figure_photodiode.line('pd_x', 'intensities',
                             line_width=1, source=pd_data_source)


@gen.coroutine
def callback_update_pd_data(pd_signal):
    new_data = dict()
    new_data['intensities'] = pd_signal
    new_data['pd_x'] = np.array(range(len(pd_signal)))
    pd_data_source.data = new_data


def __callback_pd_take_signal_button():

    try:
        response = remote_PD_take_signal(lcfg.andor_camera["ExposureTime"], 1)
        expmsg(response)
    except RemotePDConnectionError:
        expmsg("Nothing from remote, PD server is probably down.")
    for i in range(int(lcfg.andor_camera["ExposureTime"]) + 1):
        time.sleep(1)
    try:
        latest_signal = remote_PD_read_signal(1)
        expmsg("Reading PD signal...")
        doc.add_next_tick_callback(
            partial(callback_update_pd_data, latest_signal))
    except RemotePDConnectionError:
        print("Cannot connect to remote PD at converting stage, be careful with sync!")
        raise RemotePDConnectionError


button_pd_take_signal = Button(label='PD Take Signal', button_type='warning')
button_pd_take_signal.on_click(__callback_pd_take_signal_button)


def __callback_pd_reference_rbg(attr, old, new):
    lcfg.photodiode["TakePhotodiodeReference"] = [True, False][int(
        rbg_pd_reference.active)]
    lcfg.refresh_config()


rbg_pd_reference = RadioButtonGroup(
    labels=['Use PD to take reference', 'Do not use'], active=(0 if lcfg.photodiode["TakePhotodiodeReference"] else 1))
rbg_pd_reference.on_change('active', __callback_pd_reference_rbg)
