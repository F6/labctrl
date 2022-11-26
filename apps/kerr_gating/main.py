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
__version__ = "20221125"


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
from labctrl.components.lockin_and_boxcars.factory import FactoryBoxcar
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.widgets.figure import FactoryFigure

from .experiment_data import KerrGatingExpData

app_name = "kerr_gating"
doc.template_variables["app_name"] = app_name
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name = app_config["DelayLine"]
boxcar_name = app_config["Boxcar"]

# Create a reference to app_config in lstat so that other modules can access it
lstat.stat[app_name] = app_config


class KerrGatingPreviewFigure:
    """
    This class holds references to bundles of figures in reports tab,
      it is not necessary to make it a class, because it will
      only be instantialized once. This class exists only as
      a compression so that the main experiment class is not
      too cumbersome...
    """

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
        figure_bundle_config["Config"] = app_config["DelayScanFigure"]
        self.delay_scan = factory.generate_bundle(figure_bundle_config)


class KerrGatingExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.start = Button(label="Start Kerr Gating Scan",
                            button_type='success')
        self.terminate = Button(
            label="Terminate Kerr Gating Scan", button_type='warning')
        self.preview = KerrGatingPreviewFigure(lcfg, lstat)
        factory = FactoryLinearStage(lcfg, lstat)
        delayline_bundle_config = {
            "BundleType": "Bokeh",
            "Config": lcfg.config["linear_stages"][delay_stage_name]
        }
        self.linear_stage = factory.generate_bundle(delayline_bundle_config)
        factory = FactoryBoxcar(lcfg, lstat)
        boxcar_bundle_config = {
            "BundleType": "Bokeh",
            "Config": lcfg.config["lockin_and_boxcars"][boxcar_name]
        }
        self.boxcar = factory.generate_bundle(boxcar_bundle_config)
        factory = FactoryGenericMethods()
        self.generic = factory.generate(lcfg, lstat)
        self.data = KerrGatingExpData(lcfg, lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

        # region start
        @self.generic.scan_round
        @self.linear_stage.scan_range
        def unit_operation(meta=dict()):
            if self.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg(
                    "KerrGating operation received signal TERMINATE, trying graceful Thread exit")
                return
            lstat.expmsg("[KerrGatingUnit] Retriving signal from sensor...")
            data = self.boxcar.get_boxcar_data(1024)
            lstat.expmsg("[KerrGatingUnit] Adding latest signal to dataset...")
            ds = np.size(data)

            # [TODO] [ALERT]: Temporary: we are using ziUHF's own background subtraction to
            #   do the shot-to-shot subtraction here, so no need to subtract background.
            #   This is temporary, when we switch back to our own boxcar controller, the
            #   subtraction is done locally (This can be done in the server side, but it is
            #   more flexible to do it at client side.)
            # sig = data[:ds//2]
            sig = data
            bg = np.zeros(ds)
            # delta = sig - bg
            # delta = np.log10(sig/bg)
            delta = sig
            # [ENDTODO]

            sig_average = np.average(sig)
            bg_average = np.average(bg)
            delta_average = np.average(delta)
            delta_stddev = np.std(delta)
            stat = lstat.stat[delay_stage_name]

            self.data.signal[stat["iDelay"]] = sig_average
            self.data.signal_sum[stat["iDelay"]] += sig_average
            self.preview.signal.update(np.arange(np.size(sig)), sig, lstat)

            self.data.background[stat["iDelay"]] = bg_average
            self.data.background_sum[stat["iDelay"]] += bg_average
            self.preview.background.update(np.arange(np.size(bg)), bg, lstat)

            self.data.delta[stat["iDelay"]] = delta_average
            self.data.delta_sum[stat["iDelay"]] += delta_average
            self.data.delta_stddev[stat["iDelay"]] = delta_stddev
            self.preview.delta.update(np.arange(np.size(delta)), delta, lstat)
            self.preview.delay_scan.update(self.data.delays, self.data.delta, lstat)
            # If whiskers are used, add these two param as upper and lower to .update
            # KerrGating.data.delta + KerrGating.data.delta_stddev,
            # KerrGating.data.delta - KerrGating.data.delta_stddev

            # if this the end of delay scan, call export
            if stat["iDelay"] + 1 == len(stat["ScanList"]):
                lstat.expmsg("End of delay scan round, exporting data...")
                self.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                                "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))


        def task():
            lstat.expmsg("Allocating memory for experiment")
            self.data = KerrGatingExpData(lcfg, lstat)
            lstat.expmsg("Starting experiment")
            meta = dict()
            meta["TERMINATE"] = False
            unit_operation(meta=meta)
            self.flags["FINISH"] = True
            self.flags["RUNNING"] = False
            lstat.expmsg("Experiment done")


        def __callback_start():
            self.flags["TERMINATE"] = False
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = True
            # self.boxcar.switch_working_mode("Boxcar")
            thread = Thread(target=task)
            thread.start()


        self.start.on_click(__callback_start)

        # endregion start

        # region terminate
        def __callback_terminate():
            lstat.expmsg("Terminating current job")
            self.flags["TERMINATE"] = True
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = False

        self.terminate.on_click(__callback_terminate)
        # endregion terminate


kerr = KerrGatingExperiment(lcfg, lstat)


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
foo = column(
    kerr.boxcar.host,
    kerr.boxcar.port,
)
setup_tab2 = Panel(child=foo, title="Boxcar")
setup_tabs = Tabs(tabs=[setup_tab1, setup_tab2], name="setup")
doc.add_root(setup_tabs)
# endregion setup

# ================ params ================
foo = column(
    kerr.linear_stage.scan_mode,
    kerr.linear_stage.working_unit,
    kerr.linear_stage.range_scan_start,
    kerr.linear_stage.range_scan_stop,
    kerr.linear_stage.range_scan_step,
    kerr.linear_stage.external_scan_list_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
foo = column(
    Div(text="Boxcar Working Unit:"),
    kerr.boxcar.working_unit,
    kerr.boxcar.delay_background_sampling,
    kerr.boxcar.delay_integrate,
    kerr.boxcar.delay_hold,
    kerr.boxcar.delay_signal_sampling,
    kerr.boxcar.delay_reset,
    kerr.boxcar.submit_config,
    Div(text="Boxcar Working Mode:"),
    kerr.boxcar.working_mode,
    kerr.boxcar.set_working_mode,
)
foo2 = column(
    kerr.boxcar.start_PWA,
    kerr.boxcar.stop_PWA,
    kerr.boxcar.manual_get_PWA_data,
    kerr.boxcar.PWA_figure.figure,
)
bar = row(foo, foo2)
param_tab2 = Panel(child=bar, title="Boxcar Controller")
param_tabs = Tabs(tabs=[param_tab1, param_tab2], name="param")
doc.add_root(param_tabs)

# ================ manual ================
foo = column(
    kerr.linear_stage.test_online,
    Div(text="Manual Operation Unit:"),
    kerr.linear_stage.manual_unit,
    kerr.linear_stage.manual_position,
    kerr.linear_stage.manual_move,
    kerr.linear_stage.manual_step,
    kerr.linear_stage.manual_step_forward,
    kerr.linear_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Linear Stage")
foo = column(
    kerr.boxcar.test_online,
    kerr.boxcar.manual_get_boxcar_data,
)
foo2 = column(
    kerr.boxcar.boxcar_preview.figure,
)
bar = row(foo, foo2)
manual_tab2 = Panel(child=bar, title="Boxcar Controller")
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
