from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import numpy
import sys
class AnalogSensor(object):
    def __init__(self, analog_input, voltage_map):
        self.analog_input = analog_input
        self.x = [point[0] for point in voltage_map]
        self.y = [point[1] for point in voltage_map]

    def read(self):
        voltage = self.analog_input()
        return numpy.interp(voltage, self.x, self.y)
