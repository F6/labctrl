# -*- coding: utf-8 -*-

"""main.py:
This module implements the
Pump-Probe transcient absorption spectroscopy
technic

In such experiment, an Optical Parametric Amplifier(OPA) is deployed
to selectively amplify a beam of supercontinuum white light to generate
an arbitrary wavelength laser pulse, which is called the pump pulse.
Another beam of supercontinuum white light generated with the same
seed pulse, which is weaker but spectrally wider, is called the probe pulse.

The pump pulse and probe pulse is aligned to simultaneously arrive at the
same spot on the sample at zero point. A delay line is put into the probe
pulse path to delay the probe pulse, typically about 10 fs to 10 ns, so the
pump pulse is first absorbed by the sample and excites the sample to its
excited state, then the probe pulse arrives and is absorbed by both ground
state sample molecules and excited state ones. The probe pulse is then
collected and analysed with spectrometer.

A chopper chops the pump pulse in sync with half of the laser repetition
frequency, so half of time the sample is pumped and probed, half of time
the sample is not pumped but probed. Subtracting the later from the previous
results in the optical absorption change (delta O. D.), which is correlated
with change of population in excited states and ground state over time. 

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

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.linear_image_sensors.factory import FactoryLinearImageSensor
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.methods.figure import FactoryFigure1D, FactoryFigure2D

doc.template_variables["app_name"] = "pump_probe"


# META SETTINGS
delay_stage = 'ETHGASN'
spectrometer_sensor = 'FX2000'


class PumpProbePreviewFigure:
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d(
            "Real Time Spectrum", "Linear Array Pixel", "Intensity (counts)", 2048)
        self.delay = factory.generate_fig1d(
            "Time-Domain Intensity Autocorrelation", "Time Delay (ps)", "Intensity (counts)", 40)
        factory = FactoryFigure2D()
        self.twodim = factory.generate_fig2d(
            "PumpProbe Raw Intensity", "Linear Array Pixel", "Time Delay Point #", "Intensity (counts)")


class PumpProbeExpData:
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


class PumpProbeExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.start = Button(label="Start PumpProbe Scan", button_type='success')
        # self.pause = Button(label="Pause Kerr Gate Scan", button_type='warning')
        self.terminate = Button(
            label="Terminate PumpProbe Scan", button_type='warning')
        self.preview = PumpProbePreviewFigure()
        self.data = PumpProbeExpData(lcfg, lstat)
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


pump_probe = PumpProbeExperiment()


@pump_probe.generic.scan_round
@pump_probe.linear_stage.scan_delay
def unit_operation(meta=dict()):
    if pump_probe.flags["TERMINATE"]:
        meta["TERMINATE"] = True
        lstat.expmsg(
            "PumpProbe operation received signal TERMINATE, trying graceful Thread exit")
        return
    lstat.expmsg("Retriving signal from sensor...")
    sig = pump_probe.sensor.get_image()
    lstat.expmsg("Adding latest signal to dataset...")
    stat = lstat.stat[delay_stage]
    pump_probe.data.sig[stat["iDelay"], :] = sig
    pump_probe.data.sigsum[stat["iDelay"], :] += sig
    lstat.doc.add_next_tick_callback(
        partial(pump_probe.preview.signal.callback_update, pump_probe.data.pixels_list, sig))
    lstat.doc.add_next_tick_callback(
        partial(pump_probe.preview.delay.callback_update,
                stat["ScanList"], np.sum(pump_probe.data.sig, axis=1))
    )
    # if this the end of delay scan, call export
    if stat["iDelay"] + 1 == len(stat["ScanList"]):
        lstat.doc.add_next_tick_callback(
            partial(pump_probe.preview.twodim.callback_update, pump_probe.data.sig,
                    pump_probe.data.xmin, pump_probe.data.xmax, pump_probe.data.ymin, pump_probe.data.ymax)
        )
        lstat.expmsg("End of delay scan round, exporting data...")
        pump_probe.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                         "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))


def task():
    lstat.expmsg("Allocating memory for experiment")
    pump_probe.data = PumpProbeExpData(lcfg, lstat)
    lstat.expmsg("Starting experiment")
    meta = dict()
    meta["TERMINATE"] = False
    unit_operation(meta=meta)
    pump_probe.flags["FINISH"] = True
    pump_probe.flags["RUNNING"] = False
    lstat.expmsg("Experiment done")


def __callback_start():
    pump_probe.flags["TERMINATE"] = False
    pump_probe.flags["FINISH"] = False
    pump_probe.flags["RUNNING"] = True
    thread = Thread(target=task)
    thread.start()


pump_probe.start.on_click(__callback_start)


def __callback_terminate():
    lstat.expmsg("Terminating current job")
    pump_probe.flags["TERMINATE"] = True
    pump_probe.flags["FINISH"] = False
    pump_probe.flags["RUNNING"] = False


pump_probe.terminate.on_click(__callback_terminate)


# roots: ["dashboard", "setup", "params", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

# ================ params ================
foo = column(
    pump_probe.linear_stage.scan_mode,
    pump_probe.linear_stage.scan_zero,
    pump_probe.linear_stage.scan_start,
    pump_probe.linear_stage.scan_stop,
    pump_probe.linear_stage.scan_step,
    pump_probe.linear_stage.scan_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)

# ================ manual ================
foo = column(
    pump_probe.linear_stage.test_online,
    pump_probe.linear_stage.manual_position,
    pump_probe.linear_stage.manual_move,
    pump_probe.linear_stage.manual_step,
    pump_probe.linear_stage.manual_step_forward,
    pump_probe.linear_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Linear Stage")
manual_tabs = Tabs(tabs=[manual_tab1], name="manual")
doc.add_root(manual_tabs)

# ================ schedule ================
foo = column(
    pump_probe.generic.filestem,
    pump_probe.generic.scanrounds,
    pump_probe.start,
    pump_probe.terminate
)
schedule_tab1 = Panel(child=foo, title="PumpProbe")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

# ================ reports ================
foo = column(
    pump_probe.preview.signal.fig,
    pump_probe.preview.delay.fig,
    pump_probe.preview.twodim.fig
)
reports_tab1 = Panel(child=foo, title="PumpProbe")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
