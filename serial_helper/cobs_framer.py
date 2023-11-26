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
        self.frame_id = 1
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
                try:
                    decoded_packet = cobs.decode(encoded_packets[i])
                    self.received_packets.put(decoded_packet)
                except cobs.DecodeError as e:
                    lg.error("Malformed data encountered when decoding {} with COBS decoder, error: {}.".format(
                        encoded_packets[i], e))
        self.stream_content = encoded_packets[-1]

    def send_frame(self, msg: bytes, timeout: float | None = None):
        encoded_packet = cobs.encode(msg)
        packet = encoded_packet + b'\x00'
        self.ser_mgr.send(packet, message_id=self.frame_id)
        # wait for sending confirmation
        t_send, msg_id = self.ser_mgr.sent_id_queue.get(timeout=timeout)
        self.ser_mgr.sent_id_queue.task_done()
        if msg_id == self.frame_id:
            pass
        else:
            lg.warning(
                "Got other msg_id from sent_id_queue, are there other threads writing?")
            lg.warning(
                "When using a framer, it is recommanded to manage all serial writes with the framer to avoid data corruption."
            )
        self.frame_id += 1
        return len(msg)

    def receive_frame(self, timeout: float | None = None):
        try:
            item = self.received_packets.get(timeout=timeout)
            self.received_packets.task_done()
            return item
        except Empty:
            return None

    def clean_up(self):
        """
        Empties packets buffer and stream buffer.
        Useful if the user needs to get the latest message and does not care about messages in the middle.
        This function may block forever and fail, because it empties the queue by removing items one by one, which is a thread-safe method but if the other ends are putting stuff in the queue faster than while True, the loop will never end. However, if while True fails to handle so many items, the program cannot work properly anyway so we don't need to concern about this.
        """
        lg.info("Cleaning up framer buffer.")
        while True:
            try:
                _ = self.received_packets.get(block=False)
                self.received_packets.task_done()
            except Empty:
                break
        self.stream_content = b''
        lg.info("Framer buffer is cleaned.")
