# -*- coding: utf-8 -*-

"""linear_stage.py:
This module provides methods to communicate with a remote 
linear stage server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


import requests
from .configs import ir_stage_base_address

class RemoteStageConnectionError(Exception):
    """Cannot connect to remote CCD"""
    pass


def remote_stage_online(max_retry=1):
    """Tests if the remote stage server is online.
    Does not test if the remote server actually works, however."""
    for i in range(max_retry):
        try:
            apicall = ir_stage_base_address
            response = requests.get(apicall)
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            else:
                print(rc)
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)
    print("Error: Cannot connect to remote stage, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteStageConnectionError


def remote_stage_moveabs(pos, max_retry=3):
    for i in range(max_retry):
        try:
            apicall = ir_stage_base_address + \
                    'moveabs/{:.3f}'.format(pos)
            response = requests.get(apicall)
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            else:
                print(rc)
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote stage, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteStageConnectionError

