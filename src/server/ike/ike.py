from __future__ import absolute_import, division, print_function
import ike.sf800 as sf800
import ike.thermostat as thermostat
import ike.relay as relay
import ike.keg as keg
import ike.lager as lager
import ike.measurementSpecialties as ms
import ike.ads1x15 as ads1x15
import ike.carbonation as carbonation
import RPIO
import w1thermsensor
import semantic_version as sv
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
        #pressure
        self._adcManager = ads1x15.ADS1x15Manager([ads1x15.Channel(id=0, gain=4096, sps=8),
                                                   ads1x15.Channel(id=1, gain=4096, sps=8)])
        self._adcManager.start()
        self._kegPressure = ms.M7139_200PG(lambda: self._adcManager.read(0))
        self._tankPressure = ms.M7139_03KPN(lambda: self._adcManager.read(1))
        self._carbonationVolumes = lambda: carbonation.volumes(self.tempSensor.get_temperature(), self._kegPressure.read())
        RPIO.wait_for_interrupts(threaded=True)

    def __del__(self):
            self._adcManager.stop()
            self._adcManager.join()

            self._thermostat.stop()
            self._thermostat.join()

            self._kegManager.stop()
            self._kegManager.join()
            RPIO.cleanup()

    def __str__(self):
        pass
