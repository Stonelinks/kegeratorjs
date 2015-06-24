#!/usr/bin/env python3
__author__ = 'nwiles'
import unittest
import keg
import time
class FlowGetter:
    def __init__(self, const):
        self.const = const

    def get_flow_liters(self):
        return self.const

class TestLager(unittest.TestCase):
    def test_kegs(self):
        flowGetter = FlowGetter(0.0)
        uut = keg.Keg(0, 1, flowGetter.get_flow_liters)
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

        with uut._state_lock:
            flowGetter.const = uut._pour_threshold_l_per_s * uut._loop_period_s-0.001

        time.sleep(uut._loop_period_s*2)
        self.assertEqual(uut._is_pouring, False)
        state = uut.get_state()
        self.assertEqual(state['beerId'], 4)
        self.assertEqual(state['consumedL'], 1.0)
        self.assertEqual(state['capacityL'], 10.0)
        self.assertEqual(uut._is_pouring, False)

        with uut._state_lock:
            flowGetter.const += uut._pour_threshold_l_per_s * uut._loop_period_s + 0.001 # should be enough to trigger a pour

        time.sleep(uut._loop_period_s*2)
        state = uut.get_state()
        self.assertAlmostEqual(state['consumedL'], 1.00 + uut._pour_threshold_l_per_s * uut._loop_period_s + 0.001)
        self.assertEqual(state['capacityL'], 10.0)
        self.assertEqual(uut._is_pouring, True)

        time.sleep(uut._pour_timeout_s)
        self.assertEqual(uut._is_pouring, False)

        uut.join()


if __name__ == '__main__':
    unittest.main()