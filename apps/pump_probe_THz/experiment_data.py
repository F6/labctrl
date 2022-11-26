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
        signal: averaged from original, it is the signal with pump
        background: averaged from original, it is the signal without pump
        delta_od: = -log10(signal/background)

    data layout:
        2d array: pp delays first, ft delays second
                  arr[i, j] = data for i-th pp delay, j-th ft delay
    
    exports:
        
        Only time domain (semi-original) data are saved because these
        are the only thing a user need to reconstruct everything.
        
        pp_delta_od's are also exported, but just as a reference for
        the user to check their reconstruction code.
        
        The reason delta od's and FFT's are not exported is that when
        actually postprocessing the data, zero's must be padded to both ends
        of the time domain signal to interpolate the THz spectrum to
        make it smoother, because of limited FT scan range. (If we really
        don't care about experiment time, then we can use very large
        scan ranges to make the spectrum smooth and this is indeed the
        better way to do it, however in any practical experiment if 
        the FT range is too large not only the signal deteriorates because
        of unstablility of the laser, but also the sample degrades slowly
        because of intensive excitations...)

        Frequencies and Delay Lists are also exported just as a convenient
        way for postprocessing programs to read the X and Y axis ticks.
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        ft_stage = lstat.stat["pump_probe_THz"]["FourierTransformDelayLine"]
        pp_stage = lstat.stat["pump_probe_THz"]["PumpProbeDelayLine"]
        single_point_sample_size = lcfg.config["apps"]["pump_probe_THz"]["SinglePointSampleSize"]
        self.ft_delays = lstat.stat[ft_stage]["ScanList"]
        self.pp_delays = lstat.stat[pp_stage]["ScanList"]
        self.ft_delays_min = np.min(self.ft_delays)
        self.ft_delays_max = np.max(self.ft_delays)
        self.pp_delays_min = np.min(self.pp_delays)
        self.pp_delays_max = np.max(self.pp_delays)
        N = len(self.ft_delays)
        T = self.ft_delays[1] - self.ft_delays[0]  # assuming equal spaced FT
        self.fft_freqs = fftfreq(N, T)
        self.fft_freqs = fftshift(self.fft_freqs)
        self.fft_freqs_min = np.min(self.fft_freqs)
        self.fft_freqs_max = np.max(self.fft_freqs)
        # ======== Fourier Transform Time Domain Data ========
        self.original_signal = np.zeros(single_point_sample_size)
        self.original_background = np.zeros(single_point_sample_size)
        self.original_x = np.arange(single_point_sample_size) # convenient when plotting
        self.time_domain_signal = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_signal_sum = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_signal_stddev = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_background = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_background_sum = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_background_stddev = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_delta = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_delta_sum = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        self.time_domain_delta_stddev = np.zeros(
            (len(self.pp_delays), len(self.ft_delays)), dtype=np.float64)
        # ======== Fourier Transform Frequency Domain Data (2D) ========
        self.fft_real_signal = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        self.fft_imag_signal = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        self.fft_abs_signal = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        self.fft_phase_signal = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        self.fft_real_background = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        self.fft_imag_background = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        self.fft_abs_background = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        self.fft_phase_background = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)
        # ======== Pump Probe Data (1D) ========
        self.fft_abs_delta_od = np.zeros(len(self.fft_freqs), dtype=np.float64)
        # ======== Pump Probe Data (2D) ========
        self.pp_delta_od = np.zeros(
            (len(self.pp_delays), len(self.fft_freqs)), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Time-Domain-Signal.csv"
        tosave = self.time_domain_signal
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Time-Domain-Signal-Sum.csv"
        tosave = self.time_domain_signal_sum
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Time-Domain-Background.csv"
        tosave = self.time_domain_background
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Time-Domain-Background-Sum.csv"
        tosave = self.time_domain_background_sum
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Pump-Probe-Delta-OD.csv"
        tosave = self.pp_delta_od
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Fourier-Transform-Delays.csv"
        tosave = np.array(self.ft_delays)
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Frequencies.csv"
        tosave = np.array(self.fft_freqs)
        np.savetxt(filename, tosave, delimiter=',')

        filename = filestem + "-Pump-Probe-Delays.csv"
        tosave = np.array(self.pp_delays)
        np.savetxt(filename, tosave, delimiter=',')
