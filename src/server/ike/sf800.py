__author__ = 'nwiles'
try:
    import RPIO
except ImportError:
    pass

class SF800:
    _TICKS_PER_LITER = 5400
    def __init__(self, gpio_id):
        self.gpio_id = gpio_id
        RPIO.add_interrupt_callback(gpio_id, self, edge='falling', pull_up_down=RPIO.PUD_UP, threaded_callback=True, debounce_timeout_ms=2)
        RPIO.wait_for_interrupts(threaded=True)
        self.flowCounts = 0

    def __call__(self, channel, value):
        self.flowCounts +=1

    def __del__(self):
        RPIO.del_interrupt_callback(self.gpio_id)

    def __str__(self):
        return "Flow: ticks:{}".format(self.flowCounts)

    def get_flow_liters(self):
        return float(self.flowCounts)/SF800._TICKS_PER_LITER