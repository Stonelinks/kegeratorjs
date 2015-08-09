from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import numpy

class AnalogSensor(object):
    def __init__(self, analog_input, voltage_map):
        self.analog_input = analog_input
        self.voltage_map = voltage_map

    def read(self):
        voltage = self.analog_input()
        return numpy.interp(voltage, list(self.voltage_map.keys()), list(self.voltage_map.values()))
