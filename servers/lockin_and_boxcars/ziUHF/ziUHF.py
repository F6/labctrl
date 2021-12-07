# -*- coding: utf-8 -*-

"""ziUHF.py:
This module provides methods to communicate with a remote
Zurich Instruments UHF 600MHz Lock-in Amplifier Data Server
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

import time
import numpy as np
import zhinst.utils

cfg = {
    "DeviceID": "dev2461",
    "APILevel": 6,
    "ServerHost": "localhost",
    "ServerPort": 8004,
    "SamplePath": "/dev2461/boxcars/0/sample"
}


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
            cfg["DeviceID"], cfg["APILevel"], server_host=cfg["ServerHost"], server_port=cfg["ServerPort"]
        )
        zhinst.utils.api_server_version_check(self.daq)


    def get_value(self, averaging_time=0.1):
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
            sample = data[cfg["SamplePath"]]
            value = sample["value"]
            s = s + np.sum(value)
            cnt = cnt + np.size(value)

        val = s/cnt
        # print(f"Total sample count is {cnt}.")
        # print(f"Measured average amplitude is {val:.5e} V.")
        return val

uhf = ziUHF()
uhf.init_session()