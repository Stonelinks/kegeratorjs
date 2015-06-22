#!/usr/bin/env python3
__author__ = 'nwiles'
import unittest
import thermostat
import lager

class RelayStub:
    def __init__(self):
        self.is_on = False
    def __call__(self, on):
        self.is_on = on

class Float:
    def __init__(self, value):
        self.value = value
    def __call__(self, *args, **kwargs):
        return self.value

class TestThermostat(unittest.TestCase):
    def test_thermostat(self):
        relay = RelayStub()
        inputs = thermostat.ThermostatState(set_point_deg_c=1, dead_band_deg_c=2, on_adds_heat=False)
        current_temp = Float(inputs.set_point_deg_c+inputs.dead_band_deg_c+0.1)
        uut = thermostat.Thermostat(current_temp, relay, False, lager.Lager('log.temp'))
        uut.set_state(inputs)
        self.assertEqual(relay.is_on, False)
        uut.loop()
        self.assertEqual(relay.is_on, True)
        current_temp.value = inputs.set_point_deg_c-inputs.dead_band_deg_c
        uut.loop()
        self.assertEqual(relay.is_on, True)
        current_temp.value =  inputs.set_point_deg_c-inputs.dead_band_deg_c-0.1
        uut.loop()
        self.assertEqual(relay.is_on, False)
        current_temp.value = inputs.set_point_deg_c+inputs.dead_band_deg_c
        uut.loop()
        self.assertEqual(relay.is_on, False)
        current_temp.value = inputs.set_point_deg_c+inputs.dead_band_deg_c+0.1
        uut.loop()
        self.assertEqual(relay.is_on, True)

if __name__ == '__main__':
    unittest.main()