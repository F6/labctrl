# -*- coding: utf-8 -*-

"""
utils.py:
auxiliary functions, temporarily collected here, probably moving to other modules later.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221115"

import requests
import numpy as np


def calculate_dx(value: float, unit: str, multiples: float, direction: str):
    """
    Converts working unit to standard internal unit mm
     so we can send currect values to remote controller
    """
    # Basic coefficient (mm/degree)
    c = 1.0

    if unit == "radian":  # pi radian = 180 degree
        dx = value * 180 / np.pi
    elif unit == "degree":
        dx = value
    elif unit == "minute":
        dx = value / 60
    elif unit == "second":
        dx = value / 3600
    else:
        pass

    if direction == "Positive":
        pass
    elif direction == "Negative":
        dx = -dx
    else:
        pass

    dx = dx * c * multiples

    return dx


def eval_float(f):
    try:
        f = float(f)
        return f
    except Exception as e:
        print("Non-float number inputed")
        return 0.0


def eval_int(i):
    try:
        i = int(i)
        return i
    except Exception as e:
        print("Non-integer number inputed")
        return 0


def ignore_connection_error(func):
    def ret():
        try:
            func()
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return ret
