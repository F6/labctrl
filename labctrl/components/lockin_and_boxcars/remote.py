# -*- coding: utf-8 -*-

"""remote.py:
This module provides methods to communicate with a remote 
Generic Boxcar Controller.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220624"


import requests
import json
import base64
import numpy as np


class RemoteBoxcarController():
    def __init__(self, config, max_retry=3) -> None:
        self.host = config["Host"]
        self.port = config["Port"]
        self.max_retry = max_retry
        self.api_url = 'http://{host}:{port}/'.format(
            host=self.host, port=self.port)

    def apicall(self, command):
        for i in range(self.max_retry):
            try:
                apicall = self.api_url + command
                response = requests.get(apicall)
                rc = response.content.decode()
                return json.loads(rc)
            except requests.exceptions.ConnectionError as err:
                print(err)
        print("Error: Cannot connect to remote, exceeded max retry {mr}".format(
            mr=self.max_retry))
        raise requests.exceptions.ConnectionError

    def online(self):
        """Tests if the remote stage server is online.
        Does not test if the remote server actually works, however."""
        return self.apicall('')

    def get_boxcar_data(self):
        boxcar_data = self.apicall('getBoxcarData')
        boxcar_data = np.frombuffer(base64.b64decode(
            boxcar_data["result"]), dtype=np.float64)
        return boxcar_data

    def get_PWA_data(self):
        PWA_data = self.apicall('getPWAData')
        PWA_data = np.frombuffer(base64.b64decode(
            PWA_data["result"]), dtype=np.float64)
        return PWA_data

    def set_delay_background_sampling(self, delay):
        return self.apicall('setDelayBackgroundSampling/{delay}'.format(delay=delay))

    def set_delay_integrate(self, delay):
        return self.apicall('setDelayIntegrate/{delay}'.format(delay=delay))

    def set_delay_hold(self, delay):
        return self.apicall('setDelayHold/{delay}'.format(delay=delay))

    def set_delay_signal_sampling(self, delay):
        return self.apicall('setDelaySignalSampling/{delay}'.format(delay=delay))

    def set_delay_reset(self, delay):
        return self.apicall('setDelayReset/{delay}'.format(delay=delay))

    def set_adc_sampling_interval(self, delay):
        return self.apicall('setADCSamplingInterval/{delay}'.format(delay=delay))

    def set_adc_sample_number(self, n_sample):
        return self.apicall('setADCSampleNumber/{n_sample}'.format(n_sample=n_sample))

    def set_working_mode(self, mode):
        return self.apicall('setWorkingMode/{mode}'.format(mode=mode))
