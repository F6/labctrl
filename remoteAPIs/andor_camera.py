# -*- coding: utf-8 -*-

"""andor_camera.py:
This module provides methods to communicate with a remote Andor SOLIS
camera server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


import requests
from .configs import CCD_base_address
import base64
import numpy as np

class RemoteCCDConnectionError(Exception):
    """Cannot connect to remote CCD"""
    pass

class RemoteCCDSyncFailure(Exception):
    """Lost sync and cannot be recovered"""
    pass

def remote_CCD_test_online(max_retry=1):
    for i in range(max_retry):
        try:
            response = requests.get(CCD_base_address)
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteCCDSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote CCD, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteCCDConnectionError

def remote_CCD_take_signal(sid, max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                CCD_base_address + "takesignal/{sid}".format(sid=sid))
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteCCDSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote CCD, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteCCDConnectionError


def remote_CCD_clear_list(max_retry):
    for i in range(max_retry):
        try:
            response = requests.get(
                CCD_base_address + "clearsiglist")
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote CCD, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteCCDConnectionError


def remote_CCD_convert_latest(converted_path, max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                CCD_base_address + "convertlatest/{}".format(converted_path))
            rc = response.content.decode()
            if rc.startswith('[SyncError]'):
                raise RemoteCCDSyncFailure
            else:
                r = base64.decodebytes(response.content)
                q = np.frombuffer(r, dtype=np.float32)
                q = np.int64(q)
                return q
                
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote CCD, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteCCDConnectionError


def remote_CCD_check_signal(sid, max_retry):
    for i in range(max_retry):
        try:
            response = requests.get(
                CCD_base_address + "signaltaken/{sid}".format(sid=sid))
            rc = response.content.decode()
            if rc.startswith('[True]'):
                return True
            elif rc.startswith('[False]'):
                return False
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote CCD, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteCCDConnectionError