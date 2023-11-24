# -*- coding: utf-8 -*-

"""test_cobs_framer.py:
This test module tests the COBSFramer class by a serial COBS encoder-decoder-echoer.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231123"

import unittest

import struct
import time
import logging

from cobs import cobs

from serial_helper import SerialManager, SerialMocker, COBSFramer
from logging_helper import TestingLogFormatter


# configure root logger to output all logs to stdout
lg = logging.getLogger()
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(TestingLogFormatter())
lg.addHandler(ch)
# configure logger for this module.
lg = logging.getLogger(__name__)


class TestCOBSFramer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lg.info("Constructing COBS debugging echoer")
        def echoer(b:bytes) -> bytes:
            lg.debug("COBS Echoer received: {}".format(b))
            return b
        lg.info("Constructing echoer SerialMocker object.")
        cls.ser = SerialMocker("COM1", timeout=1, baudrate=115200,
                               response_generator=echoer)
        cls.mgr = SerialManager("COM1", baudrate=115200, timeout=1)
        # Replace the mgr.ser with a mocking ser!
        cls.mgr.ser = cls.ser
        cls.framer = COBSFramer(cls.mgr)
        cls.framer.start()

    @classmethod
    def tearDownClass(cls):
        lg.info("Stopping SerialManager service")
        cls.framer.stop()

    def test_send_frame(self):
        lg.debug("==== START test_send_frame ====")
        lg.info("Sending b'Hello'")
        self.framer.send_frame(b'Hello')
        r = self.framer.receive_frame(timeout=0.2)
        self.assertEqual(r, b'Hello')
        lg.info("Received: {}".format(r))
        lg.info("Sending b'Hello\\x00World!'")
        self.framer.send_frame(b'Hello\x00World!')
        r = self.framer.receive_frame(timeout=0.2)
        lg.info("Received: {}".format(r))
        self.assertEqual(r, b'Hello\x00World!')
    
    def test_seperate_multiple_frame_in_stream(self):
        lg.debug("==== START test_seperate_multiple_frame_in_stream ====")
        lg.info("Sending 3 frames directly with serial manager.")
        lg.info("These frames are sticked together in the stream.")
        lg.info("The framer should be able to seperate the stream into 3 packets.")
        self.mgr.send(b'\x06Hello\x07World!\x00\x06Hello\x07World!\x00\x06Hello\x07World!\x00')
        for i in range(3):
            r = self.framer.receive_frame(timeout=0.2)
            lg.info("Received: {}".format(r))
            self.assertEqual(r, b'Hello\x00World!')
        r = self.framer.receive_frame(timeout=0.2)
        lg.info("Received: {}".format(r))
        self.assertEqual(r, None)

    def test_combine_seperated_frame_in_stream(self):
        lg.debug("==== START test_combine_seperated_frame_in_stream ====")
        lg.info("Sending 1 frame with serial manager, but seperated in two messages.")
        lg.info("The framer should be able to combine it into one packet.")
        self.mgr.send(b'\x06Hello\x07')
        self.mgr.send(b'World!\x00')
        r = self.framer.receive_frame(timeout=0.2)
        lg.info("Received: {}".format(r))
        self.assertEqual(r, b'Hello\x00World!')
    
    def test_half_sticked_message(self):
        lg.debug("==== START test_half_sticked_message ====")
        lg.info("Sending 2 frames with serial manager, but seperated in non-boundary byte.")
        lg.info("The framer should be able to combine it and seperate into two packets.")
        self.mgr.send(b'\x06Hello\x07')
        self.mgr.send(b'World!\x00\x06Hello\x07World!\x00')
        r = self.framer.receive_frame(timeout=0.2)
        lg.info("Received: {}".format(r))
        self.assertEqual(r, b'Hello\x00World!')
        r = self.framer.receive_frame(timeout=0.2)
        lg.info("Received: {}".format(r))
        self.assertEqual(r, b'Hello\x00World!')
        self.mgr.send(b'\x06Hello\x07World!\x00\x06Hello')
        self.mgr.send(b'\x07World!\x00')
        r = self.framer.receive_frame(timeout=0.2)
        lg.info("Received: {}".format(r))
        self.assertEqual(r, b'Hello\x00World!')
        r = self.framer.receive_frame(timeout=0.2)
        lg.info("Received: {}".format(r))
        self.assertEqual(r, b'Hello\x00World!')
