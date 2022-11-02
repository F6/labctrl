# -*- coding: utf-8 -*-

"""main.py:
This module implements the
UV-Vis-IR Pump Terahertz Probe Spectroscopy
technic

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
__version__ = "20221028"


import time
import numpy as np

from functools import partial
from threading import Thread

from scipy.fft import fft, fftfreq, fftshift

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
from labctrl.methods.figure import FactoryFigure1D, FactoryFigure1DWithWhiskers, FactoryFigure2D

doc.template_variables["app_name"] = "pump_probe_THz"


# META SETTINGS
delay_stage = 'CDHD2'
ft_stage = 'USB1020'
boxcar_name = 'generic_boxcar'
# boxcar = 'ziUHF'


class THzPreviewFigure:
    """Images to be showed in the Preview tab
    """
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d(
            "Boxcar Signal", "Data #", "Intensity (V)", 256)
        self.ft_time_domain = factory.generate_fig1d(
            "Fourier Transform Delay Scan (E-Field)", "Time Delay (ps)", "Intensity (V)", 256)
        self.ft_freq_domain = factory.generate_fig1d(
            "FFT Terahertz Spectrum (Amplitude)", "Frequency (THz)", "Intensity (V*ps)", 256)
        # self.ft_phase = factory.generate_fig1d(
        #     "FFT Terahertz Spectrum (Phase)", "Frequency (THz)", "Intensity (V*ps)", 256)
        factory = FactoryFigure2D()
        self.pump_probe = factory.generate_fig2d(
            "Pump Probe", "Frequency (THz)", "Probe Time (ps)", "Intensity (V*ps)")

class THzExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg, lstat) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg

        # ======== Fourier Transform Time Domain Data ======== 
        self.ft_delays = lstat.stat[ft_stage]["ScanList"]
        self.ft_delays_min = np.min(self.ft_delays)
        self.ft_delays_max = np.max(self.ft_delays)
        self.ft_signal = np.zeros(len(self.ft_delays), dtype=np.float64)
        self.ft_signal_sum = np.zeros(len(self.ft_delays), dtype=np.float64)
        # # this is only used when using 2 backgrounds because the boxcar automatically subtracts background 
        # self.ft_background = np.zeros(len(self.ft_delays), dtype=np.float64)
        # self.ft_background_sum = np.zeros(len(self.ft_delays), dtype=np.float64)
        # self.ft_delta = np.zeros(len(self.ft_delays), dtype=np.float64)  # fig delay
        # self.ft_delta_stddev = np.zeros(
        #     len(self.ft_delays), dtype=np.float64)  # fig delay
        # self.ft_delta_sum = np.zeros(len(self.ft_delays), dtype=np.float64)

        # ======== Fourier Transform Frequency Domain Data ======== 
        N = len(self.ft_delays)
        T = self.ft_delays[1] - self.ft_delays[0] # assuming equal spaced FT
        self.fft_freqs = fftfreq(N, T)
        self.fft_freqs = fftshift(self.fft_freqs)
        self.fft_real = np.zeros(len(self.fft_freqs), dtype=np.float64)
        self.fft_imag = np.zeros(len(self.fft_freqs), dtype=np.float64)
        self.fft_abs = np.zeros(len(self.fft_freqs), dtype=np.float64)
        self.fft_phase = np.zeros(len(self.fft_freqs), dtype=np.float64)

        # ======== Pump Probe Data (2D) ======== 
        self.pp_delays = lstat.stat[delay_stage]["ScanList"]
        self.fft_freqs_min = np.min(self.fft_freqs)
        self.fft_freqs_max = np.max(self.fft_freqs)
        self.pp_delays_min = np.min(self.pp_delays)
        self.pp_delays_max = np.max(self.pp_delays)
        self.pp_signal = np.zeros((len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)

    def export(self, filestem: str) -> None:
        # filename = filestem + "-Time-Domain-Signal.csv"
        # tosave = self.ft_signal
        # np.savetxt(filename, tosave, delimiter=',')

        # filename = filestem + "-Freq-Domain-Signal.csv"
        # tosave = self.fft_abs
        # np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Pump-Probe-Signal.csv"
        tosave = self.pp_signal
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Frequencies.csv"
        tosave = np.array(self.fft_freqs)
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Pump-Probe-Delays.csv"
        tosave = np.array(self.pp_delays)
        np.savetxt(filename, tosave, delimiter=',')


class THzExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.start = Button(label="Start THz Pump Probe",
                            button_type='success')
        # self.pause = Button(label="Pause THz Pump Probe", button_type='warning')
        self.terminate = Button(
            label="Terminate THz Pump Probe", button_type='warning')
        self.preview = THzPreviewFigure()
        self.data = THzExpData(lcfg, lstat)
        factory = FactoryLinearStage()
        self.pump_probe_delay_stage = factory.generate_bundle(delay_stage, lcfg, lstat)
        self.fourier_transform_delay_stage = factory.generate_bundle(ft_stage, lcfg, lstat)
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


TerahertzPP = THzExperiment()


@TerahertzPP.generic.scan_round
@TerahertzPP.pump_probe_delay_stage.scan_delay
@TerahertzPP.fourier_transform_delay_stage.scan_delay
def unit_operation(meta=dict()):
    if TerahertzPP.flags["TERMINATE"]:
        meta["TERMINATE"] = True
        lstat.expmsg(
            "TerahertzPP operation received signal TERMINATE, trying graceful Thread exit")
        return
    lstat.expmsg("Retriving signal from sensor...")
    sig = TerahertzPP.boxcar.get_boxcar_data()
    lstat.expmsg("Adding latest signal to dataset...")
    ds = np.size(sig)
    sig_average = np.average(sig)
    delay_stat = lstat.stat[delay_stage]
    ft_stat = lstat.stat[ft_stage]

    TerahertzPP.data.ft_signal[ft_stat["iDelay"]] = sig_average
    TerahertzPP.data.ft_signal_sum[ft_stat["iDelay"]] += sig_average
    # update preview figures
    lstat.doc.add_next_tick_callback(
        partial(TerahertzPP.preview.signal.callback_update, np.arange(ds), sig))
    lstat.doc.add_next_tick_callback(
        partial(TerahertzPP.preview.ft_time_domain.callback_update, 
                TerahertzPP.data.ft_delays, TerahertzPP.data.ft_signal))
    
    # call FFT at real-time for preview. At least 5 points is needed for FFT
    if ft_stat["iDelay"] > 5:
        N = ft_stat["iDelay"]
        T = ft_stat["ScanList"][1] - ft_stat["ScanList"][0]
        yf = fft(TerahertzPP.data.ft_signal[0:N])
        xf = fftfreq(N, T)
        xf = fftshift(xf)
        yf = fftshift(yf)
        yf = yf / N
        lstat.doc.add_next_tick_callback(
            partial(TerahertzPP.preview.ft_freq_domain.callback_update, xf, np.abs(yf)))

    # if this is the end of THz FT scan, call FFT for THz
    if ft_stat["iDelay"] + 1 == len(ft_stat["ScanList"]):
        N = ft_stat["iDelay"] + 1
        T = ft_stat["ScanList"][1] - ft_stat["ScanList"][0]
        yf = fft(TerahertzPP.data.ft_signal)
        xf = fftfreq(N, T)
        xf = fftshift(xf)
        yf = fftshift(yf)
        yf = yf / N
        TerahertzPP.data.fft_abs = np.abs(yf)
        TerahertzPP.data.fft_imag = yf.imag
        TerahertzPP.data.fft_real = yf.real
        # copy the fft result to final output
        TerahertzPP.data.pp_signal[delay_stat["iDelay"], :] = np.copy(TerahertzPP.data.fft_abs)
        # update preview figures
        lstat.doc.add_next_tick_callback(
            partial(TerahertzPP.preview.ft_freq_domain.callback_update, xf, np.abs(yf)))
        lstat.doc.add_next_tick_callback(
            partial(TerahertzPP.preview.pump_probe.callback_update, TerahertzPP.data.pp_signal,
                    TerahertzPP.data.fft_freqs_min, TerahertzPP.data.fft_freqs_max, 
                    TerahertzPP.data.pp_delays_min, TerahertzPP.data.pp_delays_max)
        )



    # if this the end of delay scan, call export
    if delay_stat["iDelay"] + 1 == len(delay_stat["ScanList"]):
        lstat.expmsg("End of delay scan round, exporting data...")
        TerahertzPP.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                               "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))


def task():
    lstat.expmsg("Allocating memory for experiment")
    TerahertzPP.data = THzExpData(lcfg, lstat)
    lstat.expmsg("Starting experiment")
    meta = dict()
    meta["TERMINATE"] = False
    unit_operation(meta=meta)
    TerahertzPP.flags["FINISH"] = True
    TerahertzPP.flags["RUNNING"] = False
    lstat.expmsg("Experiment done")


def __callback_start():
    TerahertzPP.flags["TERMINATE"] = False
    TerahertzPP.flags["FINISH"] = False
    TerahertzPP.flags["RUNNING"] = True
    TerahertzPP.boxcar.set_working_mode("Boxcar")
    thread = Thread(target=task)
    thread.start()


TerahertzPP.start.on_click(__callback_start)


def __callback_terminate():
    lstat.expmsg("Terminating current job")
    TerahertzPP.flags["TERMINATE"] = True
    TerahertzPP.flags["FINISH"] = False
    TerahertzPP.flags["RUNNING"] = False


TerahertzPP.terminate.on_click(__callback_terminate)


# roots: ["dashboard", "setup", "param", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

# ================ params ================
foo = column(
    TerahertzPP.pump_probe_delay_stage.scan_mode,
    TerahertzPP.pump_probe_delay_stage.scan_zero,
    TerahertzPP.pump_probe_delay_stage.scan_start,
    TerahertzPP.pump_probe_delay_stage.scan_stop,
    TerahertzPP.pump_probe_delay_stage.scan_step,
    TerahertzPP.pump_probe_delay_stage.scan_file
)
param_tab1 = Panel(child=foo, title="Pump Probe Delay Line")
foo = column(
    TerahertzPP.fourier_transform_delay_stage.scan_mode,
    TerahertzPP.fourier_transform_delay_stage.scan_zero,
    TerahertzPP.fourier_transform_delay_stage.scan_start,
    TerahertzPP.fourier_transform_delay_stage.scan_stop,
    TerahertzPP.fourier_transform_delay_stage.scan_step,
    TerahertzPP.fourier_transform_delay_stage.scan_file
)
param_tab2 = Panel(child=foo, title="Fourier Transform Delay Line")
param_tabs = Tabs(tabs=[param_tab1, param_tab2], name="param")
doc.add_root(param_tabs)

# ================ manual ================
foo = column(
    TerahertzPP.pump_probe_delay_stage.test_online,
    TerahertzPP.pump_probe_delay_stage.manual_position,
    TerahertzPP.pump_probe_delay_stage.manual_move,
    TerahertzPP.pump_probe_delay_stage.manual_step,
    TerahertzPP.pump_probe_delay_stage.manual_step_forward,
    TerahertzPP.pump_probe_delay_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Pump Probe Delay Line")
foo = column(
    TerahertzPP.fourier_transform_delay_stage.test_online,
    TerahertzPP.fourier_transform_delay_stage.manual_position,
    TerahertzPP.fourier_transform_delay_stage.manual_move,
    TerahertzPP.fourier_transform_delay_stage.manual_step,
    TerahertzPP.fourier_transform_delay_stage.manual_step_forward,
    TerahertzPP.fourier_transform_delay_stage.manual_step_backward,
)
manual_tab2 = Panel(child=foo, title="Fourier Transform Delay Line")
manual_tabs = Tabs(tabs=[manual_tab1, manual_tab2], name="manual")
doc.add_root(manual_tabs)

# ================ schedule ================
foo = column(
    TerahertzPP.generic.filestem,
    TerahertzPP.generic.scanrounds,
    TerahertzPP.start,
    TerahertzPP.terminate
)
schedule_tab1 = Panel(child=foo, title="Terahertz Pump Probe")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

# ================ reports ================
foo = column(
    TerahertzPP.preview.signal.fig,
    TerahertzPP.preview.ft_time_domain.fig,
    TerahertzPP.preview.ft_freq_domain.fig,
    TerahertzPP.preview.pump_probe.fig,
)
reports_tab1 = Panel(child=foo, title="Terahertz Pump Probe")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
