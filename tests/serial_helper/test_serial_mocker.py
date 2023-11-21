
import unittest

import struct
import time
import logging

from serial_helper import SerialMocker
from logging_helper import TestingLogFormatter


lg = logging.getLogger("serial_helper")
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(TestingLogFormatter())
lg.addHandler(ch)


class TestSerialMocker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lg.info("Constructing response maps")
        my_device_response: dict[bytes, bytes] = dict()
        my_device_response[b'foo'] = b'bar'
        my_device_response[b'hello?'] = b'world!!!'
        my_device_response[struct.pack(
            '6b', *(1, 1, 4, 5, 1, 4))] = struct.pack('7b', *(1, 9, 1, 9, 8, 1, 0))
        lg.info("Response Map: {}".format(my_device_response))
        lg.info("Construction response generator")

        def r(b: bytes) -> bytes:
            if b == b'PANZER':
                return b'CHEAT ACTIVATED.'
            if b'echo' in b:
                return b
            return b''
        lg.info("Constructing SerialMocker object.")
        cls.ser = SerialMocker("COM1", timeout=1, baudrate=115200,
                               response_map=my_device_response,
                               mock_stream_content=bytes(range(256)), mock_stream_bps=0,
                               response_generator=r)

    @classmethod
    def tearDownClass(cls):
        lg.info("Shutting down the SerialMocker")
        cls.ser.close()

    def test_write(self):
        lg.info("Writing 11520 bytes, this should take 0.8 second")
        t0 = time.time()
        lg.info("Time started: {}".format(t0))
        result = self.ser.write(b'0' * 11520)
        t1 = time.time()
        lg.info("Time finished: {}, {} seconds elapsed, {} bytes written".format(
            t1, t1-t0, result))
        self.assertEqual(result, 11520)
        w = self.ser.in_waiting
        lg.info("Nothing should be in_waiting at present: {}".format(w))
        self.assertEqual(w, 0)
        i = self.ser.to_read_queue.qsize()
        lg.info("Nothing should be in the to_read_queue at present: {}".format(i))
        self.assertEqual(i, 0)

    def test_response_map(self):
        lg.info("Writing command defined in my_device_response 'foo'")
        self.ser.write(b'foo')
        time.sleep(0.1)
        lg.info("Now in_waiting: {}".format(self.ser.in_waiting))
        lg.info("Now actually in queue: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info("Try to read all bytes")
        result = self.ser.read(self.ser.in_waiting)
        lg.info("Read result: {}".format(result))
        self.assertEqual(result, b'bar')

    def test_response_map_binary_input(self):
        lg.info("Writing command defined in my_device_response : 0x(1, 1, 4, 5, 1, 4)")
        self.ser.write(b'\x01\x01\x04\x05\x01\x04')
        time.sleep(0.1)
        lg.info("Now in_waiting: {}".format(self.ser.in_waiting))
        lg.info("Now actually in queue: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info("Try to read all bytes")
        result = self.ser.read(self.ser.in_waiting)
        lg.info("Read result: {}".format(result))
        self.assertEqual(result, b'\x01\x09\x01\x09\x08\x01\x00')

    def test_response_map_multiple_write(self):
        lg.info("Nothing should be in_waiting at present: {}".format(
            self.ser.in_waiting))
        lg.info("Nothing should be in the to_read_queue at present: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info("Writing command defined in my_device_response 'hello?' three times.")
        for _ in range(3):
            self.ser.write(b'hello?')
        time.sleep(0.1)
        lg.info("Now in_waiting: {}".format(self.ser.in_waiting))
        lg.info("Now actually in queue: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info("Try to read all bytes")
        result = self.ser.read(self.ser.in_waiting)
        lg.info("Read result: {}".format(result))
        self.assertEqual(result, b'world!!!world!!!world!!!')

    def test_mock_stream(self):
        lg.info("Nothing should be in_waiting at present: {}".format(
            self.ser.in_waiting))
        lg.info("Nothing should be in the to_read_queue at present: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info(
            "Starting mocked stream! Expecting 9600 bits per second (9600 bytes per 8 seconds)")
        self.ser.mock_stream_bps = 9600
        lg.info("Sleeping for 1 second...")
        time.sleep(1)
        lg.info("Expecting around {} bytes in_waiting: {}".format(
            9600/8, self.ser.in_waiting))
        lg.info("Calling read_all to clear queue")
        result = self.ser.read_all()
        lg.info("Read_all result: {} bytes read, first 16 bytes: {}".format(
            len(result), result[:16]))
        lg.info("Calling read_all to test speed in 10 seconds...")
        t0 = time.time()
        bytes_read = 0
        for _ in range(10):
            time.sleep(1)
            result = self.ser.read_all()
            bytes_read += len(result)
            t1 = time.time()
            lg.info("Got {} bytes, total={} bytes, {} seconds elapsed".format(
                len(result), bytes_read, t1-t0))
        lg.info("Average: {} bps in 10 seconds".format(bytes_read*8/(t1-t0)))
        lg.info("Stopping mocked stream and clearing remaining bytes in queue")
        self.ser.mock_stream_bps = 0
        time.sleep(0.1)
        result = self.ser.read_all()
        lg.info("{} bytes discarded".format(len(result)))
        lg.info("Nothing should be in_waiting at present: {}".format(
            self.ser.in_waiting))
        lg.info("Nothing should be in the to_read_queue at present: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info(
            "to_read_queue should stop grow now, waiting for 1 second to confirm it...")
        lg.info("Nothing should be in_waiting at present: {}".format(
            self.ser.in_waiting))
        lg.info("Nothing should be in the to_read_queue at present: {}".format(
            self.ser.to_read_queue.qsize()))

    def test_mock_stream_fast(self):
        lg.info(
            "Starting mocked stream! Expecting 115200 bits per second (115200 bytes per 8 seconds)")
        self.ser.mock_stream_bps = 115200
        lg.info("Sleeping for 1 second...")
        time.sleep(1)
        lg.info("Expecting around {} bytes in_waiting: {}".format(
            115200/8, self.ser.in_waiting))
        lg.info("Calling read_all to clear queue")
        result = self.ser.read_all()
        lg.info("Read_all result: {} bytes read, first 16 bytes: {}".format(
            len(result), result[:16]))
        lg.info("Calling read_all to test speed in 10 seconds...")
        t0 = time.time()
        bytes_read = 0
        for _ in range(10):
            time.sleep(1)
            result = self.ser.read_all()
            bytes_read += len(result)
            t1 = time.time()
            lg.info("Got {} bytes, total={} bytes, {} seconds elapsed".format(
                len(result), bytes_read, t1-t0))
        lg.info("Average: {} bps in 10 seconds".format(bytes_read*8/(t1-t0)))
        lg.info("Stopping mocked stream and clearing remaining bytes in queue")
        self.ser.mock_stream_bps = 0
        time.sleep(0.1)
        result = self.ser.read_all()
        lg.info("{} bytes discarded".format(len(result)))
        lg.info("Nothing should be in_waiting at present: {}".format(
            self.ser.in_waiting))
        lg.info("Nothing should be in the to_read_queue at present: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info(
            "to_read_queue should stop grow now, waiting for 1 second to confirm it...")
        lg.info("Nothing should be in_waiting at present: {}".format(
            self.ser.in_waiting))
        lg.info("Nothing should be in the to_read_queue at present: {}".format(
            self.ser.to_read_queue.qsize()))

    def test_response_generator(self):
        lg.info("Testing response generator.")
        lg.info("Writing PANZER to serial.")
        self.ser.write(b'PANZER')
        time.sleep(0.1)
        lg.info("Now in_waiting: {}".format(self.ser.in_waiting))
        lg.info("Now actually in queue: {}".format(
            self.ser.to_read_queue.qsize()))
        lg.info("Try to read all bytes")
        result = self.ser.read(self.ser.in_waiting)
        lg.info("Read result: {}".format(result))
        self.assertEqual(result, b'CHEAT ACTIVATED.')
        for i in range(10):
            lg.info("Writing echo commands to serial.")
            self.ser.write('echo {}'.format(i).encode())
            time.sleep(0.1)
            lg.info("Now in_waiting: {}".format(self.ser.in_waiting))
            lg.info("Now actually in queue: {}".format(
                self.ser.to_read_queue.qsize()))
            lg.info("Try to read all bytes")
            result = self.ser.read(self.ser.in_waiting)
            lg.info("Read result: {}".format(result))
            self.assertEqual(result, 'echo {}'.format(i).encode())

if __name__ == '__main__':
    unittest.main()
