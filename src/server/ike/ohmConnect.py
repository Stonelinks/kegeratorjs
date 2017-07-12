
import threading
import time
import requests
import xml.etree.ElementTree
__author__ = 'nwiles'


def parse_ohm_hour_is_active(xml_str):
    """Parse xml_str and return true in case of an active ohmhour"""
    tree = xml.etree.ElementTree.fromstring(xml_str)
    active_elem = tree.find('active')
    return active_elem.text.lower() == 'true'


def check_if_ohm_hour_is_active(url, timeout):
    """Hit OhmConnect's REST API and return True if there are active ohmhours"""
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            active = parse_ohm_hour_is_active(r.content)
        else:
            active = False
            print('OhmConnect: error checking ohmhour status {}'.format(r.status_code))
    except Exception as e:
        print("OhmConnect: {}".format(e))
    return active


class OhmConnect(threading.Thread):
    def __init__(self, url, callback=lambda x: x,  poll_interval=60):
        threading.Thread.__init__(self, name="OhmConnect")
        self._url=url
        self._stop_event = threading.Event()
        self._poll_interval=poll_interval
        self._callback = callback

    def run(self):
        self._last_poll=time.time()
        while not self._stop_event.isSet():
            self.loop()
            time.sleep(0.5)

    def loop(self):
        now = time.time()
        if now-self._last_poll >= self._poll_interval:
            self._callback(check_if_ohm_hour_is_active(self._url,
                                                       self._poll_interval))
            self._last_poll = now

    def join(self, timeout=None):
        self._stop_event.set()
        super(OhmConnect, self).join(timeout=timeout)
