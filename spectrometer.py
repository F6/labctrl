# -*- coding: utf-8 -*-

"""spectrometer.py:
This module implements the spectrometer controlling and tweaking 
methods and UI widgets

2 components are available for seperated control: the 7IMSU monochromer
and the ToupTek camera

"""

from remoteAPIs.touptek_camera import remote_ToupCam_setExposureTime
from remoteAPIs.touptek_camera import remote_ToupCam_settrigmode, remote_ToupCam_setvidmode
from remoteAPIs.touptek_camera import remote_ToupCam_open, remote_ToupCam_close, remote_ToupCam_trig
from remoteAPIs.touptek_camera import remote_ToupCam_get_signal
__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

from functools import partial
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.models.widgets import Button, TextInput, Div, Spinner, RadioButtonGroup, FileInput
from tornado import gen

import base64
import numpy as np

from expmsg import expmsg
from labconfig import lcfg
from main_doc import doc


from remoteAPIs.monochromer import remote_monochromer_online, remote_monochromer_moveto, remote_monochromer_get_position, remote_monochromer_stop


# region monochromer

def __callback_monochromer_test_button():
    try:
        response = remote_monochromer_online()
        expmsg(response)
    except Exception as inst:
        print(type(inst), inst.args)
        expmsg("Nothing from remote, Monochromer server is probably down.")


button_test_monochromer_online = Button(label='Test Monochromer Server')
button_test_monochromer_online.on_click(__callback_monochromer_test_button)


def __callback_ti_monochromer_target(attr, old, new):
    try:
        pos = int(ti_monochromer_target.value)
        lcfg.monochromer["ManualRawPos"] = pos
        res = remote_monochromer_moveto(pos)
        expmsg(res)

    except Exception as inst:
        print(type(inst), inst.args)


ti_monochromer_target = TextInput(
    title='Move monochromer to (step)', value=str(lcfg.monochromer["ManualRawPos"]))
ti_monochromer_target.on_change('value', __callback_ti_monochromer_target)


def __callback_button_stop_monochromer():
    res = remote_monochromer_stop()
    expmsg(res)


button_stop_mono = Button(label="stop monochromer moving")
button_stop_mono.on_click(__callback_button_stop_monochromer)


div_mono_pos = Div(text='<pre>Monochromer Pos:</pre>')

def callback_update_monochromer_pos_div(p):
    div_mono_pos.text = '<pre>Monochromer Pos: {p}</pre>'.format(p=p)

def __callback_button_get_mono_pos():
    p = remote_monochromer_get_position()
    doc.add_next_tick_callback(partial(callback_update_monochromer_pos_div, p))



button_get_mono_pos = Button(label="get monochromer pos")
button_get_mono_pos.on_click(__callback_button_get_mono_pos)


def __callback_monochromer_mode_rbg(attr, old, new):
    mode = int(rbg_monochromer_mode.active)
    lcfg.monochromer["Mode"] = lcfg.scan_modes[mode]
    if mode == 0:
        ti_monochromer_start.visible = False
        ti_monochromer_step.visible = False
        ti_monochromer_stop.visible = False
        fi_monochromer_list.visible = False
    elif mode == 1:
        ti_monochromer_start.visible = True
        ti_monochromer_step.visible = True
        ti_monochromer_stop.visible = True
        fi_monochromer_list.visible = False
    elif mode == 2:
        ti_monochromer_start.visible = False
        ti_monochromer_step.visible = False
        ti_monochromer_stop.visible = False
        fi_monochromer_list.visible = True
    lcfg.refresh_config()


#title="monochromer Scan Mode",
rbg_monochromer_mode = RadioButtonGroup(
    labels=['Manual', 'Range', 'Ext File'], active=(lcfg.scan_modes.index(lcfg.monochromer["Mode"])))
rbg_monochromer_mode.on_change('active', __callback_monochromer_mode_rbg)


