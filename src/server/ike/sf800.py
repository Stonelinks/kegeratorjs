from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import RPIO

class SF800:
    _TICKS_PER_LITER = 5400.0
    def __init__(self, gpio_id):
        self.gpio_id = gpio_id
        RPIO.add_interrupt_callback(gpio_id, self, edge='falling', pull_up_down=RPIO.PUD_UP, threaded_callback=True, debounce_timeout_ms=2)
        self.flowCounts = 0

    def __call__(self, channel, value):
        self.flowCounts +=1

    def __str__(self):
        return "Flow: ticks:{}".format(self.flowCounts)

    def get_flow_liters(self):
        return float(self.flowCounts)/SF800._TICKS_PER_LITER
