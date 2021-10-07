# -*- coding: utf-8 -*-

"""shutter.py:
This module provides methods to communicate with a remote 
shutter server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


import requests
from .configs import shutter_base_address


class RemoteShutterConnectionError(Exception):
    """Cannot connect to remote Shutter"""
    pass


def remote_shutter_set_state(state, max_retry=3):
    for i in range(max_retry):
        try:
            if state:
                response = requests.get(
                    shutter_base_address + "on/1")
            else:
                response = requests.get(
                    shutter_base_address + "off/1")
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            else:
                print(rc)
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote Shutter, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteShutterConnectionError
