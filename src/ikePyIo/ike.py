__author__ = 'nwiles'
from sf800 import SF800
from thermostat import Thermostat
from w1thermsensor import W1ThermSensor
import semantic_version as sv
import sys

class Ike:
    #these are BOARD pins
    __GPIO_PIN_TEMPERATURE = 7 #hardcoded in the w1 kernel module to use BCM GPIO4
    __GPIO_PIN_RELAY = 11
    __GPIO_PIN_INT_FLOW_1 = 13
    __GPIO_PIN_INT_FLOW_2 = 15

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.version=sv.Version('0.0.1')
        self.flowMeters = []
        self.flowMeters.append( sf.sf800(__GPIO_PIN_INT_FLOW_1) )
        self.flowMeters.append( sf.sf800(__GPIO_PIN_INT_FLOW_2) )
        self.tempSensor = W1ThermSensor()
        self.compressorRelay = Relay(__GPIO_PIN_RELAY)
        self.thermostat = thermo.Thermostat(self.tempSensor.get_temperature, self.compressorRelay, onAddsHeat=0)
        #TODO: pressure and ADC
        #self.kegPressure =
        #self.tankPressure =

    def run(self):
        print("Welcome to IKE, version {}".format(self.version))
        while(1):
            self.thermostat.run()
            print(self.thermostat)
            for f in self.flowMeters:
                print(f)
            sys.sleep(500)

    def __del__(self):
        RPIO.cleanup()