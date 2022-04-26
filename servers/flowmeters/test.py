# -*- coding: utf-8 -*-

"""test.py
simple bokeh app to monitor dropmeter status
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220402"

import serial
import time
from collections import deque
from threading import Thread
from functools import partial
import struct
import numpy as np
from bokeh.plotting import curdoc
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput, Div, Button
from common import FactoryFigure1D

doc = curdoc()

packet_len = 4096
data_len = packet_len // 2

factory = FactoryFigure1D()
oscbundle = factory.generate_fig1d(
    'Oscilloscope', 'Time (us)', 'ADC Value', data_len)
trigbundle = factory.generate_fig1d(
    'Trigger', 'Time (us)', 'ADC Value', data_len * 2)
dpsbundle = factory.generate_fig1d('drops/s', 'Time (s)', 'Drops', 600)

low_in = TextInput(title='Pulse Trigger Threshold', value="450")
high_in = TextInput(title='Pulse Resume Threshold', value="500")
dps_average_in = TextInput(
    title='Drops per second time window (s)', value='5.0')
dcdiv = Div(text="Total Drops Count: ")


dropevents = deque([0] * 4096, maxlen=4096)  # record 4096 events max
dropcount = 0


def callback_update_dcdiv(i):
    dcdiv.text = "Total Drops Count: {}".format(i)


def callback_clear_dropcount(i):
    global dropcount
    dropcount = 0


button_clear_dc = Button(label='Clear Drops Count', button_type='warning')
button_clear_dc.on_click(callback_clear_dropcount)
s = serial.Serial('COM12', baudrate=114500, timeout=1)


def parse_data(buf):
    return np.asarray(struct.unpack('<{}H'.format(data_len), buf))


def signal_processing(x):
    # do a moving average of window length 3
    N = 3
    return np.convolve(x, np.ones(N)/N, mode='valid')


def findpulse(x, high, low):
    """find pulses, x: array; high, low: int;
    return: (bool, lindex: int)
    return: success, index when go low
    """
    xsize = np.size(x)
    # find the first element that is higher than upper threshold
    uindex = -1
    for i in range(xsize):
        if x[i] > high:
            uindex = i
            break
    if uindex == -1:  # all-low
        return (False, -1)

    # find first element that is lower than lower threashold
    lindex = -1
    for i in range(uindex, xsize):
        if x[i] < low:
            lindex = i
            break
    if lindex == -1:  # after go high, never go low again, so no trig
        return (False, -1)

    return (True, lindex)


y = np.zeros(data_len)
lastbuffer = np.zeros(data_len)


def doit(databuffer):
    global dropcount, y, lastbuffer

    lastlastbuffer = lastbuffer
    lastbuffer = y
    y = parse_data(databuffer)
    y = signal_processing(y)
    sizey = np.size(y)
    x = np.arange(sizey) * 10
    doc.add_next_tick_callback(
        partial(oscbundle.callback_update, x, y))

    # detect falling edge at middle buffer
    pulse, lindex = findpulse(lastbuffer, int(
        high_in.value), int(low_in.value))
    if pulse:
        dropevents.appendleft(time.time())
        dropcount = dropcount + 1
        pulsebuffer = np.concatenate(
            [lastlastbuffer, lastbuffer, y])
        pulse_y = pulsebuffer[sizey + lindex -
                              sizey // 4: sizey + lindex + sizey // 2]
        pulse_x = np.arange(np.size(pulse_y)) * 10
        doc.add_next_tick_callback(
            partial(trigbundle.callback_update, pulse_x, pulse_y))


def data_reading_task():
    while True:
        time.sleep(0.01)  # this is here to prevent pyserial eating up all cpu
        if s.in_waiting:
            databuffer = s.read_all()
            if len(databuffer) == packet_len:
                doit(databuffer)
            else:
                print("corrupted data!")


def drop_counting_task():
    """do dps counting every 1/10s"""
    t0 = time.time()
    while True:
        time.sleep(0.04)
        tnow = time.time()
        dt = tnow - t0
        twindow = float(dps_average_in.value)
        count = 0
        for t in dropevents:
            if tnow - t < twindow:
                count = count + 1
            else:
                break
        dps = count / twindow
        doc.add_next_tick_callback(
            partial(dpsbundle.callback_stream, [dt], [dps]))
        doc.add_next_tick_callback(
            partial(callback_update_dcdiv, dropcount))


dr = Thread(target=data_reading_task)
dr.start()

dct = Thread(target=drop_counting_task)
dct.start()

foo = column(dpsbundle.fig,
             trigbundle.fig,
             oscbundle.fig)

bar = column(low_in, high_in, dps_average_in, dcdiv, button_clear_dc)

myrow = row(foo, bar)

doc.add_root(myrow)
