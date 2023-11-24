# -*- coding: utf-8 -*-

"""pattern_framer.py:
The serial interface only provides a packet-less stream to read and write data.
Directly parsing a stream into structured data poses many difficulties for the parser.
Thus, for most applications, the stream must be framed to effectively parse protocols running on that interface.

One classical approach to frame a binary stream is by using a special byte, 
such as 0x00 as an indicator of frame boundaries.
However, this approach limits the data range that can be transmitted.
Both ends must make sure that no 0x00 byte is accidentally put into the stream content.
This can be easily achieved if the stream only transmits ASCII chars, but if we want to transmit binary data such
as ADC sampling buffer or a picture through the stream, we cannot directly put the data in the stream because these
binary data may contain 0x00 byte and accidentally end the data frame, causing a malformed frame.

To mitigate this problem, one can use a pattern, i.e. a sequence of bytes, as the frame boundary indicator.
By using a pattern, it is much less likely to encounter the same pattern in normal data.
The longer the pattern, the safer the framing algorithm gets, but the overhead also increases.
Normally, using a random pattern length of 8 is safe enough for most cases: (1/256)^8 = 1/2^64 ~ 5e-20

In the long run, even the rarest event, of possiblility as small as 5e-20, can be encountered.
Thus, to completely eliminate the problem, the packet length is appended after the packet boundary pattern (or before the start of every packet).
When the packet is accidentally framed in the middle, the framer at both sides can identify the error because the length will not match.
And the framer can wait for the next boundary indicator pattern to see if this mismatch is caused by normal data or a data corruption.

This package provides the PatternFramer class to read from a SerialManager and frame the messages.
The framed packets are stored temporarily in a queue to be consumed by protocol parsers.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231123"

# std libs
import logging
import time
import struct
from queue import Queue, Empty
from threading import Thread
from typing import Callable, Optional
# third-party libs

# this package
from .serial_manager import SerialManager

# Configure logging
lg = logging.getLogger(__name__)


class PatternFramer():
    def __init__(self, ser_mgr: SerialManager, pattern: bytes) -> None:
        self.ser_mgr = ser_mgr
        self.pattern = pattern
        self.pattern_size = len(pattern)
        # A message length information is prepended to the start of every message
        # By default, 2 bytes are used, so the message length can range from 0 - 65535 bytes.
        self.msg_len_size = 2
        self.msg_len_fmt = '>1H'
        self.stream_content = b''
        self.received_packets: Queue[bytes] = Queue()
        self.framer_thread_running = False
        self.framer_thread = Thread(target=self.framer_task)

    def start(self):
        lg.info("Starting PatternFramer")
        self.ser_mgr.start()
        self.framer_thread_running = True
        self.framer_thread.start()
        lg.info("PatternFramer started")

    def stop(self):
        lg.info("Gracefully shutting down PatternFramer")
        self.framer_thread_running = False
        self.framer_thread.join()
        self.ser_mgr.stop()
        lg.info("PatternFramer shutdown.")

    def framer_task(self):
        while self.framer_thread_running:
            try:
                _, msg = self.ser_mgr.receive(timeout=1.0)
                if msg:
                    self.stream_content += msg
                    self.__handle_new_message()
            except Empty:
                pass

    def __handle_new_message(self):
        # this will not be empty so accessing by index -1 is safe.
        packets = self.stream_content.split(self.pattern)
        for i in range(len(packets)-1):
            if packets[i]: # ignore empty packets
                packet = packets[i][self.msg_len_size:]
                packet_len_bytes = packets[i][:self.msg_len_size]
                packet_len = struct.unpack(self.msg_len_fmt, packet_len_bytes)
                if packet_len == len(packet):
                    # if the packet size matches the content of packet len bytes
                    self.received_packets.put(packet)
                else:
                    lg.warning("Silently discarding a packet because of a length mismatch.")
                    lg.warning("Discarded: {}".format(packet))
                    # [TODO]: check if packet + self.pattern + packets[i+1] matches the length
                    #  and if mismatch, check if packet + self.pattern + packets[i+1] 
                    #   + self.pattern + packets[i+2] matches the length
                    #  and if mismatch, check if ... matches the length, until the end of packets.
        self.stream_content = packets[-1]

    def send_frame(self, msg: bytes):
        msg_len = len(msg)
        msg_len_bytes = struct.pack(self.msg_len_fmt, msg_len)
        assert self.msg_len_size == len(msg_len_bytes)
        packet = msg_len_bytes + msg + self.pattern
        self.ser_mgr.send(packet)

    def receive_frame(self, timeout: float | None = None):
        try:
            item = self.received_packets.get(timeout=timeout)
            self.received_packets.task_done()
            return item
        except Empty:
            return None
