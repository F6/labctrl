# -*- coding: utf-8 -*-

"""kerr_gating.py:
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

the Zurich Instruments UHF is used as the boxcar integrator.
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
from .generic import BundleGenericMethods, FactoryGenericMethods



"""
Kerr Gating 
    delay line: AeroTech_NView
    boxcar: ziUHF
"""
dlname = "AeroTech_NView"
bxname = "ziUHF"


class KerrGatePreviewFig:
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d(
            "Kerr Gate Scan", "Time (ps)", "Boxcar Delta (V)", 40)


class KerrGateExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg, lstat) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg
        self.delays = lstat.stat[dlname]["ScanList"]
        self.sig = np.zeros(len(self.delays), dtype=np.float64)
        self.sigsum = np.zeros(len(self.delays), dtype=np.float64)

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

