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

from functools import partial
from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.lockin_and_boxcars.factory import FactoryBoxcarController
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.methods.figure import FactoryFigure1D, FactoryFigure1DWithWhiskers

doc.template_variables["app_name"] = "kerr_gating"


# META SETTINGS
delay_stage = 'ETHGASN'
boxcar_name = 'generic_boxcar'
# boxcar = 'ziUHF'


class KerrGatingPreviewFigure:
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d(
            "Boxcar Signal", "Data #", "Intensity (V)", 256)
        self.background = factory.generate_fig1d(
            "Boxcar Background", "Data #", "Intensity (V)", 256)
        self.delta = factory.generate_fig1d(
            "Shot-to-shot Boxcar Delta", "Data #", "Intensity (V)", 256)
        self.PWA = factory.generate_fig1d(
            "PWA", "Time/us", "Intensity (V)", 1024)
        factory = FactoryFigure1DWithWhiskers()
        self.delay = factory.generate_fig1d(
            "Delay Scan", "Time Delay (ps)", "Intensity (V)", 40)
        # factory = FactoryFigure2D()
        # self.twodim = factory.generate_fig2d(
        #     "KerrGating Raw Intensity", "Linear Array Pixel", "Time Delay Point #", "Intensity (counts)")


class KerrGatingExpData:
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

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.start = Button(label="Start Kerr Gating Scan",
                            button_type='success')
        # self.pause = Button(label="Pause Kerr Gating Scan", button_type='warning')
        self.terminate = Button(
            label="Terminate Kerr Gating Scan", button_type='warning')
        self.start_PWA = Button(
            label="Start Boxcar PWA", button_type='success')
        self.terminate_PWA = Button(
            label="Terminate Boxcar PWA", button_type='warning')
        self.preview = KerrGatingPreviewFigure()
        self.data = KerrGatingExpData(lcfg, lstat)
        factory = FactoryLinearStage()
        self.linear_stage = factory.generate_bundle(delay_stage, lcfg, lstat)
        factory = FactoryBoxcarController()
        self.boxcar = factory.generate_bundle(boxcar_name, lcfg, lstat)
        factory = FactoryGenericMethods()
        self.generic = factory.generate(lcfg, lstat)
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


KerrGating = KerrGatingExperiment()


