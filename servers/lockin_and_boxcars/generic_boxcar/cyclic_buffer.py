import numpy as np

class CyclicBuffer:
    def __init__(self, length=65536, dtype=np.float64) -> None: 
        self.length = length # default 64 kSamples = 512 kB
        self.data = np.zeros(self.length, dtype=dtype)
        self.current_data_index = 0
    
    def append(self, value):
        self.current_data_index += 1
        if self.current_data_index >= self.length:
            self.current_data_index = 0
        self.data[self.current_data_index] = value
    
    def append_bulk(self, slice):
        # slice_len = np.size(slice)
        for i in slice:
            self.append(i) # it might be a little bit faster if we modify the whole slice at once in julia with simd, but the performance is nearly the same in python...

    def get_current(self):
        # print(self.data)
        return self.data[self.current_data_index]
    
    def get_slice(self, istart, istop):
        # index out of bound!
        assert abs(istop - istart) <= self.length
        # recursive: put istart and istop between 0 - length
        if istop > self.length:
            return self.get_slice(istart, istop - self.length)
        if istart > self.length:
            return self.get_slice(istart - self.length, istop)
        if istart < 0:
            return self.get_slice(istart + self.length, istop)
        if istop < 0:
            return self.get_slice(istart, istop + self.length)
        # if stop is larger than start, it's just normal slice. if stop is smaller, we need to cat tail and head
        if istop > istart:
            return self.data[istart:istop]
        elif istop == istart:
            return np.array([])
        else:
            buf_tail = self.data[istart:self.length]
            buf_head = self.data[0:istop]
            return np.concatenate((buf_tail, buf_head))
