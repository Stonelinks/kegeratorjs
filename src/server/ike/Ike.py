import ike.sf800 as sf800
import ike.thermostat as thermostat
import ike.relay as relay
import ike.keg as keg
import ike.lager as lager
import semantic_version as sv

import time
try:
    import RPIO
    import w1thermsensor
except ImportError:
    pass

class Ike:
    def __init__(self, relayPin, flow1Pin, flow2Pin):
        self.version=sv.Version('0.0.1')
        self._logger = lager.Lager('events.json')
        #kegs and flow
        self.flowMeters = []
        self.flowMeters.append( sf800.SF800(flow1Pin) )
        self.flowMeters.append( sf800.SF800(flow2Pin) )
        self._kegManager = keg.KegManager(flowMeters = flowMeters, logger=self._logger)
        #thermostat
        self.tempSensor = w1thermsensor.W1ThermSensor()
        self.compressorRelay = relay.Relay(relayPin)
        self._thermostat = thermostat.Thermostat(self.tempSensor.get_temperature, self.compressorRelay, on_adds_heat=0, logger=self._logger)
        self._thermostat.start()
        self._kegManager.start()
        #TODO: pressure and ADC
        #self.kegPressure =
        #self.tankPressure =

    def run(self):
        print("Welcome to IKE, version {}".format(self.version))
        api.launch(self)
        while(1):
                print(chr(27) + "[2J")
                print(self._thermostat)
                print(self)
                time.sleep(1)


    def __del__(self):
        self._thermostat.join()
        self._kegManager.join()
        RPIO.cleanup()

    def __str__(self):
        pass
