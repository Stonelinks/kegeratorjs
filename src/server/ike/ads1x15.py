from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import ike.Adafruit_ADS1x15 as Adafruit_ADS1x15
import threading
import collections
import time

Channel = collections.namedtuple('Channel', 'id gain sps')

class ADS1x15Manager(threading.Thread):
    def __init__(self, channels, poll_interval=1):
        super(ADS1x15Manager, self).__init__()
        self._channels = channels
        self._channel_data = {}
        self._poll_interval = poll_interval
        self._adc = Adafruit_ADS1x15.ADS1x15(ic=1) #using the ADS1115
        self._stop_evt = threading.Event()
        self._api_lock = threading.Lock()
        for c in self._channels:
            self._channel_data[c.id] = 0

    def read(self, channel):
        with self._api_lock:
            return self._channel_data[channel]

    def run(self):
        while not self._stop_evt.isSet():
            with self._api_lock:
            for c in self._channels:
                self._channel_data[c.id] = (self._adc.readADCSingleEnded(channel=c.id, pga=c.gain, sps=c.sps))/1000.0
            time.sleep(self._poll_interval)
        self._stop_evt.clear()

    def stop(self):
            self._stop_evt.set()
            super(ADS1x15Manager, self).stop()