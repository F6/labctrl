# -*- coding: utf-8 -*-

"""main.py:
This module implements the
Kerr Gating Time-resolved Photoluminescence Spectroscopy
technic

The balanced Kerr gate spectroscopy can measure the ultrafast dynamics
of light emission from molecules with very weak fluorescence or phosphorescence,
for example the fluorescence from 2-dimensional materials, ACQ systems
or single molecule systems.

In such experiments, an ultrafast laser pulse excites the sample to
higher electronic excited states, then the fluorescence and
phosphorescence from the decay of the electronic excited
states are collected with reflective objectives, then sent into a 
Kerr gate and detected with balanced detector. A chopper chops the
excitation pulse train into 50% duty cycle, the sync TTL of the chopper
and the balanced signal are sent into a boxcar averager to recover 
the lifetime signal by shot-to-shot subtraction of backgrounds.
Another synchronized beam of ultrafast laser pulse and a delay 
line is used to set the opening time window of the Kerr gate. 

Reflective objectives are prefered over regular microscope objectives
because this type of objective introduces minimum distortion of
wavepacket-front in the geometric space, which will significantly decrease 
the Kerr gating efficiency and make it hard to detect the already weak
signal.

For single wavelength TRPL measurements, a notch filter is inserted
before the detector. For multi wavelength measurements, typically an array
of notch filter is used. Note that the instrument introduces dispersion
to the original signal, so dispersion correction from standard samples
must be applied for multi-wavelength time zeros.

the Zurich Instruments UHF is used as the boxcar integrator. When UHF
is not available we use our self made one
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220624"


import time
import numpy as np
import requests
import json
import base64
from functools import partial
from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg, LabConfig
from labctrl.labstat import lstat, LabStat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.lockin_and_boxcars.factory import FactoryBoxcarController
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.widgets.figure import FactoryFigure

app_name = "kerr_gating"
doc.template_variables["app_name"] = app_name
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name = app_config["DelayLine"]
boxcar_name = app_config["Boxcar"]


class KerrGatingPreviewFigure:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        factory = FactoryFigure(lcfg, lstat)
        figure_bundle_config = dict()
        figure_bundle_config["BundleType"] = "Bokeh"
        figure_bundle_config["Config"] = app_config["SignalFigure"]
        self.signal = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config["BundleType"] = "Bokeh"
        figure_bundle_config["Config"] = app_config["BackgroundFigure"]
        self.background = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config["BundleType"] = "Bokeh"
        figure_bundle_config["Config"] = app_config["DeltaFigure"]
        self.delta = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config["BundleType"] = "Bokeh"
        figure_bundle_config["Config"] = app_config["PeriodicWaveformAnalyzerFigure"]
        self.pwa = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config["BundleType"] = "Bokeh"
        figure_bundle_config["Config"] = app_config["DelayScanFigure"]
        self.delay_scan = factory.generate_bundle(figure_bundle_config)


class KerrGatingExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg
        self.delays = lstat.stat[delay_stage_name]["ScanList"]
        self.ymin = np.min(self.delays)
        self.ymax = np.max(self.delays)
        self.signal = np.zeros(len(self.delays), dtype=np.float64)
        self.signal_sum = np.zeros(len(self.delays), dtype=np.float64)
        self.background = np.zeros(len(self.delays), dtype=np.float64)
        self.background_sum = np.zeros(len(self.delays), dtype=np.float64)
        self.delta = np.zeros(len(self.delays), dtype=np.float64)  # fig delay
        self.delta_stddev = np.zeros(
            len(self.delays), dtype=np.float64)  # fig delay
        self.delta_sum = np.zeros(len(self.delays), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        tosave = self.signal
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.signal_sum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Background.csv"
        tosave = self.background
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Background.csv"
        tosave = self.background_sum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delta.csv"
        tosave = self.delta
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Standard-Deviation-Delta.csv"
        tosave = self.delta
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Delta.csv"
        tosave = self.delta_sum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.delays)
        np.savetxt(filename, tosave, delimiter=',')


class KerrGatingExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.start = Button(label="Start Kerr Gating Scan",
                            button_type='success')
        # self.pause = Button(label="Pause Kerr Gating Scan", button_type='warning')
        self.terminate = Button(
            label="Terminate Kerr Gating Scan", button_type='warning')
        self.start_PWA = Button(
            label="Start Boxcar PWA", button_type='success')
        self.terminate_PWA = Button(
            label="Terminate Boxcar PWA", button_type='warning')
        self.preview = KerrGatingPreviewFigure(lcfg, lstat)
        factory = FactoryLinearStage(lcfg, lstat)
        delayline_bundle_config = dict()
        delayline_bundle_config["BundleType"] = "Bokeh"
        delayline_bundle_config["Config"] = lcfg.config["linear_stages"][delay_stage_name]
        self.linear_stage = factory.generate_bundle(delayline_bundle_config)
        factory = FactoryBoxcarController()
        self.boxcar = factory.generate_bundle(boxcar_name, lcfg, lstat)
        factory = FactoryGenericMethods()
        self.generic = factory.generate(lcfg, lstat)
        self.data = KerrGatingExpData(lcfg, lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }
        self.PWA_flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }


kerr = KerrGatingExperiment(lcfg, lstat)


@kerr.generic.scan_round
@kerr.linear_stage.scan_range
def unit_operation(meta=dict()):
    if kerr.flags["TERMINATE"]:
        meta["TERMINATE"] = True
        lstat.expmsg(
            "KerrGating operation received signal TERMINATE, trying graceful Thread exit")
        return
    lstat.expmsg("[KerrGatingUnit] Retriving signal from sensor...")
    data = kerr.boxcar.get_boxcar_data()
    lstat.expmsg("[KerrGatingUnit] Adding latest signal to dataset...")
    ds = np.size(data)

    # [TODO] [ALERT]: Temporary: we are using ziUHF's own background subtraction to 
    #   do the shot-to-shot subtraction here, so no need to subtract background.
    #   This is temporary, when we switch back to our own boxcar controller, the
    #   subtraction is done locally (This can be done in the server side, but it is
    #   more flexible to do it at client side.)
    # sig = data[:ds//2]
    sig = data
    bg = data[ds//2:]
    # delta = sig - bg
    # delta = np.log10(sig/bg)
    delta = sig
    # [ENDTODO]

    sig_average = np.average(sig)
    bg_average = np.average(bg)
    delta_average = np.average(delta)
    delta_stddev = np.std(delta)
    stat = lstat.stat[delay_stage_name]

    kerr.data.signal[stat["iDelay"]] = sig_average
    kerr.data.signal_sum[stat["iDelay"]] += sig_average
    kerr.preview.signal.update(np.arange(np.size(sig)), sig, lstat)

    kerr.data.background[stat["iDelay"]] = bg_average
    kerr.data.background_sum[stat["iDelay"]] += bg_average
    kerr.preview.background.update(np.arange(np.size(bg)), bg, lstat)

    kerr.data.delta[stat["iDelay"]] = delta_average
    kerr.data.delta_sum[stat["iDelay"]] += delta_average
    kerr.data.delta_stddev[stat["iDelay"]] = delta_stddev
    kerr.preview.delta.update(np.arange(np.size(delta)), delta, lstat)
    kerr.preview.delay_scan.update(kerr.data.delays, kerr.data.delta, lstat)
    # If whiskers are used, add these two param as upper and lower to .update
    # KerrGating.data.delta + KerrGating.data.delta_stddev,
    # KerrGating.data.delta - KerrGating.data.delta_stddev

    # if this the end of delay scan, call export
    if stat["iDelay"] + 1 == len(stat["ScanList"]):
        lstat.expmsg("End of delay scan round, exporting data...")
        kerr.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                               "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))


def task():
    lstat.expmsg("Allocating memory for experiment")
    kerr.data = KerrGatingExpData(lcfg, lstat)
    lstat.expmsg("Starting experiment")
    meta = dict()
    meta["TERMINATE"] = False
    unit_operation(meta=meta)
    kerr.flags["FINISH"] = True
    kerr.flags["RUNNING"] = False
    lstat.expmsg("Experiment done")


def __callback_start():
    kerr.flags["TERMINATE"] = False
    kerr.flags["FINISH"] = False
    kerr.flags["RUNNING"] = True
    kerr.boxcar.set_working_mode("Boxcar")
    thread = Thread(target=task)
    thread.start()


kerr.start.on_click(__callback_start)


def __callback_terminate():
    lstat.expmsg("Terminating current job")
    kerr.flags["TERMINATE"] = True
    kerr.flags["FINISH"] = False
    kerr.flags["RUNNING"] = False


kerr.terminate.on_click(__callback_terminate)


def PWA_task():
    lstat.expmsg("Starting PWA...")
    kerr.PWA_flags["TERMINATE"] = False
    while not kerr.PWA_flags["TERMINATE"]:
        data = kerr.boxcar.get_PWA_data()
        ds = np.size(data)
        kerr.preview.pwa.update(np.linspace(0, ds//2, ds), data, lstat)
    lstat.expmsg("PWA Terminated.")
    kerr.PWA_flags["RUNNING"] = False


def __callback_PWA_start():
    kerr.PWA_flags["TERMINATE"] = False
    kerr.PWA_flags["FINISH"] = False
    kerr.PWA_flags["RUNNING"] = True
    kerr.boxcar.set_working_mode("PWA")
    thread = Thread(target=PWA_task)
    thread.start()


kerr.start_PWA.on_click(__callback_PWA_start)


def __callback_PWA_terminate():
    lstat.expmsg("Terminating current PWA job")
    kerr.PWA_flags["TERMINATE"] = True
    kerr.PWA_flags["FINISH"] = False
    kerr.PWA_flags["RUNNING"] = False
    kerr.boxcar.set_working_mode("Boxcar")


kerr.terminate_PWA.on_click(__callback_PWA_terminate)


# roots: ["dashboard", "setup", "param", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

# region messages
# ================ Experiment Message ================
doc.add_root(lstat.pre_exp_msg)
# endregion messages


# region setup
# ================ setup ================
foo = column(
    kerr.linear_stage.host,
    kerr.linear_stage.port,
    kerr.linear_stage.multiples,
    kerr.linear_stage.working_direction,
    Div(text="Position and Limitation Unit:"),
    kerr.linear_stage.position_unit,
    kerr.linear_stage.zero_point_absolute_position,
    kerr.linear_stage.soft_limit_min,
    kerr.linear_stage.soft_limit_max,
    kerr.linear_stage.driving_speed,
    kerr.linear_stage.driving_speed_unit,
    kerr.linear_stage.driving_acceleration,
    kerr.linear_stage.driving_acceleration_unit,
)
setup_tab1 = Panel(child=foo, title="Delay Line")
setup_tabs = Tabs(tabs=[setup_tab1], name="setup")
doc.add_root(setup_tabs)
# endregion setup

# ================ params ================
foo = column(
    kerr.linear_stage.scan_mode,
    kerr.linear_stage.zero_point_absolute_position,
    kerr.linear_stage.range_scan_start,
    kerr.linear_stage.range_scan_stop,
    kerr.linear_stage.range_scan_step,
    kerr.linear_stage.external_scan_list_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
foo = column(
    kerr.boxcar.delay_background_sampling,
    kerr.boxcar.delay_integrate,
    kerr.boxcar.delay_hold,
    kerr.boxcar.delay_signal_sampling,
    kerr.boxcar.delay_reset,
    kerr.boxcar.submit_config,
    kerr.boxcar.working_mode
)
foo2 = column(
    kerr.start_PWA,
    kerr.terminate_PWA,
    kerr.preview.pwa.figure,
)
bar = row(foo, foo2)
param_tab2 = Panel(child=bar, title="Boxcar Controller")
param_tabs = Tabs(tabs=[param_tab1, param_tab2], name="param")
doc.add_root(param_tabs)

# ================ manual ================
foo = column(
    kerr.linear_stage.test_online,
    kerr.linear_stage.manual_position,
    kerr.linear_stage.manual_move,
    kerr.linear_stage.manual_step,
    kerr.linear_stage.manual_step_forward,
    kerr.linear_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Linear Stage")
foo = column(
    kerr.boxcar.test_online,
)
manual_tab2 = Panel(child=foo, title="Boxcar Controller")
manual_tabs = Tabs(tabs=[manual_tab1, manual_tab2], name="manual")
doc.add_root(manual_tabs)

# ================ schedule ================
foo = column(
    kerr.generic.filestem,
    kerr.generic.scanrounds,
    kerr.start,
    kerr.terminate
)
schedule_tab1 = Panel(child=foo, title="KerrGating")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

# ================ reports ================
foo = column(
    kerr.preview.delay_scan.figure,
    kerr.preview.delta.figure,
    kerr.preview.signal.figure,
    kerr.preview.background.figure,
)
reports_tab1 = Panel(child=foo, title="KerrGating")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
