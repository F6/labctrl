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
from threading import Thread

# import zhinst.utils
import zhinst.core

from circular_buffer import CircularBuffer

cfg = {
    "DeviceID": "dev2461",
    # "DeviceID": "dev2819",
    "APILevel": 6,
    # "ServerHost": "localhost",
    "ServerHost": "127.0.0.1",
    "ServerPort": 8004,
    "SamplePath": "/dev2461/boxcars/0/sample"
    # "SamplePath": "/dev2819/boxcars/1/sample",
    # "BackgroundSamplePath": "/dev2819/boxcars/1/sample"
}


class ziUHF:
    """Temporarily holds data from UHF device, also manages the API session from
    LabOne Data Server"""

    def __init__(self) -> None:
        self.daq = None
        self.device = None
        self.props = None
        self.poll_length = 0.1  # [s]
        self.poll_timeout = 500  # [ms]
        self.poll_flags = 0
        self.poll_return_flat_dict = True
        self.buffer = CircularBuffer(length=4096)
        self.init_session()
        self.sync_thread_running = True
        self.sync_thread = Thread(target=self.sync_task)
        self.sync_thread.start()


    def init_session(self) -> None:
        # Call a zhinst utility function that returns:
        # - an API session `daq` in order to communicate with devices via the data server.
        # - the device ID string that specifies the device branch in the server's node hierarchy.
        # - the device's discovery properties.
        # (self.daq, self.device, self.props) = zhinst.utils.create_api_session(
        #     cfg["DeviceID"], cfg["APILevel"], server_host=cfg["ServerHost"], server_port=cfg["ServerPort"]
        # )
        self.daq = zhinst.core.ziDAQServer('localhost', 8004, 6)

        # zhinst.utils.api_server_version_check(self.daq)
        self.daq.subscribe(cfg["SamplePath"])
        # self.daq.subscribe(cfg["BackgroundSamplePath"])

    def sync_task(self):
        while self.sync_thread_running:
            data = self.daq.poll(self.poll_length, self.poll_timeout,
                                 self.poll_flags, self.poll_return_flat_dict)
            try:
                sample = data[cfg["SamplePath"]]
                value = sample["value"]
                self.buffer.append_bulk(value)
            except KeyError as e:
                print("[ziUHF]: KeyError {}, {}, requred result not present in poll from DAQ, \
probably misconfigured SamplePath or node not subscribed".format(e, e.args))

    def get_new_data(self, sample_count: int = 1000, timeout: float = 30.0, keep_phase_period: int = 2):
        """
        Returns an array containing new samples of required sample count size.
        A timeout must be set to prevent freezing forever, if the device is accidentally 
        offline of misconfigured.
        A keep_phase_period param can be set when data phase is critical, for example if
        we are using a chopper to chop the signal into half frequency signal and background, 
        then the buffer will look like 'S B S B S B S B S B ...', 
        if get_new_data timing is randomized, then we will get random phase slices like 
        'S B S B S B' and 'B S B S B S', and we will lose track of which one is signal and
        which one is background.
        If a keep_phase_period param is set, then the istart will always be snapped to a
        latest grid point of grid size keep_phase_period, for example if keep_phase_period=8,
        then istart will always be one of 8, 16, 24, 32...
        """
        istart = self.buffer.current_data_index
        istart = istart // keep_phase_period + keep_phase_period
        istop = (istart + sample_count) % self.buffer.length
        tstart = time.time()
        while self.buffer.current_data_index < istop:
            time.sleep(0.01)
            tnow = time.time()
            if (tnow - tstart) > timeout:
                raise TimeoutError
        return self.buffer.get_slice(istart, istop)
    
    def get_value(self, sample_count: int = 1000, timeout: float = 30.0):
        """
        Same as get_new_data, but returns mean only
        """
        return np.mean(self.get_new_data(sample_count=sample_count, timeout=timeout))


uhf = ziUHF()
