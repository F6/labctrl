# -*- coding: utf-8 -*-

"""monochromer.py:
This module provides methods to communicate with a remote 
monochromer server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"



import requests
from .configs import monochromer_base_address

class RemoteMonochromerConnectionError(Exception):
    """Cannot connect to remote Monochromer"""
    pass


def remote_monochromer_online(max_retry=1):
    """Tests if the remote server is online.
    Does not test if the remote server actually works, however."""
    for i in range(max_retry):
        try:
            apicall = monochromer_base_address
            response = requests.get(apicall)
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            else:
                print(rc)
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)
    print("Error: Cannot connect to remote monochromer, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteMonochromerConnectionError


def remote_monochromer_moveto(pos:int, max_retry=3)->str:
    for i in range(max_retry):
        try:
            apicall = monochromer_base_address + \
                    'moveto/{:.0f}'.format(pos)
            response = requests.get(apicall)
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            else:
                print(rc)
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote monochromer, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteMonochromerConnectionError


def remote_monochromer_get_position(max_retry:int=1) -> int:
    for i in range(max_retry):
        try:
            apicall = monochromer_base_address + 'getpos'
            response = requests.get(apicall)
            rc = response.content.decode()
            return int(rc)
        except requests.exceptions.ConnectionError as err:
            print(err)
    print("Error: Cannot connect to remote monochromer, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteMonochromerConnectionError

def remote_monochromer_stop(max_retry=1):
    for i in range(max_retry):
        try:
            apicall = monochromer_base_address + 'stop'
            response = requests.get(apicall)
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            else:
                print(rc)
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)
    print("Error: Cannot connect to remote monochromer, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteMonochromerConnectionError