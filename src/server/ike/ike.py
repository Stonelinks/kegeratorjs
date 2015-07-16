import ike.sf800 as sf800
import ike.thermostat as thermostat
import ike.relay as relay
import ike.keg as keg
import ike.lager as lager
import RPIO
import w1thermsensor
import semantic_version as sv
import time
import os.path
import config

class Ike:
    def __init__(self):
        self.version=sv.Version('0.0.1')
        self._logger = lager.Lager(os.path.join(config.DB_ROOT, 'events.json'))
        #kegs and flow
        self._flowMeters = []
        self._flowMeters.append( sf800.SF800(config.FLOW_1_PIN) )
        self._flowMeters.append( sf800.SF800(config.FLOW_2_PIN) )
        self._kegManager = keg.KegManager(flow_meters = self._flowMeters, logger=self._logger)
        #thermostat
        self.tempSensor = w1thermsensor.W1ThermSensor()
        self.compressorRelay = relay.Relay(config.RELAY_PIN)
        self._thermostat = thermostat.Thermostat(self.tempSensor.get_temperature, self.compressorRelay, on_adds_heat=0, logger=self._logger)
        self._thermostat.start()
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
