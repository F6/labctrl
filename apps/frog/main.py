# -*- coding: utf-8 -*-

"""main.py:
This module implements the
Frequency Resolved Optical Gating
technic

The purpose of a FROG is mainly to determine the pulse shape of a ultrafast
pulsed laser, including it's field strength over time and other properties.
FROG is commonly used as a quick and simple monitoring device for 
adjusting compression in chirped pulse amplifiers. It can also be used to
monitor chirps and distortions introduced by OPAs, NOPAs, OPCPAs, and other 
nonlinear optical devices.

A typical SHG-FROG is set up like a Michelson inteferometer, a pulse is split
by a 50/50 ultralow GDD beam splitter, then re-aligned and focused to cross
the same point in a BBO crystal or other nonlinear crystals. The angle of the
two beams are kept very small, and the BBO is cut and rotated to the specific
angle where 2 SHG spots from the two beams have nearly identical intensity.
If the 2 pulses arrive at the same time, then another SHG beam is generated
between the 2 original beams, according to phase matching conditions. By delaying
one pulse slightly, the SHG efficiency changes drastically because the two
pulses are not overlapping in time. So if we detect the strength and spectrum
of the autocorrelation beam, it is possible to do reverse calculations to
determine the pulse shape.

To measure very short pulses, a very thin BBO or other crystal is needed.
Around 100 um is good for pulses longer than 50 fs, if pulse is shorter, consider
use 50 um or 10 um BBOs. The delay stage also needs to be precise to sub
micrometer, so most cheap linear servos will not work. For a cheap substitution,
stepper motor + screws are generally more stable when abused (pros are that they
can achieve good incremental relative accuracy if correctly driven, the resolution
can easily get to below 5 fs, and that they are super cheap, cons are that they 
can only scan in one direction, and the zero point drifts terribly because of 
mechanical assembly clearance). Ideally, a voice coil linear stage is best for
autocorrelation scans because they are extremely fast and precise. Paired wedges 
can also be used as cheap substitution if non of the above is available, pros are
that it can get to attosecond resolution with cheap setup, cons are that it
introduces additional chirp and distortion to the pulse.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220525"


import time
import numpy as np

from functools import partial
from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg, LabConfig
from labctrl.labstat import lstat, LabStat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.linear_image_sensors.factory import FactoryLinearImageSensor
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.widgets.figure import FactoryFigure

from .frog_data import FROGExpData

app_name = "frog"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["apps"][app_name]
delay_stage_name: str = app_config["DelayStage"]
linear_detector_name: str = app_config["LinearDetector"]
# Create a reference to app_config in lstat so that other modules can access it
lstat.stat[app_name] = app_config


class FROGPreviewFigure:
    def __init__(self) -> None:
        factory = FactoryFigure(lcfg, lstat)
        figure_bundle_config = {"BundleType": "Bokeh",
                                "Config": app_config["SignalFigure"]}
        self.signal = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config = {"BundleType": "Bokeh",
                                "Config": app_config["IntensityCorrelationFigure"]}
        self.delay = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config = {"BundleType": "Bokeh",
                                "Config": app_config["FrogFigure"]}
        self.frog = factory.generate_bundle(figure_bundle_config)



class FROGExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self, lcfg:LabConfig, lstat:LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat
        config = lcfg.config
        self.start = Button(label="Start FROG Scan", button_type='success')
        # self.pause = Button(label="Pause Kerr Gate Scan", button_type='warning')
        self.terminate = Button(
            label="Terminate FROG Scan", button_type='warning')
        self.preview = FROGPreviewFigure()
        factory = FactoryLinearStage(self.lcfg, self.lstat)
        frog_stage_bundle_config = {
            "BundleType": "Bokeh",
            "Config": config["linear_stages"][delay_stage_name],
        }
        self.linear_stage = factory.generate_bundle(
            frog_stage_bundle_config)
        factory = FactoryLinearImageSensor()
        self.sensor = factory.generate_bundle(
            linear_detector_name, self.lcfg, self.lstat)
        self.data = FROGExpData(app_config, self.lcfg, self.lstat)
        factory = FactoryGenericMethods()
        self.generic = factory.generate(self.lcfg, self.lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }
    
    
        @self.generic.scan_round
        @self.linear_stage.scan_range
        def unit_operation(meta=dict()):
            if self.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg(
                    "FROG operation received signal TERMINATE, trying graceful Thread exit")
                return
            self.lstat.expmsg("Retriving signal from sensor...")
            sig = self.sensor.get_image()
            lstat.expmsg("Adding latest signal to dataset...")
            delay_stat = self.lstat.stat[delay_stage_name]
            self.data.sig[delay_stat["iDelay"], :] = sig
            self.data.sigsum[delay_stat["iDelay"], :] += sig
            self.preview.signal.update(self.data.pixels_list, sig, lstat)
            self.preview.delay.update(
                delay_stat["ScanList"], np.sum(self.data.sig, axis=1), lstat)

            # if this the end of delay scan, call export
            if delay_stat["iDelay"] + 1 == len(delay_stat["ScanList"]):
                self.preview.frog.update(
                    self.data.sig,
                    self.data.xmin,
                    self.data.xmax,
                    self.data.ymin,
                    self.data.ymax,
                    lstat
                )
                self.lstat.expmsg("End of delay scan round, exporting data...")
                self.data.export("scandata/" + self.lcfg.config["basic"]["FileStem"] +
                                "-Round{rd}".format(rd=self.lstat.stat["basic"]["iRound"]))


        def task():
            self.lstat.expmsg("Allocating memory for experiment")
            self.data = FROGExpData(app_config, self.lcfg, self.lstat)
            self.lstat.expmsg("Starting experiment")
            meta = dict()
            meta["TERMINATE"] = False
            unit_operation(meta=meta)
            self.flags["FINISH"] = True
            self.flags["RUNNING"] = False
            self.lstat.expmsg("Experiment done")


        def __callback_start():
            self.flags["TERMINATE"] = False
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = True
            thread = Thread(target=task)
            thread.start()


        self.start.on_click(__callback_start)


        def __callback_terminate():
            self.lstat.expmsg("Terminating current job")
            self.flags["TERMINATE"] = True
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = False


        self.terminate.on_click(__callback_terminate)


frog = FROGExperiment(lcfg, lstat)




# roots: ["dashboard", "setup", "params", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

# ================ params ================
foo = column(
    Div(text="<b>Pump Probe Delay Line:</b>"),
    frog.linear_stage.scan_mode,
    frog.linear_stage.working_unit,
    frog.linear_stage.range_scan_start,
    frog.linear_stage.range_scan_stop,
    frog.linear_stage.range_scan_step,
    frog.linear_stage.external_scan_list_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)

# region messages
# ================ Experiment Message ================
doc.add_root(lstat.pre_exp_msg)
# endregion messages

# ================ manual ================
foo = column(
    frog.linear_stage.test_online,
    frog.linear_stage.manual_position,
    frog.linear_stage.manual_move,
    frog.linear_stage.manual_step,
    frog.linear_stage.manual_step_forward,
    frog.linear_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Linear Stage")
manual_tabs = Tabs(tabs=[manual_tab1], name="manual")
doc.add_root(manual_tabs)

# ================ schedule ================
foo = column(
    frog.generic.filestem,
    frog.generic.scanrounds,
    frog.start,
    frog.terminate
)
schedule_tab1 = Panel(child=foo, title="FROG")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

# ================ reports ================
foo = column(
    frog.preview.signal.figure,
    frog.preview.delay.figure,
    frog.preview.frog.figure
)
reports_tab1 = Panel(child=foo, title="FROG")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
