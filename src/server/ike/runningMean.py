from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import collections

class RunningMean:
    def __init__(self, window_size):
        self.cache = collections.deque()
        self.cum_sum = 0
        self.window_size = window_size
    def add_val(self, val):
        self.cache.append(val)
        self.cum_sum += val
        if len(self.cache) >= self.window_size:  # if window is saturated, subtract oldest value
            self.cum_sum -= self.cache.popleft()
            self.avg = self.cum_sum/float(self.window_size)
        else:
            self.avg = self.cum_sum/float(len(self.cache))
    def get_avg(self):
        return self.avg