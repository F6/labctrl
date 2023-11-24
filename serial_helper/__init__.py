# -*- coding: utf-8 -*-

"""serial_helper:
This module provides some useful tools for developing serial port protocols and APIs.

SerialMocker is provided to mock a real serial device for testing.
SerialManager is provided to buffer serial IO in real-time and gracefully handle unexpected disconnection/reconnection.
SerialProtocol is provided to parse stream-based serial IO into structured data, and serialize structured data to send.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

import logging

from .serial_mocker import SerialMocker
from .serial_manager import SerialManager
from .cobs_framer import COBSFramer
from .pattern_framer import PatternFramer

lg = logging.getLogger(__name__)
lg.debug("Imported serial_helper")
