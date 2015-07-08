__author__ = 'nwiles'
import ike.thermostat as thermostat
import ike.keg as keg
import ike.lager as lager
import config

def set_relay(input):
    pass

def temp_input():
    return 4.0

class FlowStub:
    def get_flow_liters(self):
        return True

class Ike:
    def __init__(self):
        self._logger = lager.Lager('events.json')
        flow_stubs = []
        flow_stubs.append(FlowStub())
        flow_stubs.append(FlowStub())
        self._kegManager = keg.KegManager(flow_meters=flow_stubs)
        self._thermostat = thermostat.Thermostat(temp_input, set_relay, False, self._logger)