def __callback_monochromer_range_start_text_input(attr, old, new):
    try:
        lcfg.monochromer["Start"] = float(
            ti_monochromer_start.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_monochromer_start = TextInput(
    title='Scan range: Start (nm)', value=str(lcfg.monochromer["Start"]))
ti_monochromer_start.on_change(
    'value', __callback_monochromer_range_start_text_input)


def __callback_monochromer_range_stop_text_input(attr, old, new):
    try:
        lcfg.monochromer["Stop"] = float(
            ti_monochromer_stop.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_monochromer_stop = TextInput(
    title='Scan range: Stop (nm)', value=str(lcfg.monochromer["Stop"]))
ti_monochromer_stop.on_change(
    'value', __callback_monochromer_range_stop_text_input)


def __callback_monochromer_range_step_text_input(attr, old, new):
    try:
        lcfg.monochromer["Step"] = float(
            ti_monochromer_step.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_monochromer_step = TextInput(
    title='Scan range: Step (nm)', value=str(lcfg.monochromer["Step"]))
ti_monochromer_step.on_change(
    'value', __callback_monochromer_range_step_text_input)


def __callback_monochromer_list_file_input(attr, old, new):
    expmsg("monochromer list inputed")
    fcontent = base64.b64decode(fi_monochromer_list.value).decode()
    # print(fcontent)
    lcfg.monochromer["Mode"] = "ExtFile"
    rbg_monochromer_mode.active = lcfg.scan_modes.index(
        lcfg.monochromer["Mode"])
    lcfg.monochromer["ExternalList"] = list(map(float, fcontent.split()))
    lcfg.refresh_config()


fi_monochromer_list = FileInput(accept=".txt")
fi_monochromer_list.on_change('value', __callback_monochromer_list_file_input)


# monochromer calibration


mono_calib_source = ColumnDataSource(lcfg.monochromer["CalibrationTable"])

columns = [
    TableColumn(field="Wavelength", title="Wavelength (nm)"),
    TableColumn(field="Step", title="Step"),
]
mono_calib_table = DataTable(
    source=mono_calib_source, columns=columns, width=400, height=280)




class MonoCalibration:
    def __init__(self, calibration_table: dict, model: str) -> None:
        # calibration table: k - wavelength, v - steps
        self.ct = calibration_table
        self.cm = model
        self.lut = None

    def getlut(self):
        x = self.ct["Wavelength"]
        y = self.ct["Step"]
        if self.cm == "Linear":
            from scipy import stats
            res = stats.linregress(x, y)

            def lut(x):
                return int(res.intercept + res.slope * x)
        self.lut = lut
        return lut

monocalib = MonoCalibration(lcfg.monochromer["CalibrationTable"], lcfg.monochromer["CalibrationModel"])
monocalib.getlut()

# endregion

# region ToupCam
spectrum_tools = "box_zoom,undo,redo,reset,save,crosshair,hover"

figure_toup_camera_sig = figure(title="Signal", x_axis_label="Detector Pixel",
                                y_axis_label="Intensity", plot_width=500, plot_height=310, tools=spectrum_tools)

figure_toup_camera_ref = figure(title="Reference", x_axis_label="Detector Pixel",
                                y_axis_label="Intensity", plot_width=500, plot_height=310, tools=spectrum_tools)

figure_toup_camera_delta = figure(title="Delta", x_axis_label="Detector Pixel",
                                  y_axis_label="Intensity", plot_width=500, plot_height=310, tools=spectrum_tools)


signals = np.zeros(lcfg.toupcamera["Width"])
refs = np.zeros(lcfg.toupcamera["Width"])
deltas = signals-refs
rawdata_x = np.array(range(lcfg.toupcamera["Width"]))

waveform_data_source = ColumnDataSource(
    data=dict(rawdata_x=rawdata_x, signals=signals, refs=refs, deltas=deltas))

waveform_sig = figure_toup_camera_sig.line('rawdata_x', 'signals',
                                           line_width=1, source=waveform_data_source)
waveform_ref = figure_toup_camera_ref.line('rawdata_x', 'refs',
                                           line_width=1, source=waveform_data_source)
waveform_delta = figure_toup_camera_delta.line('rawdata_x', 'deltas',
                                               line_width=1, source=waveform_data_source)


@gen.coroutine
def callback_update_toupcam_figure(sig, ref):
    new_data = dict()
    new_data['signals'] = sig
    new_data['refs'] = ref
    new_data['deltas'] = sig-ref
    new_data['rawdata_x'] = rawdata_x
    waveform_data_source.data = new_data


def __callback_siglower(attr, old, new):
    lcfg.toupcamera["SignalLower"] = int(spinner_siglower.value)


spinner_siglower = Spinner(title="Signal Lower", low=0,
                           high=lcfg.toupcamera["Height"], step=1, value=lcfg.toupcamera["SignalLower"], width=80)
spinner_siglower.on_change('value', __callback_siglower)


def __callback_sigupper(attr, old, new):
    lcfg.toupcamera["SignalUpper"] = int(spinner_sigupper.value)


spinner_sigupper = Spinner(title="Signal Upper", low=0,
                           high=lcfg.toupcamera["Height"], step=1, value=lcfg.toupcamera["SignalUpper"], width=80)
spinner_sigupper.on_change('value', __callback_sigupper)


def __callback_reflower(attr, old, new):
    lcfg.toupcamera["ReferenceLower"] = int(spinner_reflower.value)


spinner_reflower = Spinner(title="Ref Lower", low=0,
                           high=lcfg.toupcamera["Height"], step=1, value=lcfg.toupcamera["ReferenceLower"], width=80)
spinner_reflower.on_change('value', __callback_reflower)


def __callback_refupper(attr, old, new):
    lcfg.toupcamera["ReferenceUpper"] = int(spinner_refupper.value)


spinner_refupper = Spinner(title="Ref Upper", low=0,
                           high=lcfg.toupcamera["Height"], step=1, value=lcfg.toupcamera["ReferenceUpper"], width=80)
spinner_refupper.on_change('value', __callback_refupper)


def __callback_button_toupcam_getsignal():
    expmsg("Retriving signal from remote ToupTek Camera")
    sig, ref = remote_ToupCam_get_signal(
        lcfg.toupcamera["SignalLower"],
        lcfg.toupcamera["SignalUpper"],
        lcfg.toupcamera["ReferenceLower"],
        lcfg.toupcamera["ReferenceUpper"]
    )

    callback_update_toupcam_figure(sig, ref)


button_toupcam_getsignal = Button(label="Retrive Signal")
button_toupcam_getsignal.on_click(__callback_button_toupcam_getsignal)


def __callback_button_toupcam_trig():
    expmsg(remote_ToupCam_trig())


button_toupcam_trig = Button(label="Trig Camera")
button_toupcam_trig.on_click(__callback_button_toupcam_trig)


def __callback_button_open_toupcam():
    expmsg(remote_ToupCam_open())


button_start_toupcam = Button(
    label="Open ToupTek Camera", button_type='success')
button_start_toupcam.on_click(__callback_button_open_toupcam)


def __callback_button_stop_toupcam():
    expmsg(remote_ToupCam_close())


button_stop_toupcam = Button(
    label="Close ToupTek Camera", button_type='warning')
button_stop_toupcam.on_click(__callback_button_stop_toupcam)


def __callback_rbg_toupcam_mode(attr, old, new):
    mode = int(rbg_toupcam_mode.active)
    lcfg.toupcamera["Mode"] = lcfg.camera_modes[mode]
    if mode == 0:  # video
        button_toupcam_trig.visible = False
        expmsg(remote_ToupCam_setvidmode())
    elif mode == 1:  # Software Trigger
        button_toupcam_trig.visible = True
        expmsg(remote_ToupCam_settrigmode())

    lcfg.refresh_config()


rbg_toupcam_mode = RadioButtonGroup(
    labels=['Video', 'SoftwareTrigger'], active=(lcfg.camera_modes.index(lcfg.toupcamera["Mode"])))
rbg_toupcam_mode.on_change('active', __callback_rbg_toupcam_mode)


def __callback_ti_toupcam_exposure_time(attr, old, new):
    try:
        t = int(
            ti_toupcam_exposure_time.value)
        lcfg.toupcamera["ExposureTime"] = t
        lcfg.refresh_config()
        expmsg(remote_ToupCam_setExposureTime(t))
    except Exception as inst:
        print(type(inst), inst.args)


ti_toupcam_exposure_time = TextInput(
    title='Exposure time (each sample, us)', value=str(lcfg.toupcamera["ExposureTime"]))
ti_toupcam_exposure_time.on_change(
    'value', __callback_ti_toupcam_exposure_time)

# endregion
