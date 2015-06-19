from sf800 import SF800
from thermostat import Thermostat
from relay import Relay
from w1thermsensor import W1ThermSensor
import semantic_version as sv
from time import sleep
import RPIO
import keg
import lager

class Ike:
    def __init__(self, relayPin, flow1Pin, flow2Pin):
        self.version=sv.Version('0.0.1')
        self.logger = lager.Lager('events.json')
        #kegs and flow
        self.flowMeters = []
        self.flowMeters.append(SF800(flow1Pin))
        self.flowMeters.append(SF800(flow2Pin))
        self.kegs = []
        for f, i in self.flowMeters:
            self.kegs.append(keg.Keg(i, f.get_flow_liters, 0, logger=self.logger))
        #thermostat
        self.tempSensor = W1ThermSensor()
        self.compressorRelay = Relay(relayPin)
        self.thermostat = Thermostat(self.tempSensor.get_temperature, self.compressorRelay, on_adds_heat=0)
        self.thermostat.start()
        #TODO: pressure and ADC
        #self.kegPressure =
        #self.tankPressure =

    def run(self):
        print("Welcome to IKE, version {}".format(self.version))
        while(1):
            print(chr(27) + "[2J")
            print(self.thermostat)
            for f in self.flowMeters:
                print(f)
            sleep(1)

    def __del__(self):
        self.thermostat.join()
        for k in self.kegs:
            k.join()
        RPIO.cleanup()
