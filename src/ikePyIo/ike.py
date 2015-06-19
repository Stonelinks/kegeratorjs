import sf800
import thermostat
import relay
import w1thermsensor
import semantic_version as sv
import time
import RPIO
import keg
import lager

class Ike:
    def __init__(self, relayPin, flow1Pin, flow2Pin):
        self.version=sv.Version('0.0.1')
        self.logger = lager.Lager('events.json')
        #kegs and flow
        self.flowMeters = []
        self.flowMeters.append( sf800.SF800(flow1Pin) )
        self.flowMeters.append( sf800.SF800(flow2Pin) )
        self.kegs = []
        for f, i in self.flowMeters:
            self.kegs.append(keg.Keg(i, f.get_flow_liters, 0, logger=self.logger))
        #thermostat
        self.tempSensor = w1thermsensor.W1ThermSensor()
        self.compressorRelay = relay.Relay(relayPin)
        self.thermostat = thermostat.Thermostat(self.tempSensor.get_temperature, self.compressorRelay, on_adds_heat=0)
        self.thermostat.start()
        #TODO: pressure and ADC
        #self.kegPressure =
        #self.tankPressure =

    def run(self):
        print("Welcome to IKE, version {}".format(self.version))
        while(1):
            print(chr(27) + "[2J")
            print(self.thermostat)
            print(self)
            time.sleep(1)

    def __del__(self):
        self.thermostat.join()
        for k in self.kegs:
            k.join()
        RPIO.cleanup()

    def __str__(self):
        pass