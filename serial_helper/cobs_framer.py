# -*- coding: utf-8 -*-

"""cobs_framer.py:
The serial interface only provides a packet-less stream to read and write data.
Directly parsing a stream into structured data poses many difficulties for the parser.
Thus, for most applications, the stream must be framed to effectively parse protocols running on that interface.

There're a lot of algorithms to frame a stream, one efficient algorithm is the COBS algorithm.

One classical approach to frame a binary stream is by using a special byte, 
such as 0x00 as an indicator of frame boundaries.
However, this approach limits the data range that can be transmitted.
Both ends must make sure that no 0x00 byte is accidentally put into the stream content.
This can be easily achieved if the stream only transmits ASCII chars, but if we want to transmit binary data such
as ADC sampling buffer or a picture through the stream, we cannot directly put the data in the stream because these
binary data may contain 0x00 byte and accidentally end the data frame, causing a malformed frame.

COBS is short for Consistent Overhead Byte Stuffing. The algorithm encodes a packet of bytes (range from 0x00 to 0xFF) 
into a new packet of bytes that is slightly longer but does not contain a given byte, such as the 0x00 byte. 
Then we can safely use that byte as a packet boundary marker, without the concern that the packet may be incorrectly cut 
in the middle.

This package provides the COBSFramer class to read from a SerialManager and frame the messages.
The framed packets are stored temporarily in a queue to be consumed by protocol parsers.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231123"

# std libs
import logging
import time
from queue import Queue, Empty
from threading import Thread
from typing import Callable, Optional
# third-party libs
from cobs import cobs
# this package
from .serial_manager import SerialManager

# Configure logging
lg = logging.getLogger(__name__)


class COBSFramer():
    def __init__(self, ser_mgr: SerialManager) -> None:
        self.ser_mgr = ser_mgr
        self.stream_content = b''
        self.received_packets: Queue[bytes] = Queue()
        self.framer_thread_running = False
        self.framer_thread = Thread(target=self.framer_task)

    def start(self):
        lg.info("Starting COBSFramer")
        self.ser_mgr.start()
        lg.info("Starting Framer reading thread")
        self.framer_thread_running = True
        self.framer_thread.start()
        lg.info("COBSFramer started")

    def stop(self):
        lg.info("Gracefully shutting down COBSFramer")
        lg.info("Waiting for Framer reading thread to finish")
        self.framer_thread_running = False
        self.framer_thread.join()
        self.ser_mgr.stop()
        lg.info("COBSFramer shutdown.")

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
        encoded_packets = self.stream_content.split(b'\x00')
        for i in range(len(encoded_packets)-1):
            if encoded_packets[i]:
                decoded_packet = cobs.decode(encoded_packets[i])
                self.received_packets.put(decoded_packet)
        self.stream_content = encoded_packets[-1]

    def send_frame(self, msg: bytes):
        encoded_packet = cobs.encode(msg)
        packet = encoded_packet + b'\x00'
        self.ser_mgr.send(packet)

    def receive_frame(self, timeout: float | None = None):
        try:
            item = self.received_packets.get(timeout=timeout)
            self.received_packets.task_done()
            return item
        except Empty:
            return None
