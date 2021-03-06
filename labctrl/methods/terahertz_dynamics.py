# -*- coding: utf-8 -*-

"""THz.py:
This module implements the
Vis/IR Pump THz Probe Spectroscopy
technic

The terahertz dynamics experiment can be used to measure the time evolution
of low wavenumber vibrational modes in solids, for example the charge carrier
dynamics in solar cells, or energy transfer rate from/to low frequency modes in 
carbon nanotubes and graphene

In such experiments, an ultrafast laser pulse from an optical
parametric amplifier excites the molecules in a sample, then
another laser pulse which is in the range of THz is sent through
the sample and detected to determine the sample's transcient absorption
in the range of THz

The interval between the excitation pump pulse and the THz probe
pulse is set via optical delay line 1, which is the PMT48MT6 in A304.

The OPA for visible pump pulse is TOPAS. The self-made NOPA can also be
used, if all TOPAS are in use. However, if NOPA is used, the corresponding
factory in this script needs to be changed from FactoryTOPAS to FactoryNOPA.
The terahertz dynamics are quite slow in general, so no additional compression
is needed for the excitation pulse.

The terahertz probe pulse is generated via four-wave mixing in the air,
and filtered with a Si window to get rid of visible part from the 
supercontinuum. The mid-IR part of the supercontinnum white light can
pass through the Si window and serve as a rough indicator of the beam
location and shape, so you can use the simpler visible-pump-midIR-probe
signal to roughly adjust the spatial overlap of the visible pump pulse 
and the THz probe lightspot.

The four-wave mixing design is quite tricky to tweak, in case that the design
does not work, the probe pulse can also be generated by directly passing 800nm pulse to
a ZnTe crystal (100). The THz signal from ZnTe crystal is tested very clear and strong
for thickness of 0.5mm or 1mm, so it is much easier to detect. The drawback of the
ZnTe crystal is that it only generates THz pulse up to around 3 THz, in contrast,
the four-wave mixing generates THz pulse at all freqs up to mid-IR.

The THz pulse is detected by mixing it with a 808nm pulse. The 808nm pulse is focused
into a gas chamber with a pair of parallel metal plate installed, and the plate is charged
to high voltage just below the gas breakdown voltage to induce SHG at the focusing area.
When THz pulse is mixed into the area, the modulating electrical field of the THz pulse
alters the SHG efficiency and cause the intensity of the 404nm pulse to change periodically
with the phase of the THz light. Scanning the time delay between THz pulse and the 808nm 
pulse with optical delay line 2, which is the USB1020 linear stage at A304, the mixed signal
can be detected with PMT and then Fourier transformed to retrive the original THz signal. 

If a high voltage source is absent, electro-optical crystals can also be used to detect THz
pulse, for example 1mm ZnTe (100). In this case a circular polarized light and the THz pulse are
passed through the crystal, and the polarization of the light is modulated in the crystal, 
so a PBS/Glan prism can be inserted after the crystal and we can detect the p/s light 
intensity with balanced boxcar to recover the THz signal. However, this also limits our
detection spectrum to below 3 THz, again.

Like all pump-probe experiments, there's 4 signal taken for each round, so ideally the signal
is recovered by a 4-shot per round sampling with pump pulse chopped to 1/4 frequency of the repetition rate and probe pulse chopped to 1/2 frequency of the repetition rate. However, this
sampling scheme needs additional trigger phase information for each run. In our setup, the
pure THz absorption is extracted shot-to-shot by modulating the high voltage at 50% duty
cycle of the laser repetition rate, and the visible pump is modulated with a shutter to get
the delta OD. This setup is simpler than the 4-shot modulation and the phase of the shot-to-shot
subtraction is always correct, but it suffers more from 1/f noise and low frequency drifting
of the pulse intensities.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


import time
import numpy as np
from threading import Thread
from functools import partial
from bokeh.layouts import column, row
from bokeh.models.widgets import Button

from .common import FactoryFigure1D
from .generic import FactoryGenericMethods



"""
Terahertz dynamics 
    delay line 1: PMT48MT6
    delay line 2: USB1020
    topas: Topas_60fs
    boxcar: ziUHF
