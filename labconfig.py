# -*- coding: utf-8 -*-

"""labconfig.py:
This module provides the singleton class LabConfig to hold parameters for
instruments and experiment configurations.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"

import json
import time
import os
import numpy as np
from datetime import datetime

from singleton import Singleton
from expmsg import expmsg


class LabConfig(metaclass=Singleton):
    """Singleton class to hold all the information needed for our experiment.
    """

    def __init__(self) -> None:
        # region Default Settings
        # IMFS: IR Modulated Fluorescence
        # WLS: White light spectrum test
        # IPVP: IR Pump Visible Probe
        # TRPL: Time-resolved Photoluminescence (Kerr Gating)
        self.experiment_type = "IMFS"
        self.file_stem = "NewSample"
        self.scan_rounds = 10

        self.andor_camera = dict()
        self.andor_camera["ExposureTime"] = 1.0
        self.andor_camera["ManualSignalNo"] = 0

        self.shutter = dict()
        self.shutter["UseShutterBackground"] = False

        self.photodiode = dict()
        self.photodiode["TakePhotodiodeReference"] = False

        # False: This parameter is maually set by hand or other program.
        # Range: Automatically generate an evenly-stepped list to scan over.
        # ExtFile: Load a scan list from an external ascii file.
        self.scan_modes = (False, "Range", "ExtFile")

        self.visible_topas = dict()
        self.visible_topas["Name"] = "VisibleTopas"
        self.visible_topas["Unit"] = "nm"
        self.visible_topas["Mode"] = "Range"
        self.visible_topas["Start"] = 460
        self.visible_topas["Step"] = 10
        self.visible_topas["Stop"] = 481
        self.visible_topas["ScanList"] = list()
        # this ExternalList is used to temporarily hold loaded external list so
        #  that if the user switches to other scan modes and then switches back,
        #  the list does not need to be loaded from a file again.
        # the list used in experiment procedures is always Scanlist, do not use
        #  this ExternalList other than temporarily holding data.
        self.visible_topas["ExternalList"] = list()

        self.ir_topas = dict()
        self.ir_topas["Name"] = "IRTopas"
        self.ir_topas["Unit"] = "cm-1"
        self.ir_topas["Mode"] = "Range"
        self.ir_topas["Start"] = 1300
        self.ir_topas["Step"] = 10
        self.ir_topas["Stop"] = 1700
        self.ir_topas["ScanList"] = list()
        self.ir_topas["ExternalList"] = list()

        self.delay_line = dict()
        self.delay_line["Name"] = "DelayLine"
        self.delay_line["Unit"] = "ps"
        self.delay_line["Mode"] = "Range"
        self.delay_line["Start"] = -10
        self.delay_line["Step"] = 1
        self.delay_line["Stop"] = 20
        self.delay_line["ScanList"] = list()
        self.delay_line["ExternalList"] = list()
        self.delay_line["ZeroAbsPos"] = -120.158
        # temporarily hold the value for manual operations
        self.delay_line["ManualPos"] = self.delay_line["ZeroAbsPos"]

        self.monochromer = dict()
        self.monochromer["Name"] = "7IMSU"
        self.monochromer["UnitRaw"] = "step"
        self.monochromer["Unit"] = "nm"
        self.monochromer["Mode"] = "Range"
        self.monochromer["Start"] = 200
        self.monochromer["Step"] = 20
        self.monochromer["Stop"] = 600
        self.monochromer["ScanList"] = list()
        self.monochromer["ExternalList"] = list()
        # zero point deviation is 1680 steps from 0
        self.monochromer["ZeroAbsPos"] = 1680
        self.monochromer["ManualRawPos"] = 0
        self.monochromer["ManualCalibratedPos"] = 0
        self.monochromer["CalibrationTable"] = dict()
        self.monochromer["CalibrationTable"]["Wavelength"] = [200, 400, 500]
        self.monochromer["CalibrationTable"]["Step"] = [10000, 20000, 30000]
        self.monochromer["CalibrationModel"] = "Linear"

        # Video: The camera constantly refreshes itself, and notify the program if a new frame is available
        # SoftwareTrigger: The camera holds for command from this software to start integrating
        # ExternalTrigger: The camera waits for a external signal to start integrating to keep sync with other hardware
        self.camera_modes = ("Video", "SoftwareTrigger", "ExternalTrigger")

        self.toupcamera = dict()
        self.toupcamera["Name"] = "ToupTekCamera"
        self.toupcamera["Mode"] = "Video"
        self.toupcamera["Width"] = 2592
        self.toupcamera["Height"] = 1944
        # microseconds
        self.toupcamera["ExposureTime"] = 100000
        self.toupcamera["TargetTemperature"] = 0
        # upper half of the CMOS is used for signal measuring and the
        #  bottom half is used for reference signal measuring
        self.toupcamera["SignalLower"] = 0
        self.toupcamera["SignalUpper"] = 500
        self.toupcamera["ReferenceLower"] = 1000
        self.toupcamera["ReferenceUpper"] = 1500
        self.toupcamera["SpectralWidth"] = 25  # nm

        # Demodulator: The Lock-in amplifier demodulates the signal amplitude and
        #              phase from carrier
        # BoxcarAverager: Use Boxcar Averager to recover signal
        self.lockin_modes = ("Demodulator", "BoxcarAverager")
        self.ziUHF = dict()
        self.ziUHF["Name"] = "ZurichInstrumentsUHF"
        self.ziUHF["DeviceID"] = 'dev2480'
        self.ziUHF["ServerHost"] = "localhost"
        self.ziUHF["ServerPort"] = 8004
        self.ziUHF["APILevel"] = 6
        self.ziUHF["Mode"] = "Boxcar"
        self.ziUHF["Boxcar"] = dict() # params for boxcar averager
        self.ziUHF["Boxcar"]["out_channel"] = 0
        self.ziUHF["Boxcar"]["in_channel"] = 0
        self.ziUHF["Boxcar"]["osc_index"] = 0
        self.ziUHF["Boxcar"]["frequency"] = 400e3
        self.ziUHF["Boxcar"]["boxcar_index"] = 0
        self.ziUHF["Boxcar"]["inputpwa_index"] = 0
        self.ziUHF["Boxcar"]["amplitude"] = 0.5
        self.ziUHF["Boxcar"]["frequency"] = 9.11e6
        self.ziUHF["Boxcar"]["windowstart"] = 75
        self.ziUHF["Boxcar"]["windowsize"] = 3e-9
        self.ziUHF["Boxcar"]["periods"] = 512


        # endregion

    def load_config(self, config: dict = None) -> None:
        """If a config is loaded, recursively overwrite default settings 
        or current settings.
        This method only cares about loading config, scanlists are not 
        automatically generated. If that is desired, call refresh_config 
        after loading config
        """
        def recursive_load(df: dict, dt: dict) -> None:
            for k, v in iter(df.items()):
                if type(v) is not dict:
                    dt[k] = v
                else:
                    recursive_load(v, dt[k])

        if config:
            for k, v in iter(config.items()):
                if type(v) is not dict:
                    self.__dict__[k] = v
                else:
                    recursive_load(v, self.__dict__[k])

    def save_config(self, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    def generate_scanlist(self, device: dict) -> list:
        """After experiment settings are changed, scanlists need to be automatically
        generated."""

        if device["Mode"] == 'ExtFile':
            # if the flag is set to Ext, then the ext list is set by external program so just copy it
            device["ScanList"] = device["ExternalList"]
        elif device["Mode"] == 'Range':
            # if the flag is set to True, then we need to construct scan lists by given parameter
            device["ScanList"] = np.arange(
                device["Start"], device["Stop"], device["Step"]).tolist()
        else:
            # this sets the len of the list to 1 for our convenience when dealing with for loops,
            #  while preventing accidentally set wavelengths or delays if we have a bug elsewhere
            device["ScanList"] = [None]

        return device["ScanList"]

    def update_lists(self) -> None:
        """Generate ScanLists for all enabled devices"""
        enabled_devices = (
            self.visible_topas,
            self.ir_topas,
            self.delay_line,
            self.monochromer,
        )
        for device in enabled_devices:
            self.generate_scanlist(device)

    def print_lists(self) -> str:
        """returns an html preformatted string for overview of 
        experiment parameters
        """
        enabled_devices = (
            self.visible_topas,
            self.ir_topas,
            self.delay_line,
            self.monochromer,
        )
        sl = list()
        for device in enabled_devices:
            if device["Mode"] == 'ExtFile':
                m = "(Set by external list)"
            elif device["Mode"] == 'Range':
                m = '(Generated list)'
            else:
                m = '(Manually Set)'
            s = '    {name}({unit}):{m}{l}'.format(
                name=device["Name"],
                unit=device["Unit"],
                m=m,
                l=str(device["ScanList"])
            )
            sl.append(s)
        l_str = "Scan Sums:\n" + \
            '\n'.join(sl) + '\n    Delayzero   : {zero} mm (Absolute distance from Home)'.format(
                zero=self.delay_line["ZeroAbsPos"])

        return l_str

    def estimate_time(self) -> str:
        """returns a html preformatted string for summary of 
        experiment time
        """
        enabled_devices = (
            self.visible_topas,
            self.ir_topas,
            self.delay_line,
            self.monochromer,
        )
        # total sample number is the product of the length of each set of params
        scan_len = 1
        for device in enabled_devices:
            scan_len *= len(device["ScanList"])
        # each sample will cost exposure time to be taken
        # if self.experiment_type == "IMFS":
        #     t_each_sample = self.andor_camera["ExposureTime"]
        # elif self.experiment_type == "WLS":
        #     t_each_sample = self.toupcamera["ExposureTime"]
        t_each_sample = 1
        # because network latency, add 1 second to exposure for a more precise estimation
        t_each_sample = t_each_sample + 1
        # if a shutter is used to take background for each param, the time required is doubled
        if self.shutter["UseShutterBackground"]:
            t_each_sample = t_each_sample * 2

        t_now = str(datetime.now())
        t_delay = scan_len * t_each_sample
        t_total = t_delay * self.scan_rounds
        t_est = str(datetime.fromtimestamp(time.time() + t_total))
        t_delay = '{h:.0f} hours {m:.0f} mins {s} seconds'.format(
            h=t_delay//3600, m=t_delay % 3600//60, s=t_delay % 60)
        t_total = '{h:.0f} hours {m:.0f} mins {s} seconds'.format(
            h=t_total//3600, m=t_total % 3600//60, s=t_total % 60)
        t_str = '''Time Sums:
    Start time  : {t_now}
    Round time  : {t_delay}
    Total time  : {t_total}
    Est. finish : {t_est}'''.format(t_now=t_now, t_delay=t_delay, t_total=t_total, t_est=t_est)
        return t_str

    def refresh_config(self) -> None:
        """Regenerate all scan lists, and save backup config in last_config.json"""
        self.update_lists()
        self.save_config("last_config.json")
        # a convenient alias: print sums when refresh config
        expmsg(self.print_lists())
        expmsg(self.estimate_time())


lcfg = LabConfig()
last_config_file = "last_config.json"
if last_config_file in os.listdir():
    with open(last_config_file, 'r') as f:
        last_config = json.load(f)
    lcfg.load_config(last_config)
    lcfg.refresh_config()
    expmsg("Automatically loaded previous configs from last_config.json")
