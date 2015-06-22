__author__ = 'nwiles'
import threading
import time
import runningMean
import lager
import tinydb

class ThermostatState:
    def __init__(self, set_point_deg_c=0, dead_band_deg_c=0, on_adds_heat=False):
        self.set_point_deg_c = set_point_deg_c
        self.dead_band_deg_c = dead_band_deg_c
        self.on_adds_heat = on_adds_heat

    def to_json(self):
        return {"setPointDegC": self.set_point_deg_c,
                "deadBandDegC": self.dead_band_deg_c,
                'onAddsHeat': self.on_adds_heat}

    def from_json(self, value):
        self.set_point_deg_c = value['setPointDegC']
        self.dead_band_deg_c = value['deadBandDegC']
        self.on_adds_heat = value['onAddsHeat']
        return self

class ThermostatSense:
    def __init__(self, deg_c, avg_deg_c):
        self.deg_c = deg_c
        self.avg_deg_c = avg_deg_c

    def to_json(self):
        return {"degC":self.deg_c,
                "avgDegC":self.avg_deg_c}

class Thermostat(threading.Thread):
    def __init__(self, temp_input_fn, relay, on_adds_heat, logger):
        threading.Thread.__init__(self, name="Thermostat")
        self._logger = logger
        self._db = tinydb.TinyDB("thermostat.json")
        if len(self._db.all()) is 0:
            initial_state = ThermostatState(set_point_deg_c=2.5, dead_band_deg_c=2, on_adds_heat=on_adds_heat)
            self._db.insert(initial_state.to_json())
        self._getTempInput_DegC = temp_input_fn
        self._sense = ThermostatSense(0, 0)
        self._avg_deg_c = runningMean.RunningMean(1000)
        self._relay = relay
        self._outputSetting=False
        self._state_lock = threading.Lock()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.isSet():
            self.loop()
            time.sleep(5.0)

    def loop(self):
        try:
            new_reading_deg_c = self._getTempInput_DegC()
            with self._state_lock:
                inputs = ThermostatState()
                inputs.from_json(value=self._db.all()[0])
                self._sense.deg_c = new_reading_deg_c
                self._avg_deg_c.add_val(new_reading_deg_c)
                self._sense.avg_deg_c = self._avg_deg_c.get_avg()
                #run logic:
                if self._sense.deg_c > inputs.set_point_deg_c+inputs.dead_band_deg_c:
                    # too warm
                    self._outputSetting = not inputs.on_adds_heat
                elif self._sense.deg_c < inputs.set_point_deg_c-inputs.dead_band_deg_c:
                    # too cold
                    self._outputSetting = inputs.on_adds_heat
                self._relay(self._outputSetting)
                self._logger.log_event(lager.Event.thermostatSense, self._sense.to_json())
        except Exception as e:
            print("Thermostat: error reading temp or setting output")
            print(e)

    def set_state(self, state):
        with self._state_lock:
            state_json = state.to_json()
            self._db.update(state_json, eids=[1])
            self._logger.log_event(lager.Event.thermostatSettings, state_json)

    def get_state(self):
        with self._state_lock:
            return ThermostatState.from_json(self._db.all()[0])

    def get_sense(self):
        with self._state_lock:
            sense = self._sense
            return sense.deepcopy()

    def __str__(self):
        with self._state_lock:
            inputs = ThermostatState.from_json(self._db.all()[0])
            return "Thermostat: sense:{:2.1f} \
                    avg:{:2.1f} \
                    set:{:2.1f} \
                    delta:{:2.1f}degC {}".format(self._sense.deg_c,
                                                 self._sense.avg_deg_c,
                                                 inputs.set_point_deg_c,
                                                 self._sense.deg_c-inputs.set_point_deg_c,
                                                 self._relay)
    def join(self, timeout=None):
        self._stop_event.set()
        super(Thermostat, self).join()