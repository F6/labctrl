# -*- coding: utf-8 -*-

"""main.py:
This module implements the
Terahertz absorption spectroscopy technic

In such experiments, a laser pulse from an optical
parametric amplifier excites the molecules in a sample, then
another laser pulse which is in the range of THz is sent through
the sample and detected to determine the sample's transcient absorption
in the range of THz (i.e. the relatively slow modes of the molecule).

The experiment setup uses a femtosecond laser pulse to pump the sample.
A variable delay line delays another beam of pulsed 808 nm fs laser to generate
a time-delayed terahertz white light to probe the sample.
The terahertz white light pulse is detected using Fourier Transform technic, a
third beam of pulsed fs laser aligned temporally and spacially with the terahertz
white light on a nonlinear crystal, so that the strong electric field of THz pulse
rotates the polarization of the third pulse.
The rotation of the polarization is detected with a extremely sensitive balanced
detector (home made), the time delta between the thz white light and the third beam
is scanned by a second small delay line, and the intensity profile along the scan is
fourier transformed to retrive the original E-field frequency specrtum of the
terahertz white light.

A chopper chops the repetition rate of the pump laser to 1/2 frequency, to recover
the difference of the pumped and non-pumped signal. For generic Fourier Transform
detection, since FT(a(t) - b(t)) = FT(a(t)) - FT(b(t)), direct subtraction of detector
signal shot-to-shot can be used before FT.

the Zurich Instruments UHF is used as the boxcar integrator. When UHF
is not available we use our self made one
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20230316"


import time
import numpy as np

from functools import partial
from threading import Thread

from scipy.fft import fft, fftfreq, fftshift

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg, LabConfig
from labctrl.labstat import lstat, LabStat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.lockin_and_boxcars.factory import FactoryBoxcar
from labctrl.widgets.figure import FactoryFigure
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods

from .experiment_data import THzExpData

app_name = "THz_absorption"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["apps"][app_name]
ft_stage_name: str = app_config["FourierTransformDelayLine"]
boxcar_name: str = app_config["Boxcar"]
single_point_sample_size = app_config["SinglePointSampleSize"]
# Create a reference to app_config in lstat so that other modules can access it
lstat.stat[app_name] = app_config


class THzPreviewFigure:
    """
    This class holds references to bundles of figures in reports tab,
      it is not necessary to make it a class, because it will
      only be instantialized once. This class exists only as
      a compression so that the main experiment class is not
      too cumbersome...
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        factory = FactoryFigure(lcfg, lstat)
        figure_bundle_config = {"BundleType": "Bokeh",
                                "Config": app_config["SignalFigure"]}
        self.signal = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config = {"BundleType": "Bokeh",
                                "Config": app_config["FourierTransformSignalFigure"]}
        self.ft_signal = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config = {"BundleType": "Bokeh",
                                "Config": app_config["OriginalSignalFigure"]}
        self.original_signal = factory.generate_bundle(figure_bundle_config)


class THzExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        config = lcfg.config
        self.preview = THzPreviewFigure(lcfg, lstat)
        factory = FactoryLinearStage(lcfg, lstat)
        ft_stage_bundle_config = {
            "BundleType": "Bokeh",
            "Config": config["linear_stages"][ft_stage_name],
        }
        self.fourier_transform_delay_stage = factory.generate_bundle(
            ft_stage_bundle_config)
        factory = FactoryBoxcar(lcfg, lstat)
        boxcar_bundle_config = {
            "BundleType": "Bokeh",
            "Config": config["lockin_and_boxcars"][boxcar_name]
        }
        self.boxcar = factory.generate_bundle(boxcar_bundle_config)
        factory = FactoryGenericMethods()
        self.generic = factory.generate(lcfg, lstat)

        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

        self.data = THzExpData(lcfg, lstat)

        self.start = Button(label="Start THz",
                            button_type='success')
        # self.pause = Button(label="Pause THz", button_type='warning')
        self.terminate = Button(
            label="Terminate THz", button_type='warning')

        @self.generic.scan_round
        @self.fourier_transform_delay_stage.scan_range
        def unit_operation(meta=dict()):
            if self.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg(
                    "[THz] THz operation received signal TERMINATE, trying graceful Thread exit")
                return
            # ======== Begin ziUHF only data sampling ========
            lstat.expmsg("[THz][ziUHF Only] Retriving Signal from sensor...")
            while True:
                try:
                    # print("Getting Data")
                    self.data.original_signal = self.boxcar.get_boxcar_data(
                    single_point_sample_size)
                    break
                except Exception as e:
                    print("Error during retriving data, retry. Error:", e)
            # ======== End ziUHF only data sampling ========

            # aliases for delay stage states
            ft = lstat.stat[ft_stage_name]

            self.data.time_domain_signal[ft["iDelay"]] = np.average(
                self.data.original_signal)
            self.data.time_domain_signal_sum[ft["iDelay"]] += np.average(
                self.data.original_signal)

            # update preview figures after single sampling
            self.preview.original_signal.update(
                self.data.original_x, self.data.original_signal, lstat)
            self.preview.signal.update(
                self.data.ft_delays, self.data.time_domain_signal, lstat)

            # call FFT at real-time for preview. At least 5 points is needed for FFT
            if ft["iDelay"] > 5:
                N = ft["iDelay"] + 1
                T = ft["ScanList"][1] - ft["ScanList"][0]
                xf = fftfreq(N, T)
                xf = fftshift(xf)
                yf_signal = fft(
                    self.data.time_domain_signal[0:N])
                yf_signal = fftshift(yf_signal)
                yf_signal = yf_signal / N
                yf_signal_abs = np.abs(yf_signal)
                yf_signal_phase = np.arctan(
                    yf_signal.imag/yf_signal.real)
                self.preview.ft_signal.update(xf, yf_signal_abs, lstat)
                # copy fft result to output buffer if end of THz FT scan
                if ft["iDelay"] + 1 == len(ft["ScanList"]):
                    self.data.fft_real_signal = np.copy(
                        yf_signal.real)
                    self.data.fft_imag_signal = np.copy(
                        yf_signal.imag)
                    self.data.fft_abs_signal = np.copy(
                        yf_signal_abs)
                    self.data.fft_phase_signal = np.copy(
                        yf_signal_phase)

            # if this the end of delay scan, call export
            if ft["iDelay"] + 1 == len(ft["ScanList"]):
                lstat.expmsg("End of delay scan round, exporting data...")
                self.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                                 "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))

        def task():
            lstat.expmsg("Allocating memory for experiment")
            self.data = THzExpData(lcfg, lstat)
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
            thread = Thread(target=task)
            thread.start()

        self.start.on_click(__callback_start)

        def __callback_terminate():
            lstat.expmsg("Terminating current job")
            self.flags["TERMINATE"] = True
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = False

        self.terminate.on_click(__callback_terminate)


thz_absorption = THzExperiment(lcfg, lstat)


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

foo2 = column(
    Div(text="<b>Fourier Transform Delay Line:</b>"),
    thz_absorption.fourier_transform_delay_stage.host,
    thz_absorption.fourier_transform_delay_stage.port,
    thz_absorption.fourier_transform_delay_stage.multiples,
    thz_absorption.fourier_transform_delay_stage.working_direction,
    Div(text="Position and Limitation Unit:"),
    thz_absorption.fourier_transform_delay_stage.position_unit,
    thz_absorption.fourier_transform_delay_stage.zero_point_absolute_position,
    thz_absorption.fourier_transform_delay_stage.soft_limit_min,
    thz_absorption.fourier_transform_delay_stage.soft_limit_max,
    thz_absorption.fourier_transform_delay_stage.driving_speed,
    thz_absorption.fourier_transform_delay_stage.driving_speed_unit,
    thz_absorption.fourier_transform_delay_stage.driving_acceleration,
    thz_absorption.fourier_transform_delay_stage.driving_acceleration_unit,
)
bar = row(foo2)
setup_tab1 = Panel(child=bar, title="Delay Lines")
foo = column(
    thz_absorption.boxcar.host,
    thz_absorption.boxcar.port,
)
setup_tab2 = Panel(child=foo, title="Boxcar")
setup_tabs = Tabs(tabs=[setup_tab1, setup_tab2], name="setup")
doc.add_root(setup_tabs)
# endregion setup

