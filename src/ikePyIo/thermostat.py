__author__ = 'nwiles'
import threading
import time
import runningMean

class ThermostatState:
    def __init__(self, set_point_deg_c, dead_band_deg_c, on_adds_heat):
        self.set_point_deg_c = set_point_deg_c
        self.dead_band_deg_c = dead_band_deg_c
        self.on_adds_heat = on_adds_heat

class ThermostatSense:
    def __init__(self, deg_c, avg_deg_c):
        self.deg_c = deg_c
        self.avg_deg_c = avg_deg_c

class Thermostat(threading.Thread):
    def __init__(self, tempInputFn, relay, on_adds_heat):
        threading.Thread.__init__(self, name="Thermostat")
        self._state = ThermostatState(set_point_deg_c=2.5, dead_band_deg_c=2, on_adds_heat=on_adds_heat)
        self._getTempInput_DegC = tempInputFn
        self._sense = ThermostatSense(0, 0)
        self._avg_deg_c = RunningMean(1000)
        self._relay = relay
        self._outputSetting=False
        self._state_lock = threading.Lock()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.isSet():
            try:
                new_reading_deg_c = self._getTempInput_DegC()
                with self._state_lock:
                    self._sense.deg_c = new_reading_deg_c
                    self._avg_deg_c.add_val(new_reading_deg_c)
                    self._sense.avg_deg_c = self._avg_deg_c.get_avg()
                    #run logic:
                    if self._sense.deg_c > self._state.set_point_deg_c+self._state.dead_band_deg_c:
                        # too warm
                        self._outputSetting = not self._state.on_adds_heat
                    elif self._sense.deg_c < self._state.set_point_deg_c-self._state.dead_band_deg_c:
                        # too cold
                        self._outputSetting = self._state.on_adds_heat
                self._relay(self._outputSetting)
            except Exception as e:
                print("Thermostat: error reading temp or setting output")
                print(e)
            print(chr(27) + "[2J")
            print(self.__str__())
            time.sleep(0.5)


    def set_state(self, state):
        with self._state_lock:
            self._state = state

    def get_state(self):
        with self._state_lock:
            state = self._state
            sense = self._sense
            return state, sense

    def __str__(self):
        with self._state_lock:
            return "Thermostat: sense:{:2.1f} avg:{:2.1f} set:{:2.1f} delta:{:2.1f}degC {}".format(self._sense.deg_c,
                                                                                                       self._sense.avg_deg_c,
                                                                                                       self._state.set_point_deg_c,
                                                                                                       self._sense.deg_c-self._state.set_point_deg_c,
                                                                                                       self._relay)
    def join(self, timeout=None):
        self._stop_event.set()
        super(Thermostat, self).join()