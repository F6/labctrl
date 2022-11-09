# -*- coding: utf-8 -*-

"""
COM_mitm.py:

This utility script is used to setup Man-in-the-Middle proxy for debug
COM port communications on the Windows platform.

In POSIX platforms, you simply pipe the messages from one COM to another
COM, so this script is not needed if only monitoring is needed, however,
if you'd like to alter the buffers on-the-fly, this script can also be used.

Tutorial:
    1. install com0com util, you can get it on sourceforge or in this dir
        (only needed on Windows)
    2. setup a pair of virtual COM ports using com0com, e.g. COM15 and COM16
        (only needed on Windows, the com0com util should have automatically 
            done this for you by default)
    3. set below SOURCE_PORT to one of the virtual ports, e.g. COM15
    4. set below TARGET_PORT to device port to be MitM'd, e.g. COM14
    5. implement forward_transmit_hook and backward_transmit_hook as hooks
        (for now they are implemented as GRBL interface message parsers)
    6. run this script
    7. open another *virtual port* in application to be MitM'd, 
        e.g. open COM16 in bCNC
    8. you are good to go
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221106"

import serial
import time
import sys
from threading import Thread

from GRBL_interface_parser import GRBLParser


SOURCE_PORT = "COM15"
TARGET_PORT = "COM14"
print("Opening Source Port {}".format(SOURCE_PORT))
sf = serial.Serial(SOURCE_PORT, timeout=1, baudrate=115200)
print("Opening Target Port {}".format(TARGET_PORT))
st = serial.Serial(TARGET_PORT, timeout=1, baudrate=115200)

parser = GRBLParser()

running = True

def forward_transmit_hook(buf):
    print("[Source->Target]: ", buf.decode())
    sys.stdout.flush()
    return buf

def backward_transmit_hook(buf):
    messages = buf.decode().split('\n')
    for message in messages:
        print("[Target->Source]:{}".format(message))
        message = message.strip("\r\n")
        if message:
            # print("[Parser]: Parsing: {}".format(message))
            parser.parse_push_message(message)
            print("[Parser]: Parsed result: {}".format(parser.vars))
        sys.stdout.flush()
    return buf

def task():
    while running:
        time.sleep(0.05)
        if sf.in_waiting:
            buf = sf.read_all()
            try:
                buf = forward_transmit_hook(buf)
            except Exception as e:
                print(e)
                sys.stdout.flush()
            st.write(buf)
        if st.in_waiting:
            buf = st.read_all()
            try:
                buf = backward_transmit_hook(buf)
            except Exception as e:
                print(e)
                sys.stdout.flush()
            sf.write(buf)

thread = Thread(target=task)
thread.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sf.close()
        st.close()
        running = False
        exit()
