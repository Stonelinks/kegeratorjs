#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'

import unittest
import ike.analogSensor as analogSensor

class Getter():
    def __init__(self, data):
        self.data = data

    def __call__(self):
        return self.data

class TestAnalogSensor(unittest.TestCase):
    def test_analog_sensor(self):
        getter = Getter(0)
        uut = analogSensor.AnalogSensor(getter, [(0, 2),
                                                 (10,200)])
        self.assertEqual(uut.read(), 2)
        getter.data = 10
        self.assertEqual(uut.read(), 200)
        getter.data = 5
        self.assertEqual(uut.read(), 101)

if __name__ == '__main__':
    unittest.main()