# region params
# ================ params ================
foo2 = column(
    Div(text="<b>Fourier Transform Delay Line:</b>"),
    thz_absorption.fourier_transform_delay_stage.scan_mode,
    thz_absorption.fourier_transform_delay_stage.working_unit,
    thz_absorption.fourier_transform_delay_stage.range_scan_start,
    thz_absorption.fourier_transform_delay_stage.range_scan_stop,
    thz_absorption.fourier_transform_delay_stage.range_scan_step,
    thz_absorption.fourier_transform_delay_stage.external_scan_list_file
)
bar = row(foo2)
param_tab1 = Panel(child=bar, title="Delay Lines")
foo = column(
    Div(text="Boxcar Working Unit:"),
    thz_absorption.boxcar.working_unit,
    thz_absorption.boxcar.delay_background_sampling,
    thz_absorption.boxcar.delay_integrate,
    thz_absorption.boxcar.delay_hold,
    thz_absorption.boxcar.delay_signal_sampling,
    thz_absorption.boxcar.delay_reset,
    thz_absorption.boxcar.submit_config,
    Div(text="Boxcar Working Mode:"),
    thz_absorption.boxcar.working_mode,
    thz_absorption.boxcar.set_working_mode,
)
foo2 = column(
    thz_absorption.boxcar.start_PWA,
    thz_absorption.boxcar.stop_PWA,
    thz_absorption.boxcar.manual_get_PWA_data,
    thz_absorption.boxcar.PWA_figure.figure,
)
bar = row(foo, foo2)
param_tab2 = Panel(child=bar, title="Boxcar Controller")
param_tabs = Tabs(tabs=[param_tab1, param_tab2], name="param")
doc.add_root(param_tabs)
# endregion params

# region manual
# ================ manual ================
foo2 = column(
    Div(text="<b>Fourier Transform Delay Line:</b>"),
    thz_absorption.fourier_transform_delay_stage.test_online,
    Div(text="Manual Operation Unit:"),
    thz_absorption.fourier_transform_delay_stage.manual_unit,
    thz_absorption.fourier_transform_delay_stage.manual_position,
    thz_absorption.fourier_transform_delay_stage.manual_move,
    thz_absorption.fourier_transform_delay_stage.manual_step,
    thz_absorption.fourier_transform_delay_stage.manual_step_forward,
    thz_absorption.fourier_transform_delay_stage.manual_step_backward,
)
bar = row(foo2)
manual_tab1 = Panel(child=bar, title="Delay Lines")
foo = column(
    thz_absorption.boxcar.test_online,
    thz_absorption.boxcar.manual_get_boxcar_data,
)
foo2 = column(
    thz_absorption.boxcar.boxcar_preview.figure,
)
bar = row(foo, foo2)
manual_tab2 = Panel(child=bar, title="Boxcar Controller")
manual_tabs = Tabs(tabs=[manual_tab1, manual_tab2], name="manual")
doc.add_root(manual_tabs)
# endregion manual

# ================ schedule ================
foo = column(
    thz_absorption.generic.filestem,
    thz_absorption.generic.scanrounds,
    thz_absorption.start,
    thz_absorption.terminate
)
schedule_tab1 = Panel(child=foo, title="Terahertz Absorption")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

# ================ reports ================
foo = column(
    thz_absorption.preview.original_signal.figure,
    thz_absorption.preview.signal.figure,
    thz_absorption.preview.ft_signal.figure,
)
reports_tab1 = Panel(child=foo, title="Terahertz Absorption")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
