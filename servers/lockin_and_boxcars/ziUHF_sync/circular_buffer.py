# -*- coding: utf-8 -*-

"""circular_buffer.py:
This module provides an inefficient circular buffer for generic buffering
of incoming data.
For data intensive apps, use C extension to hold the buffer and deal with
data reading and statistics, interface with ctypes instead.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221113"


import numpy as np


class CircularBuffer:
    """
    This implementation uses a classical double size buffer for continuous block access,
    which slows down appending by 2x but speeds up reading and manipulation when 'tail'
    of circular buffer is accessed 
    """

    def __init__(self, length: int = 65536, dtype=np.float64) -> None:
        self.length: int = length  # default 64 kSamples = 512 kB
        # shadow buffer the same size as circular
        self.internal_length: int = self.length * 2
        self.data = np.zeros(self.internal_length, dtype=dtype)
        self.current_data_index: int = 0

    def append(self, value):
        if self.current_data_index >= self.length:
            self.current_data_index = 0
        self.data[self.current_data_index] = value
        # write to shadow buffer
        self.data[self.current_data_index + self.length] = value
        self.current_data_index += 1

    def append_bulk(self, slice):
        # slice_len = np.size(slice)
        for i in slice:
            # it might be a little bit faster if we modify the whole slice at once in julia with simd, 
            # but the performance is nearly the same in python...
            self.append(i)

    def get_current(self):
        # print(self.data)
        return self.data[self.current_data_index]

    def get_slice(self, istart, istop):
        assert abs(istop - istart) <= self.length, "Index out of bound!"
        istop = istop % self.length
        istart = istart % self.length
        if istop > istart:
            return self.data[istart:istop]
        else:
            return self.data[istart:istop+self.length]
