from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import RPIO

class Relay:
    def __init__(self, gpioPin):
        self.gpioPin = gpioPin
        RPIO.setup(self.gpioPin, RPIO.OUT)
        self.relayOutput = False

    def __call__(self, on):
        self.relayOutput = on
        RPIO.output(self.gpioPin, self.relayOutput)

    def __del__(self):
        RPIO.setup(self.gpioPin, RPIO.IN)

    def __str__(self):
        return "relay:{}".format(self.relayOutput)
