from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
import ike.analogSensor as analogSensor

class M7139_200PG(analogSensor.AnalogSensor):
    def __init__(self, analog_input):
        volts_to_pascals_map = [(0.453, 0.0),
                                (4.5, 1378951.46)] # 0 to 200 psi
        super(M7139_200PG, self).__init__(analog_input, volts_to_pascals_map)


class M7139_03KPN(analogSensor.AnalogSensor):
    def __init__(self, analog_input):
        volts_to_pascals_map = [(0.453, 0.0),
                                (4.5, 20684271.9)] # 0 to 3000 psi
        super(M7139_03KPN, self).__init__(analog_input, volts_to_pascals_map)