"""
dlname1 = "PMT48MT6"
dlname2 = "USB1020"
topasname = "Topas_60fs"
bxname = "ziUHF"


class THzPreviewFig:
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d(
            "Terahertz Signal (Pumped, Time Domain)", "Time (ps)", "Boxcar Delta (V)", 40)
        self.signal_fft_abs = factory.generate_fig1d(
            "Terahertz Spectrum (Pumped, FFT Abs)", "Frequency (THz)", "Intensity (V.ps)", 40)
        self.background = factory.generate_fig1d(
            "Terahertz Signal (Background, Time Domain)", "Time (ps)", "Boxcar Delta (V)", 40)
        self.background_fft_abs = factory.generate_fig1d(
            "Terahertz Spectrum (Background, FFT Abs)", "Frequency (THz)", "Intensity (V.ps)", 40)
        self.transmission = factory.generate_fig1d(
            "Terahertz Spectrum (Transmission)", "Frequency (THz)", "Transmission (%)", 40)

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
        self.pump_delays = lstat.stat[dlname1]["ScanList"]
        self.thz_scan_delays = lstat.stat[dlname2]["ScanList"]

        self.sig = np.zeros((len(self.pump_delays), len(self.thz_scan_delays)), dtype=np.float64)
        self.sigsum = np.zeros_like(self.sig)
        self.bg = np.zeros_like(self.sig)
        self.bgsum = np.zeros_like(self.sig)
        self.sig_fft = np.zeros_like(self.sig)
        self.sig_fft_sum = np.zeros_like(self.sig)
        self.bg_fft = np.zeros_like(self.sig)
        self.bg_fft_sum = np.zeros_like(self.sig)
        self.transmission = np.zeros_like(self.sig)


    def export(self, filestem: str) -> None:
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.pump_delays)
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Signal.csv"
        tosave = self.sig
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.sigsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Background.csv"
        tosave = self.bg
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Background.csv"
        tosave = self.bgsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Signal-FFT.csv"
        tosave = self.sig_fft
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal-FFT.csv"
        tosave = self.sig_fft_sum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Background.csv"
        tosave = self.bg
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Background.csv"
        tosave = self.bgsum
        np.savetxt(filename, tosave, delimiter=',')

class BundleKerrGating:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """
    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.start = Button(label="Start Kerr Gate Scan", button_type='success')
        # self.pause = Button(label="Pause Kerr Gate Scan", button_type='warning')
        self.terminate = Button(label="Terminate Kerr Gate Scan", button_type='warning')
        self.preview = KerrGatePreviewFig()
        self.generic = None
        self.delayline = None
        self.boxcar = None
        self.data = None
        self.unit_operation = None
        self.task = None
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

    def quick_control_group(self):
        return row(
            column(
            self.generic.quick_control_group(),
            # self.delayline.quick_control_group(),
            # self.boxcar.quick_control_group(),
            self.start,
            # self.pause,
            self.terminate),
            self.preview.signal.fig,
        )

class FactoryKerrGating:
    def __init__(self) -> None:
        pass

    def generate(self, bundle_linearstage, bundle_boxcar, lcfg, lstat) -> BundleKerrGating:
        """
        requires:
            bundle_linearstage -> must implement @scan_delay decorator
            bundle_boxcar -> must implement get_value function for single point detection
        """

        bundle = BundleKerrGating()
        bundle.delayline = bundle_linearstage
        bundle.boxcar = bundle_boxcar

        factory = FactoryGenericMethods()
        bundle.generic = factory.generate(lcfg, lstat)

        scan_round = bundle.generic.scan_round
        scan_delay = bundle.delayline.scan_delay


        @scan_round
        @scan_delay
        def unit_operation(meta=dict()):
            if bundle.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg("kerr_gating received signal TERMINATE, trying graceful Thread exit")
                return
            lstat.expmsg("Retriving signal from Lock-in amplifier data server")
            sig = bundle.boxcar.get_value()
            lstat.expmsg("Adding latest signal to dataset...")
            stat = lstat.stat[dlname]
            bundle.data.sig[stat["iDelay"]] = sig
            bundle.data.sigsum[stat["iDelay"]] += sig
            lstat.doc.add_next_tick_callback(
                partial(bundle.preview.signal.callback_update, stat["ScanList"], bundle.data.sig))
            # if this the end of delay scan, call export
            if stat["iDelay"] + 1 == len(stat["ScanList"]):
                bundle.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                            "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))

        bundle.unit_operation = unit_operation

        def task():
            lstat.expmsg("Allocating memory for experiment")
            bundle.data = KerrGateExpData(lcfg, lstat)
            lstat.expmsg("Starting experiment")
            meta = dict()
            meta["TERMINATE"] = False
            bundle.unit_operation(meta=meta)
            bundle.flags["FINISH"] = True
            bundle.flags["RUNNING"] = False
            lstat.expmsg("Experiment done")

        bundle.task = task

        def __callback_start():
            bundle.flags["TERMINATE"] = False
            bundle.flags["FINISH"] = False
            bundle.flags["RUNNING"] = True
            thread = Thread(target=bundle.task)
            thread.start()

        bundle.start.on_click(__callback_start)

        def __callback_terminate():
            lstat.expmsg("Terminating current job")
            bundle.flags["TERMINATE"] = True
            bundle.flags["FINISH"] = False
            bundle.flags["RUNNING"] = False

        bundle.terminate.on_click(__callback_terminate)

        return bundle

