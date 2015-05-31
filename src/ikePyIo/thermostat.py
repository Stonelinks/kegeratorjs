__author__ = 'nwiles'

class Thermostat:
    def __init__(self, tempInputFn, relay, onAddsHeat):
        self.setpoint_DegC = 4
        self.deadBand_DegC = 2
        self.getTempInput_DegC = tempInputFn
        self.onAddsHeat = onAddsHeat
        self.sense_DegC = 0
        self.relay = relay
        self.outputSetting=False

    def run(self):
        try:
            self.sense_DegC = self.getTempInput_DegC()
            if(self.sense_DegC > self.setpoint_DegC+self.deadBand_DegC):
                #too warm
                self.outputSetting = not self.onAddsHeat
            elif(self.sense_DegC < self.setpoint_DegC-self.deadBand_DegC):
                #too cold
                self.outputSetting = self.onAddsHeat
            self.relay(self.outputSetting)
        except:
            print("Thermostat: error reading temp or setting output")

    def __str__(self):
        return "Thermostat: sense:{:2.1f} set:{:2.1f} delta:{:2.1f}degC {}".format(self.sense_DegC,
                                                                                   self.setpoint_DegC,
                                                                                   self.sense_DegC-self.setpoint_DegC,
                                                                                   self.relay)
