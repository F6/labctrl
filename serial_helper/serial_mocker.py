# -*- coding: utf-8 -*-

"""serial_mocker.py:
This module provides the SerialMocker class to mock a pySerial Serial object for testing other modules.

When implementing libraries for embeded devices, it is common to use the pyserial library to communicate with USB CDC 
VCP devices or RS232 devices.
We probably want to communicate with and manupulate the real device only after other library codes are working. 
Or we risk causing damage to real devices if the library codes went wrong.
Thus it is better to use a mock object, which responds to commands and streams data lke the real device, for testing 
library codes.

The SerialMocker object has similar methods with a Serial object.
It supports open, close, write, read and read_all methods.
These methods also block for an appropriate amount of time just like the real ports would do, to simulate low baudrate 
slow ports.
The .read supports timeouts like a real Serial object.
SerialMocker also mocks in_waiting, is_open member variable

Data returned from calling .read() comes from two sources: 
1. response map: 
Like a lot of serial devices, when you write a certein command to the device, it writes back a bunch of requested data. 
For mocking this behaviour, define the command and desired response in a dictionary and pass it to SerialMocker as 
response_map.
2. stream
Some serial devices, for example humidity sensors or temperature sensors, send data continuously to host port without 
any command. 
For mocking this behaviour, define the content of the stream as bytes and pass it to SerialMocker as 
mock_stream_content. 
To start the streaming, set mock_stream_bps to a positive value which is the average data rate of the stream. 
To stop the streaming, set mock_stream_bps to 0.

Note that SerialMocker does not raise the same exceptions as Serial, because it is not a real serial io.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

import logging
import time
import struct
from queue import Queue, Empty
from threading import Thread
from typing import Callable
# Configure logging
lg = logging.getLogger(__name__)


class SerialMockerError(Exception):
    pass


class SerialMocker:
    """
    Mocks the behaviour of a pySerial object for testing.
    """

    def __init__(self, port: str, timeout: float = 1.0, baudrate: int = 9600,
                 will_throw: bool = False, response_map: dict[bytes, bytes] = {},
                 mock_stream_content: bytes = b'', mock_stream_bps: int = 0,
                 response_generator: Callable[[bytes], bytes] = lambda x:b'') -> None:
        # ==== Basic serial port params, just like the real serial port. ====
        self.port = port
        self.timeout = timeout
        self.baudrate = baudrate
        # ==== Mocking params ====
        # if will_throw, raises exception when error happens. if not, ignores errors as if they don't exist.
        self.will_throw = will_throw
        # get a custom response when given pattern is wrote to device
        self.response_map = response_map
        # if it does not match anything in response_map, then the response_generator generates a response.
        # if no response is needed, return a b'' (empty byte) for it in response_generator to skip.
        self.response_generator = response_generator
        self.mock_response = False
        # mocks data streams sent from device.
        # feeds data from mock_stream_content at rate of mock_stream_bps to read_queue.
        # mock_stream_content is used cyclically
        # set mock_stream_bps to 0 to disable the stream.
        self.mock_stream_content = mock_stream_content
        self.mock_stream_content_len = len(self.mock_stream_content)
        self.mock_stream_bps = mock_stream_bps
        self.mock_stream = False
        # ==== Internal states ====
        self.bytes_written = 0
        self.bytes_read = 0
        # Bytes waiting in the buffer to be read
        self.in_waiting = 0
        self.to_read_queue = Queue()  # queue of int
        self.wrote_queue = Queue()  # queue of bytes
        # handles what data to return when read() called.
        self.mock_response_thread = Thread(target=self.mock_response_task)
        self.mock_stream_thread = Thread(target=self.mock_stream_task)
        self.open()
        lg.info("Created SerialMocker object, com_port: {}, timeout: {}, baudrate: {}".format(
            port, timeout, baudrate))

    def open(self):
        lg.info("Opening mocked serial connection")
        self.is_open = True
        self.mock_response = True
        self.mock_response_thread.start()
        self.mock_stream = True
        self.mock_stream_thread.start()

    def close(self):
        lg.info("Closing mocked serial connection")
        self.is_open = False
        self.mock_response = False
        self.mock_stream = False
        self.wrote_queue.put(None)
        self.mock_response_thread.join()
        self.mock_stream_thread.join()

    def write(self, to_write: bytes) -> int:
        """
        Simulates writing to a connected serial device.
        The function blocks for the theoratical time required to send these data with the given baudrate, assuming that 
        1byte=8bits and 1baud=1bit.
        If not will_throw, the write will succeed even if port is closed. Error will be logged but program will not be 
        interrupted.
        """
        bytes_to_write = len(to_write)
        lg.debug("Mocked write called, requested bytes to write: {}".format(
            bytes_to_write))
        if self.is_open:
            time_to_wait = bytes_to_write / self.baudrate * 8
            if time_to_wait > 0.02:
                # Only simulates blocking time that is longer than 20 ms, because for very short to_writes, time.sleep
                # cannot generate accurate delays due to OS implementations of sleep and thread scheduling.
                time.sleep(time_to_wait)
        else:
            lg.error(
                "Mocked WRITE called but mocked serial connection is closed!")
            if self.will_throw:
                raise SerialMockerError
        self.wrote_queue.put(to_write)
        self.bytes_written += bytes_to_write
        return bytes_to_write

    def read(self, bytes_to_read: int) -> bytes:
        """
        Simulates reading from pyserial driver buffer.
        The function returns bytes_to_read bytes immediately if there's enough bytes to read, blocks and wait for new 
        bytes until timeout if not enough bytes are in the to_read_queue.
        Bytes are added to the to_read_queue by mock_response_task and mock_stream_task.
        If not will_throw, the read will succeed even if the port is closed. Error will be logged but program will not 
        be interrupted. 
        However, if timeout is specified, SerialMockError will be raised if timeout happens, even if will_throw is 
        False, because in this case there's no way the function can return the required number of bytes and the error 
        cannot be ignored.
        """
        lg.debug("Mocked read called, requested bytes to read: {}".format(
            bytes_to_read))
        try:
            mocked_response = list()
            for _ in range(bytes_to_read):
                c = self.to_read_queue.get(
                    block=True, timeout=self.timeout).to_bytes()
                mocked_response.append(c)
                self.in_waiting -= 1
            mocked_response = b''.join(mocked_response)
        except Empty:
            raise SerialMockerError
        if self.is_open:
            pass
        else:
            lg.error(
                "Mocked READ called but mocked serial connection is closed!")
            if self.will_throw:
                raise SerialMockerError
        self.bytes_read += bytes_to_read
        return mocked_response

    def read_all(self):
        return self.read(self.in_waiting)

    def mock_response_task(self):
        while self.mock_response:
            wrote = self.wrote_queue.get()
            if wrote is None:
                break
            if wrote in self.response_map:
                # Match response_map first
                to_read = self.response_map[wrote]
            else:
                to_read = self.response_generator(wrote)
            if to_read:
                for c in to_read:
                    self.to_read_queue.put(c)
                    self.in_waiting += 1

    def mock_stream_task(self):
        i = 0
        t_prev = time.time()
        while self.mock_stream:
            if self.mock_stream_bps == 0:
                # if bps is set to 0, no need to calculate anything.
                # However, we will update t_prev to current time because if it is not updated, then the next time user
                # changes bps to a non-zero value, t_delta will be huge because it counted all time since last byte sent
                t_prev = time.time()
                time.sleep(0.01)
                continue
            # calculate how many bytes from stream to send to to_read_queue
            t_now = time.time()
            t_delta = t_now - t_prev
            n_bytes = int(self.mock_stream_bps * t_delta / 8)
            if n_bytes:
                # check if mock_stream_content is empty
                if self.mock_stream_content_len == 0:
                    raise SerialMockerError
                for _ in range(n_bytes):
                    # Fun fact:
                    #  In [0]: b'\x01\x02\x03\x04'[1]
                    #  Out[0]: 2
                    #  In [1]: b'\x01\x02\x03\x04'[1:2]
                    #  Out[1]: b'\x02'
                    self.to_read_queue.put(self.mock_stream_content[i])
                    i = (i + 1) % self.mock_stream_content_len
                    self.in_waiting += 1
                t_prev = t_now
            else:
                # if no bytes to send, t_prev does not need to be updated
                pass
