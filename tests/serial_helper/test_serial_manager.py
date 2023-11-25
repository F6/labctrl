# -*- coding: utf-8 -*-

"""test_serial_manager.py:
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231123"

import unittest

import struct
import time
import logging

from serial_helper import SerialManager, SerialMocker
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


class TestSerialManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lg.info("Constructing response maps")
        my_device_response: dict[bytes, bytes] = dict()
        my_device_response[b'foo'] = b'bar'
        my_device_response[b'hello?'] = b'world!!!'
        my_device_response[struct.pack(
            '6b', *(1, 1, 4, 5, 1, 4))] = struct.pack('7b', *(1, 9, 1, 9, 8, 1, 0))
        lg.info("Response Map: {}".format(my_device_response))
        lg.info("Constructing SerialMocker object.")
        ser = SerialMocker("COM1", timeout=1, baudrate=115200,
                           response_map=my_device_response,
                           mock_stream_content=bytes(range(256)), mock_stream_bps=0,
                           )
        cls.mgr = SerialManager("COM1", baudrate=115200, timeout=1)
        # Replace the mgr.ser with a mocking ser!
        cls.mgr.ser = ser
        cls.mgr.start()

    @classmethod
    def tearDownClass(cls):
        lg.info("Stopping SerialManager service")
        cls.mgr.stop()

    def test_send(self):
        lg.debug("==== START test_send ====")
        lg.info(
            "Asynchronously writing 11520 bytes with id 888, this should be finished after 0.8 seconds")
        lg.info("Nothing should be in the sent_id_queue yet: {}".format(
            self.mgr.sent_id_queue.qsize()))
        t0 = time.time()
        lg.info("Time started: {}".format(t0))
        result = self.mgr.send(b'0' * 11520, message_id=888)
        lg.info("Message put to queue!")
        t1 = time.time()
        lg.info("Time: {}, {} seconds elapsed, {} bytes sent to queue.".format(
            t1, t1-t0, result))
        self.assertEqual(result, 11520)
        lg.info("Now waiting for message to be sent...")
        t2, result = self.mgr.sent_id_queue.get()
        t2 = t2/1e9
        lg.info("Got {} from sent_id_queue, {} seconds elapsed.".format(result, t2-t0))
        self.assertEqual(result, 888)

    def test_command_and_response(self):
        lg.debug("==== START test_command_and_responses ====")
        lg.info("Asynchronously writing command defined in my_device_response: 'foo'")
        self.mgr.send(b'foo', message_id=123)
        lg.info("Waiting for message to be sent...")
        t1, result = self.mgr.sent_id_queue.get()
        lg.info("Data wrote to serial port, time={}, id={}".format(t1, result))
        lg.info("Response should be in the received_queue now: {}".format(
            self.mgr.received_queue.qsize()))
        lg.info("Try to read response")
        t2, result = self.mgr.receive()
        lg.info("Read result: {}, received time: {}, response latency={}ns".format(
            result, t2, t2-t1))
        # device should response after command
        self.assertGreaterEqual(t2, t1)
        # device should response according to map
        self.assertEqual(result, b'bar')

    def test_command_and_response_binary(self):
        lg.debug("==== START test_command_and_response_binary ====")
        lg.info(
            "Asynchronously writing command defined in my_device_response: 0x(1, 1, 4, 5, 1, 4)")
        self.mgr.send(b'\x01\x01\x04\x05\x01\x04', message_id=123)
        lg.info("Waiting for message to be sent...")
        t1, result = self.mgr.sent_id_queue.get()
        lg.info("Data wrote to serial port, time={}, id={}".format(t1, result))
        lg.info("Response should be in the received_queue now: {}".format(
            self.mgr.received_queue.qsize()))
        lg.info("Try to read response")
        t2, result = self.mgr.receive()
        lg.info("Read result: {}, received time: {}, response latency={}ns".format(
            result, t2, t2-t1))
        # device should response after command
        self.assertGreaterEqual(t2, t1)
        # device should response according to map
        self.assertEqual(result, b'\x01\x09\x01\x09\x08\x01\x00')

    def test_command_and_response_multiple_write(self):
        lg.debug("==== START test_command_and_response_multiple_write ====")
        lg.info("Nothing should be in received_queue: {}".format(
            self.mgr.received_queue.qsize()))
        lg.info("Writing command defined in my_device_response 'hello?' 100 times.")
        t0 = time.time()
        lg.info("Time started: {}".format(t0))
        result = 0
        for i in range(99):
            result += self.mgr.send(b'hello?')
        # send last item with a sent_id to track the time sending finishes
        result += self.mgr.send(b'hello?', message_id=100)
        t1 = time.time()
        lg.info("Time: {}, {} seconds elapsed, {} bytes sent to queue.".format(
            t1, t1-t0, result))
        lg.info("Waiting for all items sent...")
        t2, sid = self.mgr.sent_id_queue.get()
        t2 = t2 / 1e9 # converts ns to s
        self.assertEqual(sid, 100)
        lg.info("All items sent! Time elapsed: {}, bps: {}".format(
            t2 - t0, result*8/(t2-t0)))
        lg.info("Receive until nothing in the received_queue")
        responses = []
        while self.mgr.received_queue.qsize():
            responses.append(self.mgr.receive())
        lg.info("Received: {} items.".format(len(responses)))
        response_stream = b''.join([i[1] for i in responses])
        self.assertEqual(response_stream, b'world!!!'*100)

    def test_receive_timeout(self):
        lg.debug("==== START test_receive_timeout ====")
        lg.info("Nothing should be in the received_queue now: {}".format(
            self.mgr.received_queue.qsize()))
        lg.info("Try to receive from empty received_queue with timeout 1.0 seconds")
        t2, result = self.mgr.receive(timeout=1.0)
        lg.info("Read result: {}, received time: {}".format(
            result, t2, t2))
        assert t2 is None
        assert result is None
    # [TODO] tests for streaming and multi-thread command and response.
