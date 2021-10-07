# -*- coding: utf-8 -*-

"""photodiode.py:
This module provides methods to communicate with a remote 
photodiode server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


import requests
from .configs import PD_base_address
import base64
import numpy as np

class RemotePDConnectionError(Exception):
    """Cannot connect to remote CCD"""
    pass

class RemotePDSyncFailure(Exception):
    """Lost sync and cannot be recovered"""
    pass


def remote_PD_take_signal(exposure_time, max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                PD_base_address + "takesignal/{exposure_time}".format(exposure_time=exposure_time))
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote PD, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemotePDConnectionError


def remote_PD_read_signal(max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                PD_base_address + "readsignal")
            rc = response.content.decode()
            if rc.startswith('[Error]'):
                raise RemotePDSyncFailure
            else:
                r = base64.decodebytes(response.content)
                q = np.frombuffer(r, dtype=np.float32)
                return q
                
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote PD, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemotePDConnectionError
