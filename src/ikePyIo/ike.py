import sf800
import thermostat
import relay
import w1thermsensor
import semantic_version as sv
import time
import RPIO

class Ike:

    def __init__(self, relayPin, flow1Pin, flow2Pin):
        self.version=sv.Version('0.0.1')
        self.flowMeters = []
        self.flowMeters.append( sf800.SF800(flow1Pin) )
        self.flowMeters.append( sf800.SF800(flow2Pin) )
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
            for f in self.flowMeters:
                print(f)
            time.sleep(1)

    def __del__(self):
        self.thermostat.join()
        RPIO.cleanup()
