# -*- coding: utf-8 -*-

"""ETHGASN.py:
This module implements class ETHGASN to access
Dongguan Bopai Tech ETH_GAS_N motion controllers

The controller output is connected to a Yaskawa SGDV-1R6A05A
servo driver. The servo driver needs seperate setting to work, please 
refer to the corresponding doc.

Only the axis 1 is controlled and only 1 card is installed.
For more complicated controls, use functions in Multicard.py
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220106"

import time
import MultiCard as lib