@KerrGating.generic.scan_round
@KerrGating.linear_stage.scan_delay
def unit_operation(meta=dict()):
    if KerrGating.flags["TERMINATE"]:
        meta["TERMINATE"] = True
        lstat.expmsg(
            "KerrGating operation received signal TERMINATE, trying graceful Thread exit")
        return
    lstat.expmsg("Retriving signal from sensor...")
    data = KerrGating.boxcar.get_boxcar_data()
    lstat.expmsg("Adding latest signal to dataset...")
    ds = np.size(data)
    sig = data[:ds//2]
    bg = data[ds//2:]
    delta = sig - bg
    sig_average = np.average(sig)
    bg_average = np.average(bg)
    delta_average = np.average(delta)
    delta_stddev = np.std(delta)
    stat = lstat.stat[delay_stage]

    KerrGating.data.signal[stat["iDelay"]] = sig_average
    KerrGating.data.signal_sum[stat["iDelay"]] += sig_average
    lstat.doc.add_next_tick_callback(
        partial(KerrGating.preview.signal.callback_update, np.arange(ds//2), sig))

    KerrGating.data.background[stat["iDelay"]] = bg_average
    KerrGating.data.background_sum[stat["iDelay"]] += bg_average
    lstat.doc.add_next_tick_callback(
        partial(KerrGating.preview.background.callback_update, np.arange(ds//2), bg))

    KerrGating.data.delta[stat["iDelay"]] = delta_average
    KerrGating.data.delta_sum[stat["iDelay"]] += delta_average
    KerrGating.data.delta_stddev[stat["iDelay"]] = delta_stddev
    lstat.doc.add_next_tick_callback(
        partial(KerrGating.preview.delta.callback_update, np.arange(ds//2), delta))
    lstat.doc.add_next_tick_callback(
        partial(KerrGating.preview.delay.callback_update,
                KerrGating.data.delays, KerrGating.data.delta, KerrGating.data.delays,
                KerrGating.data.delta + KerrGating.data.delta_stddev,
                KerrGating.data.delta - KerrGating.data.delta_stddev)
    )

    # if this the end of delay scan, call export
    if stat["iDelay"] + 1 == len(stat["ScanList"]):
        lstat.expmsg("End of delay scan round, exporting data...")
        KerrGating.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                               "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))


def task():
    lstat.expmsg("Allocating memory for experiment")
    KerrGating.data = KerrGatingExpData(lcfg, lstat)
    lstat.expmsg("Starting experiment")
    meta = dict()
    meta["TERMINATE"] = False
    unit_operation(meta=meta)
    KerrGating.flags["FINISH"] = True
    KerrGating.flags["RUNNING"] = False
    lstat.expmsg("Experiment done")


def __callback_start():
    KerrGating.flags["TERMINATE"] = False
    KerrGating.flags["FINISH"] = False
    KerrGating.flags["RUNNING"] = True
    KerrGating.boxcar.set_working_mode("Boxcar")
    thread = Thread(target=task)
    thread.start()


KerrGating.start.on_click(__callback_start)


def __callback_terminate():
    lstat.expmsg("Terminating current job")
    KerrGating.flags["TERMINATE"] = True
    KerrGating.flags["FINISH"] = False
    KerrGating.flags["RUNNING"] = False


KerrGating.terminate.on_click(__callback_terminate)


def PWA_task():
    lstat.expmsg("Starting PWA...")
    KerrGating.PWA_flags["TERMINATE"] = False
    while not KerrGating.PWA_flags["TERMINATE"]:
        data = KerrGating.boxcar.get_PWA_data()
        ds = np.size(data)
        doc.add_next_tick_callback(partial(KerrGating.preview.PWA.callback_update, np.linspace(0, ds//2, ds), data))
    lstat.expmsg("PWA Terminated.")
    KerrGating.PWA_flags["RUNNING"] = False

def __callback_PWA_start():
    KerrGating.PWA_flags["TERMINATE"] = False
    KerrGating.PWA_flags["FINISH"] = False
    KerrGating.PWA_flags["RUNNING"] = True
    KerrGating.boxcar.set_working_mode("PWA")
    thread = Thread(target=PWA_task)
    thread.start()

KerrGating.start_PWA.on_click(__callback_PWA_start)

def __callback_PWA_terminate():
    lstat.expmsg("Terminating current PWA job")
    KerrGating.PWA_flags["TERMINATE"] = True
    KerrGating.PWA_flags["FINISH"] = False
    KerrGating.PWA_flags["RUNNING"] = False
    KerrGating.boxcar.set_working_mode("Boxcar")

KerrGating.terminate_PWA.on_click(__callback_PWA_terminate)


# roots: ["dashboard", "setup", "param", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

# ================ params ================
foo = column(
    KerrGating.linear_stage.scan_mode,
    KerrGating.linear_stage.scan_zero,
    KerrGating.linear_stage.scan_start,
    KerrGating.linear_stage.scan_stop,
    KerrGating.linear_stage.scan_step,
    KerrGating.linear_stage.scan_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
foo = column(
    KerrGating.boxcar.delay_background_sampling,
    KerrGating.boxcar.delay_integrate,
    KerrGating.boxcar.delay_hold,
    KerrGating.boxcar.delay_signal_sampling,
    KerrGating.boxcar.delay_reset,
    KerrGating.boxcar.submit_config,
    KerrGating.boxcar.working_mode
)
foo2 = column(
    KerrGating.start_PWA,
    KerrGating.terminate_PWA,
    KerrGating.preview.PWA.fig,
)
bar = row(foo, foo2)
param_tab2 = Panel(child=bar, title="Boxcar Controller")
param_tabs = Tabs(tabs=[param_tab1, param_tab2], name="param")
doc.add_root(param_tabs)

# ================ manual ================
foo = column(
    KerrGating.linear_stage.test_online,
    KerrGating.linear_stage.manual_position,
    KerrGating.linear_stage.manual_move,
    KerrGating.linear_stage.manual_step,
    KerrGating.linear_stage.manual_step_forward,
    KerrGating.linear_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Linear Stage")
foo = column(
    KerrGating.boxcar.test_online,
)
manual_tab2 = Panel(child=foo, title="Boxcar Controller")
manual_tabs = Tabs(tabs=[manual_tab1, manual_tab2], name="manual")
doc.add_root(manual_tabs)

# ================ schedule ================
foo = column(
    KerrGating.generic.filestem,
    KerrGating.generic.scanrounds,
    KerrGating.start,
    KerrGating.terminate
)
schedule_tab1 = Panel(child=foo, title="KerrGating")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

# ================ reports ================
foo = column(
    KerrGating.preview.delay.fig,
    KerrGating.preview.delta.fig,
    KerrGating.preview.signal.fig,
    KerrGating.preview.background.fig,
)
reports_tab1 = Panel(child=foo, title="KerrGating")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
