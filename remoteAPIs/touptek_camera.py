# -*- coding: utf-8 -*-

"""touptek_camera.py:
This module provides methods to communicate with a remote
ToupTek camera server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


import requests
from .configs import toupcam_base_address
import base64
import numpy as np

class RemoteToupCamConnectionError(Exception):
    """Cannot connect to remote ToupCam"""
    pass

class RemoteToupCamSyncFailure(Exception):
    """Lost sync and cannot be recovered"""
    pass

def remote_ToupCam_test_online(max_retry=1):
    for i in range(max_retry):
        try:
            response = requests.get(toupcam_base_address)
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError

def remote_ToupCam_open(max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                toupcam_base_address + "open")
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError


def remote_ToupCam_close(max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                toupcam_base_address + "close")
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError

def remote_ToupCam_trig(max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                toupcam_base_address + "trig")
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError


def remote_ToupCam_get_signal(siglower, sigupper, reflower, refupper, max_retry=3):
    b = '{} {} {} {}'.format(siglower, sigupper, reflower, refupper)
    for i in range(max_retry):
        try:
            response = requests.get(
                toupcam_base_address + "gs/{}".format(b))
            rc = response.content.decode()
            if rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                r = base64.decodebytes(response.content)
                q = np.frombuffer(r, dtype=np.uint32)
                sig = np.array(q[:len(q)//2], dtype=np.int64)
                ref = np.array(q[len(q)//2:], dtype=np.int64)
                return sig, ref
                
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError


def remote_ToupCam_settrigmode(max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                toupcam_base_address + "settrig")
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError


def remote_ToupCam_setvidmode(max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                toupcam_base_address + "setvid")
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError


def remote_ToupCam_setExposureTime(t:int, max_retry=3):
    for i in range(max_retry):
        try:
            response = requests.get(
                toupcam_base_address + "t/{t:.0f}".format(t=t))
            rc = response.content.decode()
            if rc.startswith('[OK]'):
                return rc
            elif rc.startswith('[SyncError]'):
                raise RemoteToupCamSyncFailure
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            print(err)

    print("Error: Cannot connect to remote ToupCam, exceeded max retry {mr}".format(
        mr=max_retry))
    raise RemoteToupCamConnectionError