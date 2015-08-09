#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import unittest
import ike.keg as keg
import ike.lager
import tinydb
import time
import os
class FlowGetter:
    def __init__(self, const):
        self.const = const

    def get_flow_liters(self):
        return self.const

class TestLager(unittest.TestCase):
    def test_kegs(self):
        flowGetter = FlowGetter(0.0)
        try:
            os.remove("keg.temp")
        except:
            pass
        uut = keg.Keg(0, 1, flowGetter.get_flow_liters, ike.lager.Lager("test.log"), tinydb.TinyDB("keg.temp") )
        state = uut.get_state()
        self.assertEqual(state['beerId'], 1)
        self.assertEqual(state['consumedL'], 0.0)
        self.assertEqual(state['capacityL'], 17.0)
        self.assertEqual(state['flowRateLitersPerSec'], 0.0)

        uut.set_state({'beerId': 4,
                       'consumedL': 1,
                       'capacityL': 10})
        state = uut.get_state()

        self.assertEqual(state['beerId'], 4)
        self.assertEqual(state['consumedL'], 1.0)
        self.assertEqual(state['capacityL'], 10.0)
        self.assertEqual(state['flowRateLitersPerSec'], 0.0)

        flowGetter.const = uut._pour_threshold_l_per_s * uut._loop_period_s-0.001

        time.sleep(uut._loop_period_s*2)
        uut.loop()
        self.assertEqual(uut._is_pouring, False)
        state = uut.get_state()
        self.assertEqual(state['beerId'], 4)
        self.assertEqual(state['consumedL'], 1.0)
        self.assertEqual(state['capacityL'], 10.0)
        self.assertEqual(uut._is_pouring, False)

        flowGetter.const += uut._pour_threshold_l_per_s * uut._loop_period_s + 0.001 # should be enough to trigger a pour

        uut.loop()
        time.sleep(uut._loop_period_s*2)
        uut.loop()

        state = uut.get_state()
        self.assertEqual(uut._is_pouring, True)
        self.assertAlmostEqual(state['consumedL'], 1.00 + uut._pour_threshold_l_per_s * uut._loop_period_s + 0.001)
        self.assertEqual(state['capacityL'], 10.0)

        time.sleep(uut._pour_timeout_s)
        uut.loop()

        self.assertEqual(uut._is_pouring, False)


if __name__ == '__main__':
    unittest.main()