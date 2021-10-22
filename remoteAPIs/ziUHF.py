# -*- coding: utf-8 -*-

"""ziUHF.py:
This module provides methods to communicate with a remote
Zurich Instruments UHF 600MHz Lock-in Amplifier Data Server
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211021"

import time
import numpy as np
import zhinst.utils

# TODO: importing from upper folder is ugly and risky
from ..labconfig import lcfg


class ziUHF:
    """Temporarily holds data from UHF device, also manages the API session from
    LabOne Data Server"""

    def __init__(self) -> None:
        self.daq = None
        self.device = None
        self.props = None

    def init_session(self) -> None:
        # Call a zhinst utility function that returns:
        # - an API session `daq` in order to communicate with devices via the data server.
        # - the device ID string that specifies the device branch in the server's node hierarchy.
        # - the device's discovery properties.
        (self.daq, self.device, self.props) = zhinst.utils.create_api_session(
            lcfg.ziUHF["DeviceID"], lcfg.ziUHF["APILevel"], server_host=lcfg.ziUHF["ServerHost"], server_port=lcfg.ziUHF["ServerPort"]
        )
        zhinst.utils.api_server_version_check(self.daq)

        # Create a base configuration: Disable all available outputs, awgs, demods, scopes,...
        zhinst.utils.disable_everything(self.daq, self.device)

    def close_session(self) -> None:
        # Unsubscribe from all paths
        self.daq.unsubscribe("*")
        # flush streaming data still in the buffer
        self.daq.flush()
        # disable all outputs and inputs to prevent accidental electrical damage
        zhinst.utils.disable_everything(self.daq, self.device)

    def init_boxcar(self) -> None:
        """Configures the ziUHF instrument for boxcar averaging measurement.
        """
        # Now configure the instrument for this experiment. The following channels
        # and indices work on all device configurations. The values below may be
        # changed if the instrument has multiple input/output channels and/or either
        # the Multifrequency or Multidemodulator options installed.
        out_mixer_channel = zhinst.utils.default_output_mixer_channel(
            self.props)

        bp = lcfg.ziUHF["Boxcar"]  # Boxcar Params

        exp_setting = [
            ["/%s/sigins/%d/imp50" %
                (self.device, bp["in_channel"]), 1],
            ["/%s/sigins/%d/ac" %
                (self.device, bp["in_channel"]), 0],
            ["/%s/sigins/%d/range" %
                (self.device, bp["in_channel"]), 2 * bp["amplitude"]],
            ["/%s/inputpwas/%d/oscselect" %
                (self.device, bp["inputpwa_index"]), bp["osc_index"]],
            ["/%s/inputpwas/%d/inputselect" %
                (self.device, bp["inputpwa_index"]), bp["in_channel"]],
            ["/%s/inputpwas/%d/mode" % (self.device, bp["inputpwa_index"]), 1],
            ["/%s/inputpwas/%d/shift" %
                (self.device, bp["inputpwa_index"]), 0.0],
            ["/%s/inputpwas/%d/harmonic" %
                (self.device, bp["inputpwa_index"]), 1],
            ["/%s/inputpwas/%d/enable" %
                (self.device, bp["inputpwa_index"]), 1],
            ["/%s/boxcars/%d/oscselect" %
                (self.device, bp["boxcar_index"]), bp["osc_index"]],
            ["/%s/boxcars/%d/inputselect" %
                (self.device, bp["boxcar_index"]), bp["in_channel"]],
            ["/%s/boxcars/%d/windowstart" %
                (self.device, bp["boxcar_index"]), bp["windowstart"]],
            ["/%s/boxcars/%d/windowsize" %
                (self.device, bp["boxcar_index"]), bp["windowsize"]],
            ["/%s/boxcars/%d/limitrate" %
                (self.device, bp["boxcar_index"]), 1e3],
            ["/%s/boxcars/%d/periods" %
                (self.device, bp["boxcar_index"]), bp["periods"]],
            ["/%s/boxcars/%d/enable" % (self.device, bp["boxcar_index"]), 1],
            ["/%s/oscs/%d/freq" %
                (self.device, bp["osc_index"]), bp["frequency"]],
            ["/%s/sigouts/%d/on" % (self.device, bp["out_channel"]), 1],
            ["/%s/sigouts/%d/enables/%d" %
                (self.device, bp["out_channel"], out_mixer_channel), 1],
            ["/%s/sigouts/%d/range" % (self.device, bp["out_channel"]), 1],
            [
                "/%s/sigouts/%d/amplitudes/%d" % (self.device,
                                                  bp["out_channel"], out_mixer_channel),
                bp["amplitude"],
            ],
        ]
        self.daq.set(exp_setting)

        # Wait for boxcar output to settle
        time.sleep(bp["periods"] / bp["frequency"])

        # Perform a global synchronisation between the device and the data server:
        # Ensure that the settings have taken effect on the device before issuing
        # the poll().
        self.daq.sync()

        # Get the values that were actually set on the device
        frequency_set = self.daq.getDouble(
            "/%s/oscs/%d/freq" % (self.device, bp["osc_index"]))
        windowstart_set = self.daq.getDouble(
            "/%s/boxcars/%d/windowstart" % (self.device, bp["boxcar_index"])
        )
        windowsize_set = self.daq.getDouble(
            "/%s/boxcars/%d/windowsize" % (self.device, bp["boxcar_index"]))
        # Subscribe to the nodes we would like to record data from
        self.boxcar_sample_path = "/%s/boxcars/%d/sample" % (
            self.device, bp["boxcar_index"])
        boxcar_periods_path = "/%s/boxcars/%d/periods" % (
            self.device, bp["boxcar_index"])
        inputpwa_wave_path = "/%s/inputpwas/%d/wave" % (
            self.device, bp["inputpwa_index"])
        self.daq.subscribe(
            [self.boxcar_sample_path, boxcar_periods_path, inputpwa_wave_path])
        # We use getAsEvent() to ensure we obtain the first ``periods`` value; if
        # its value didn't change, the server won't report the first value.
        self.daq.getAsEvent(boxcar_periods_path)

    def get_boxcar_value(self, averaging_time=0.1):
        # flush old streaming data that is still in the buffer
        self.daq.flush()
        tnow = time.time_ns()
        tuntil = tnow + averaging_time * 10e9
        datas = list()
        while time.time_ns() < tuntil:
            # Poll the data
            poll_length = 0.1  # [s]
            poll_timeout = 500  # [ms]
            poll_flags = 0
            poll_return_flat_dict = True
            data = self.daq.poll(poll_length, poll_timeout,
                                poll_flags, poll_return_flat_dict)
            datas.append(data)

        s = 0
        cnt = 0
        for data in datas:
            sample = data[self.boxcar_sample_path]

            # When using API Level 4 (or higher) poll() returns both the 'value' and
            # 'timestamp' of the node. These are two vectors of the same length;
            # which consist of (timestamp, value) pairs.
            boxcar_value = sample["value"]
            boxcar_timestamp = sample["timestamp"]
            # boxcar_periods_value = data[boxcar_periods_path]["value"]
            # boxcar_periods_timestamp = data[boxcar_periods_path]["timestamp"]
            s = s + np.sum(boxcar_value)
            cnt = cnt + np.size(boxcar_value)


        val = s/cnt
        print(f"Total boxcar sample count is {cnt}.")
        print(f"Measured average boxcar amplitude is {val:.5e} V.")
        return val

    def init_demodulator(self):
        pass

    def get_demodulator_value(self):
        pass