# -*- coding: utf-8 -*-

"""serial_manager.py:
This module provides the SerialManager class to provide buffering and queueing of messages for serial port devices.
It also converts synchronous serial IO into asynchronous API that is easier for higher level applications such as stream
parsers to work on.

It is necessary to use a dedicated serial manager to buffer data because depending on OS implementations, pySerial has 
different input buffer sizes and output buffer sizes.

The buffer sizes are in general quite small, and most of the times it is hard-coded in the driver C library and there's 
no easy way to controll that.
Thus, for transmitting large amount of data, it is necessary to build a secondary buffer to clean the limited driver 
buffer in time to avoid data loss and corruption.

The driver input buffer also does not include a timestamp to indicate the time when a message is received, which is 
quite inconvenient for real-time controlling and other time-critical applications. 
So I also added a timestamp to each message received/sent, so the user can track the timeline of every message.

Note, despite that in most of the cases data sent togather are read togather and put togather in the same 'message', 
serial port is inherently packet-less, meaning that we don't have real 'message's like websocket/HTTP. 
Data for the same message may be sticked togather in a single 'message', or may be seperated in different 'message's.
The only promise is that when 'message's are joined togather, the original byte sequence is kept. 
So it is the user's responsibility to parse their data by reading the stream.

To extract complete message frames from the stream, you need to use a framing algorithm to mark packet boundaries.
There're two options provided by labctrl: 

1. The standard COBS algorithm. See cobs_framer.py

2. The length-content-pattern framer. See pattern_framer.py
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
import serial

# Configure logging
lg = logging.getLogger(__name__)


class SerialManager:
    """
    SerialManager binds to a given serial port and buffers all IO on the port to provide an asynchronous interface.
    Also prevents data loss and corruption due to serial driver buffer overflow.
    And also provides thread-safe methods to communicate with serial ports.
    """

    def __init__(self, com_port: str,
                 baudrate: int = 115200, timeout: float = 1.0,
                 ) -> None:
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        # multithread channels and flags
        self.received_queue = Queue()
        self.to_send_queue = Queue()
        self.sent_id_queue = Queue()
        self.is_manager_running = False
        self.serial_read_thread = Thread(target=self.serial_read_task)
        self.serial_write_thread = Thread(target=self.serial_write_task)
        lg.info("Created SerialManager, bound to port {}".format(self.com_port))

    def get_serial(self):
        """
        connects to serial port according to current configuration.
        returns the handler Serial object.
        """
        return serial.Serial(self.com_port, baudrate=self.baudrate, timeout=self.timeout)

    def start(self):
        if self.is_manager_running:
            lg.warning(
                "SerialManager already started! If restart is intended, try call .stop first.")
            return
        # make sure serial port is connected.
        if self.ser:
            if not self.ser.is_open:
                self.ser.open()
        else:
            lg.warning("Serial port is not connected yet, reconnecting")
            self.ser = self.get_serial()
        # check for empty queues
        n_items = self.received_queue.qsize()
        if n_items != 0:
            lg.warning("Receiving queue still has {} item(s) not consumed! \
                       You may get old results from last connection when calling .receive. \
                       If this is not intended, consider clear the queue \
                       before calling start".format(n_items))
        n_items = self.to_send_queue.qsize()
        if n_items != 0:
            lg.warning("Sending queue still has {} item(s) not sent! \
                       These items will be wrote to port immediately after start.\
                       If this is not intended, consider clear the queue\
                       before calling start".format(n_items))
        # start the threads
        lg.info("Starting SerialManager R/W threads.")
        self.is_manager_running = True
        self.serial_read_thread.start()
        self.serial_write_thread.start()

    def stop(self):
        lg.info("Gracefully halting R/W threads, this may block a while.")
        self.is_manager_running = False
        # put None in the queue to indicate closing of the send queue because python queue doesn't have a explicit way
        # to express releasing of a channel.
        self.to_send_queue.put(None)
        # wait for threads to finish last jobs
        self.serial_read_thread.join()
        self.serial_write_thread.join()
        # close serial port
        self.ser.close()

    def receive(self, timeout: float | None = None) -> tuple[int, bytes]:
        """
        Gets earlist message in the buffer queue.

        Returns: (
            time_ns : int, the time when message is received, unit in ns, since epoch. 
            message : bytes, the message
            )
            or (None, None) if timeout exceeds

        This method blocks until a message arrives if received_queue is empty, or until timeout,
        so check for queue size before calling if blocking is not desired.
        """
        try:
            item = self.received_queue.get(timeout=timeout)
            self.received_queue.task_done()
            return item
        except Empty:
            return (None, None)

    def send(self, to_send: bytes, sent_id: int = 0) -> int:
        """
        Adds a message to the send queue. If message is empty, nothing happens.
        This method will not block. If you need to wait for confirmation, use sent_id.

        Optional: a sent_id number can be passed in. If the sent_id is non-zero, after the message is sent, the sent_id
            and a timestamp is put into a sent_id_queue. The user can monitor the sent_id_queue to check if a specific 
            message has been written to serial port and when is the writing done.
        """
        if to_send:
            self.to_send_queue.put((to_send, sent_id))
            return len(to_send)
        else:
            return 0

    def serial_read_task(self):
        while self.is_manager_running:
            if self.ser.in_waiting:
                new_data = self.ser.read_all()
                current_time_ns = time.time_ns()
                self.received_queue.put((current_time_ns, new_data))

    def serial_write_task(self):
        while self.is_manager_running:
            send_task = self.to_send_queue.get()
            if send_task:
                to_write, sent_id = send_task[0], send_task[1]
                self.ser.write(to_write)
                if sent_id:
                    current_time_ns = time.time_ns()
                    self.sent_id_queue.put((current_time_ns, sent_id))
                self.to_send_queue.task_done()
            else:
                # send_task = None indicates the producer is closing the queue, thread ends.
                self.to_send_queue.task_done()
                break
