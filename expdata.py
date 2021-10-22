# -*- coding: utf-8 -*-

"""expdata.py:
This module provides the class ExpData to temporarily hold
the data generated in experiment.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"


from labconfig import LabConfig
import numpy as np
from scipy import signal

from andor_camera import ANDOR_CCD_PIXELS_WIDTH


class ExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg: LabConfig) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg
        if lcfg.experiment_type == "IMFS":  # IR Modulated Fluorescence Spectroscopy
            self.__init_imfs()
        elif lcfg.experiment_type == "WLS":
            self.__init_wls()
        elif lcfg.experiment_type == "IPVP":
            self.__init_ipvp()
        elif lcfg.experiment_type == "TRPL":
            self.__init_trpl()

    def export(self, filestem: str) -> None:
        if self.lcfg.experiment_type == "IMFS":  # IR Modulated Fluorescence Spectroscopy
            self.__export_imfs(filestem)
        elif self.lcfg.experiment_type == "WLS":
            self.__export_wls(filestem)
        elif self.lcfg.experiment_type == "IPVP":
            self.__export_ipvp(filestem)
        elif self.lcfg.experiment_type == "TRPL":
            self.__export_trpl(filestem)

    def __init_imfs(self) -> None:
        """allocate space for IR Modulated Fluorescence Spectroscopy experiment.
        There's 4 dimensions for such experiment: delay line, visible wavelength,
        IR wavelength and fluorescence spectrum.
        4 different signal is measured:
            sig   : The fluorescence signal with both IR and visible pulse present
            bg    : The fluorescence signal with only visible pulse present
            sigref: Power of visible pulse when measuring sig
            bgref : Power of visible pulse when measuring bg 
        For references, the fluorescence spectrum does not need to be measured,
        only the power of the excitation light (a number) is required, so the 
        reference matrices are 3-dimensional.
        """
        len_delay = len(self.lcfg.delay_line["ScanList"])
        len_vis = len(self.lcfg.visible_topas["ScanList"])
        len_ir = len(self.lcfg.ir_topas["ScanList"])
        self.sig = np.zeros(
            (len_delay, len_vis, len_ir, ANDOR_CCD_PIXELS_WIDTH), dtype=np.int64)
        self.bg = np.zeros(
            (len_delay, len_vis, len_ir, ANDOR_CCD_PIXELS_WIDTH), dtype=np.int64)
        self.sigref = np.zeros(
            (len_delay, len_vis, len_ir), dtype=np.float32)
        self.bgref = np.zeros(
            (len_delay, len_vis, len_ir), dtype=np.float32)
        # The results from different rounds are summed and previewed on-the-fly,
        #  so a seperate space needs to be allocated for the summed results
        self.sigsum = np.zeros(
            (len_delay, len_vis, len_ir, ANDOR_CCD_PIXELS_WIDTH), dtype=np.int64)
        self.bgsum = np.zeros(
            (len_delay, len_vis, len_ir, ANDOR_CCD_PIXELS_WIDTH), dtype=np.int64)
        self.sigrefsum = np.zeros(
            (len_delay, len_vis, len_ir), dtype=np.float32)
        self.bgrefsum = np.zeros(
            (len_delay, len_vis, len_ir), dtype=np.float32)

    def __export_imfs(self, filestem: str) -> None:
        """export data for IMFS scans"""
        scan_ir_only = (self.lcfg.delay_line["Mode"] == False) and (
            self.lcfg.visible_topas["Mode"] == False) and (self.lcfg.ir_topas["Mode"] != False)
        if scan_ir_only:
            filename = filestem + "-Signal.csv"
            np.savetxt(filename, self.sig[0, 0, :, :], delimiter=',')
            filename = filestem + "-Background.csv"
            np.savetxt(filename, self.bg[0, 0, :, :], delimiter=',')
            filename = filestem + "-SignalReference.csv"
            np.savetxt(filename, self.sigref[0, 0, :], delimiter=',')
            filename = filestem + "-BackgroundReference.csv"
            np.savetxt(filename, self.bgref[0, 0, :], delimiter=',')
            filename = filestem + "-Sum-Signal.csv"
            np.savetxt(filename, self.sigsum[0, 0, :, :], delimiter=',')
            filename = filestem + "-Sum-Background.csv"
            np.savetxt(filename, self.bgsum[0, 0, :, :], delimiter=',')
            filename = filestem + "-Sum-SignalReference.csv"
            np.savetxt(filename, self.sigrefsum[0, 0, :], delimiter=',')
            filename = filestem + "-Sum-BackgroundReference.csv"
            np.savetxt(filename, self.bgrefsum[0, 0, :], delimiter=',')
            filename = filestem + "-SignalDelta.csv"
            np.savetxt(
                filename, self.sig[0, 0, :, :] - self.bg[0, 0, :, :], delimiter=',')
            filename = filestem + "-Sum-SignalDelta.csv"
            np.savetxt(
                filename, self.sigsum[0, 0, :, :] - self.bgsum[0, 0, :, :], delimiter=',')
            return
        scan_delay_only = (self.lcfg.delay_line["Mode"] != False) and (
            self.lcfg.visible_topas["Mode"] == False) and (self.lcfg.ir_topas["Mode"] == False)
        if scan_delay_only:
            filename = filestem + "-Signal.csv"
            np.savetxt(filename, self.sig[:, 0, 0, :], delimiter=',')
            filename = filestem + "-Background.csv"
            np.savetxt(filename, self.bg[:, 0, 0, :], delimiter=',')
            filename = filestem + "-SignalReference.csv"
            np.savetxt(filename, self.sigref[:, 0, 0], delimiter=',')
            filename = filestem + "-BackgroundReference.csv"
            np.savetxt(filename, self.bgref[:, 0, 0], delimiter=',')
            filename = filestem + "-Sum-Signal.csv"
            np.savetxt(filename, self.sigsum[:, 0, 0, :], delimiter=',')
            filename = filestem + "-Sum-Background.csv"
            np.savetxt(filename, self.bgsum[:, 0, 0, :], delimiter=',')
            filename = filestem + "-Sum-SignalReference.csv"
            np.savetxt(filename, self.sigrefsum[:, 0, 0], delimiter=',')
            filename = filestem + "-Sum-BackgroundReference.csv"
            np.savetxt(filename, self.bgrefsum[:, 0, 0], delimiter=',')
            filename = filestem + "-SignalDelta.csv"
            np.savetxt(
                filename, self.sig[:, 0, 0, :] - self.bg[:, 0, 0, :], delimiter=',')
            filename = filestem + "-Sum-SignalDelta.csv"
            np.savetxt(
                filename, self.sigsum[:, 0, 0, :] - self.bgsum[:, 0, 0, :], delimiter=',')
            return

        # regular scan, do regular save
        for i in range(len(self.lcfg.delay_line["ScanList"])):
            for j in range(len(self.lcfg.visible_topas["ScanList"])):
                filename = filestem + "-{d}ps-{v}nm-Signal.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.sig[i, j, :, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-Background.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.bg[i, j, :, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-SignalReference.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.sigref[i, j, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-BackgroundReference.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.bgref[i, j, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-Sum-Signal.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.sigsum[i, j, :, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-Sum-Background.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.bgsum[i, j, :, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-Sum-SignalReference.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.sigrefsum[i, j, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-Sum-BackgroundReference.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(filename, self.bgrefsum[i, j, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-SignalDelta.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(
                    filename, self.sig[i, j, :, :] - self.bg[i, j, :, :], delimiter=',')
                filename = filestem + "-{d}ps-{v}nm-Sum-SignalDelta.csv".format(
                    d=self.lcfg.delay_line["ScanList"][i],
                    v=self.lcfg.visible_topas["ScanList"][j])
                np.savetxt(
                    filename, self.sigsum[i, j, :, :] - self.bgsum[i, j, :, :], delimiter=',')

    def __init_wls(self):
        """allocate space for white light spectrum test experiment.
        There's 2 dimensions for such experiment: monochromer central wavelength
         and white light spectrum.
        1 signal is measured for each monochromer wavelength:
            sig   : The white light spectrum at this wavelength
        """
        len_mono = len(self.lcfg.monochromer["ScanList"])

        self.sig = np.zeros(
            (len_mono, self.lcfg.toupcamera["Width"]), dtype=np.int64)

        # The results from different rounds are summed and previewed on-the-fly,
        #  so a seperate space needs to be allocated for the summed results
        self.sigsum = np.zeros(
            (len_mono, self.lcfg.toupcamera["Width"]), dtype=np.int64)
        self.ref = np.zeros(
            (len_mono, self.lcfg.toupcamera["Width"]), dtype=np.int64)
        self.refsum = np.zeros(
            (len_mono, self.lcfg.toupcamera["Width"]), dtype=np.int64)

    def __export_wls(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        np.savetxt(filename, self.sig, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        np.savetxt(filename, self.sigsum, delimiter=',')
        filename = filestem + "-Reference.csv"
        np.savetxt(filename, self.ref, delimiter=',')
        filename = filestem + "-Sum-Reference.csv"
        np.savetxt(filename, self.refsum, delimiter=',')

    def __init_ipvp(self):
        """allocate space for IR Pump Visible Probe experiment.
        There's 3 dimensions for such experiment: IR delay, monochromer central wavelength
         and white light spectrum.
        1 signal is measured for each monochromer wavelength:
            sig   : The white light spectrum at this wavelength
        """
        len_delay = len(self.lcfg.delay_line["ScanList"])
        len_mono = len(self.lcfg.monochromer["ScanList"])

        self.sig = np.zeros(
            (len_mono, len_delay, self.lcfg.toupcamera["Width"]), dtype=np.int64)

        # The results from different rounds are summed and previewed on-the-fly,
        #  so a seperate space needs to be allocated for the summed results
        self.sigsum = np.zeros(
            (len_mono, len_delay, self.lcfg.toupcamera["Width"]), dtype=np.int64)
        self.ref = np.zeros(
            (len_mono, len_delay, self.lcfg.toupcamera["Width"]), dtype=np.int64)
        self.refsum = np.zeros(
            (len_mono, len_delay, self.lcfg.toupcamera["Width"]), dtype=np.int64)

    def __export_ipvp(self, filestem: str) -> None:
        for i in range(len(self.lcfg.monochromer["ScanList"])):
            filename = filestem + "-{d}nm-Signal.csv".format(
                d=self.lcfg.monochromer["ScanList"][i])
            tosave = self.sig[i, :, :]
            # tosave = signal.savgol_filter(tosave, 161, 3)
            np.savetxt(filename, tosave, delimiter=',')
            filename = filestem + "-{d}nm-Sum-Signal.csv".format(
                d=self.lcfg.monochromer["ScanList"][i])
            tosave = self.sigsum[i, :, :]
            # tosave = signal.savgol_filter(tosave, 161, 3)
            np.savetxt(filename, tosave, delimiter=',')
            filename = filestem + "-{d}nm-Reference.csv".format(
                d=self.lcfg.monochromer["ScanList"][i])
            tosave = self.ref[i, :, :]
            # tosave = signal.savgol_filter(tosave, 161, 3)
            np.savetxt(filename, tosave, delimiter=',')
            filename = filestem + "-{d}nm-Sum-Reference.csv".format(
                d=self.lcfg.monochromer["ScanList"][i])
            tosave = self.refsum[i, :, :]
            # tosave = signal.savgol_filter(tosave, 161, 3)
            np.savetxt(filename, tosave, delimiter=',')
            filename = filestem + "-{d}nm-Ratio.csv".format(
                d=self.lcfg.monochromer["ScanList"][i])
            tosave = np.divide(self.sigsum[i, :, :], self.refsum[i, :, :])
            # tosave = signal.savgol_filter(tosave, 161, 3)
            np.savetxt(filename, tosave, delimiter=',')

    def __init_trpl(self):
        """allocate space for Kerr Gating Time-resolved Photoluminescence 
        Spectroscopy experiment.
        There's only 1 dimension for such experiment: signal strength over
        time delay.
        1 signal is measured for each time delay:
            sig   : The intensity at this time delay
        """
        len_delay = len(self.lcfg.delay_line["ScanList"])

        self.sig = np.zeros(len_delay, dtype=np.int64)

        # The results from different rounds are summed and previewed on-the-fly,
        #  so a seperate space needs to be allocated for the summed results
        self.sigsum = np.zeros(len_delay, dtype=np.int64)

    def __export_trpl(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        np.savetxt(filename, self.sig, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        np.savetxt(filename, self.sigsum, delimiter=',')
