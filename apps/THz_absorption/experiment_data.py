# -*- coding: utf-8 -*-

"""experiment_data.py:

This module holds the ExperimentData class for THz Pump Probe experiments.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221126"

import numpy as np
from scipy.fft import fft, fftfreq, fftshift

from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat


class THzExpData:
    """
    Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.

    names:
        original: Data points directly read from boxcar, need to be averaged

    data layout:
        1d array: ft delays
                  arr[i] = data for i-th ft delay
    
    exports:
        
        Only time domain (semi-original) data are saved because these
        are the only thing a user need to reconstruct everything.
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        ft_stage = lstat.stat["THz_absorption"]["FourierTransformDelayLine"]
        single_point_sample_size = lcfg.config["apps"]["THz_absorption"]["SinglePointSampleSize"]
        self.ft_delays = lstat.stat[ft_stage]["ScanList"]
        self.ft_delays_min = np.min(self.ft_delays)
        self.ft_delays_max = np.max(self.ft_delays)
        N = len(self.ft_delays)
        T = self.ft_delays[1] - self.ft_delays[0]  # assuming equal spaced FT
        self.fft_freqs = fftfreq(N, T)
        self.fft_freqs = fftshift(self.fft_freqs)
        self.fft_freqs_min = np.min(self.fft_freqs)
        self.fft_freqs_max = np.max(self.fft_freqs)
        # ======== Fourier Transform Time Domain Data ========
        self.original_signal = np.zeros(single_point_sample_size)
        self.original_x = np.arange(single_point_sample_size) # convenient when plotting
        self.time_domain_signal = np.zeros(
            (len(self.ft_delays)), dtype=np.float64)
        self.time_domain_signal_sum = np.zeros(
            (len(self.ft_delays)), dtype=np.float64)
        self.time_domain_signal_stddev = np.zeros(
            (len(self.ft_delays)), dtype=np.float64)
        # ======== Fourier Transform Frequency Domain Data (1D) ========
        self.fft_real_signal = np.zeros(
            (len(self.fft_freqs)), dtype=np.float64)
        self.fft_imag_signal = np.zeros(
            (len(self.fft_freqs)), dtype=np.float64)
        self.fft_abs_signal = np.zeros(
            (len(self.fft_freqs)), dtype=np.float64)
        self.fft_phase_signal = np.zeros(
            (len(self.fft_freqs)), dtype=np.float64)


    def export(self, filestem: str) -> None:
        filename = filestem + "-Time-Domain-Signal.csv"
        tosave = self.time_domain_signal
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Time-Domain-Signal-Sum.csv"
        tosave = self.time_domain_signal_sum
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Fourier-Transform-Delays.csv"
        tosave = np.array(self.ft_delays)
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Frequencies.csv"
        tosave = np.array(self.fft_freqs)
        np.savetxt(filename, tosave, delimiter=',')
