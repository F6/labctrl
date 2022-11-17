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
from psutil import pid_exists

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.linear_image_sensors.factory import FactoryLinearImageSensor
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.widgets.figure import FactoryFigure1D, FactoryFigure2D

doc.template_variables["app_name"] = "frog"


# META SETTINGS
delay_stage = 'USB1020'
spectrometer_sensor = 'FX2000'


class FROGPreviewFigure:
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d(
            "Real Time Spectrum", "Wavelength (nm)", "Intensity (counts)", 2048)
        self.delay = factory.generate_fig1d(
            "Time-Domain Intensity Autocorrelation", "Time Delay (ps)", "Intensity (counts)", 40)
        factory = FactoryFigure2D()
        self.twodim = factory.generate_fig2d(
            "FROG Raw Intensity", "Wavelength", "Time Delay", "Intensity (counts)")


class FROGExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg, lstat) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg
        self.delays = lstat.stat[delay_stage]["ScanList"]
        self.npixels = lcfg.config["linear_image_sensors"][spectrometer_sensor]["NumberOfPixels"]
        self.pixels_list = np.arange(self.npixels)
        self.xmin = np.min(self.pixels_list)
        self.xmax = np.max(self.pixels_list)
        self.ymin = np.min(self.delays)
        self.ymax = np.max(self.delays)
        self.sig = np.zeros((len(self.delays), self.npixels), dtype=np.float64)
        self.sigsum = np.zeros(
            (len(self.delays), self.npixels), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        tosave = self.sig
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.sigsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.delays)
        np.savetxt(filename, tosave, delimiter=',')


class FROGExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.start = Button(label="Start FROG Scan", button_type='success')
        # self.pause = Button(label="Pause Kerr Gate Scan", button_type='warning')
        self.terminate = Button(
            label="Terminate FROG Scan", button_type='warning')
        self.preview = FROGPreviewFigure()
        self.data = FROGExpData(lcfg, lstat)
        factory = FactoryLinearStage()
        self.linear_stage = factory.generate_bundle(delay_stage, lcfg, lstat)
        factory = FactoryLinearImageSensor()
        self.sensor = factory.generate_bundle(spectrometer_sensor, lcfg, lstat)
        factory = FactoryGenericMethods()
        self.generic = factory.generate(lcfg, lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }


frog = FROGExperiment()


@frog.generic.scan_round
@frog.linear_stage.scan_delay
def unit_operation(meta=dict()):
    if frog.flags["TERMINATE"]:
        meta["TERMINATE"] = True
        lstat.expmsg(
            "FROG operation received signal TERMINATE, trying graceful Thread exit")
        return
    lstat.expmsg("Retriving signal from sensor...")
    sig = frog.sensor.get_image()
    lstat.expmsg("Adding latest signal to dataset...")
    stat = lstat.stat[delay_stage]
    frog.data.sig[stat["iDelay"], :] = sig
    frog.data.sigsum[stat["iDelay"], :] += sig
    lstat.doc.add_next_tick_callback(
        partial(frog.preview.signal.callback_update, frog.data.pixels_list, sig))
    lstat.doc.add_next_tick_callback(
        partial(frog.preview.delay.callback_update,
                stat["ScanList"], np.sum(frog.data.sig, axis=1))
    )
    # if this the end of delay scan, call export
    if stat["iDelay"] + 1 == len(stat["ScanList"]):
        lstat.doc.add_next_tick_callback(
            partial(frog.preview.twodim.callback_update, frog.data.sig,
                    frog.data.xmin, frog.data.xmax, frog.data.ymin, frog.data.ymax)
        )
        lstat.expmsg("End of delay scan round, exporting data...")
        frog.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                         "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))


def task():
    lstat.expmsg("Allocating memory for experiment")
    frog.data = FROGExpData(lcfg, lstat)
    lstat.expmsg("Starting experiment")
    meta = dict()
    meta["TERMINATE"] = False
    unit_operation(meta=meta)
    frog.flags["FINISH"] = True
    frog.flags["RUNNING"] = False
    lstat.expmsg("Experiment done")


def __callback_start():
    frog.flags["TERMINATE"] = False
    frog.flags["FINISH"] = False
    frog.flags["RUNNING"] = True
    thread = Thread(target=task)
    thread.start()


frog.start.on_click(__callback_start)


def __callback_terminate():
    lstat.expmsg("Terminating current job")
    frog.flags["TERMINATE"] = True
    frog.flags["FINISH"] = False
    frog.flags["RUNNING"] = False


frog.terminate.on_click(__callback_terminate)


# roots: ["dashboard", "setup", "params", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

# ================ params ================
foo = column(
    frog.linear_stage.scan_mode,
    frog.linear_stage.scan_zero,
    frog.linear_stage.scan_start,
    frog.linear_stage.scan_stop,
    frog.linear_stage.scan_step,
    frog.linear_stage.scan_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)

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
    frog.preview.signal.fig,
    frog.preview.delay.fig,
    frog.preview.twodim.fig
)
reports_tab1 = Panel(child=foo, title="FROG")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
