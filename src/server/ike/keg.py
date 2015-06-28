__author__ = 'nwiles'
import threading
import tinydb
import time
import lager

class TinyDBThreadSafe(tinydb.TinyDB):
    def __init__(self, *args, **kwargs):
        super(TinyDBThreadSafe, self).__init__(*args, **kwargs)
        self._state_lock = threading.Lock()


    def __getattr__(self, name, *args, **kwargs):
        with self._state_lock:
            return super(TinyDBThreadSafe, self).__getattr__(name, *args, **kwargs)


class KegManager(threading.Thread):
    def __init__(self,
                 loop_period_s=0.1,
                 flow_meters=[], logger=None):
        #threading
        threading.Thread.__init__(self, name="KegManager")
        self._stop_event = threading.Event()
        #configurable
        self._loop_period_s = loop_period_s
        self._db = TinyDBThreadSafe("kegs.json")
        self._kegs=[]
        for i,f in enumerate(flow_meters):
            self._kegs.append(Keg(i, i, f.get_flow_liters, 0, logger=logger, db=self._db))
        self.start()

    def run(self):
        while not self._stop_event.isSet():
            for k in self._kegs:
                k.loop()
            time.sleep(self._loop_period_s)

    def join(self, timeout=None):
        self._stop_event.set()
        super(KegManager, self).join()

    def dispatch(self, id, funcName, *args, **kwargs):
        fn = getattr(self._kegs[id], funcName)
        if id is not None:
            return fn(*args, **kwargs)
        else:
            return [ret for ret in self._kegs.fn(*args, **kwargs)]

class Keg():
    def __init__(self,
                 id,
                 beer_id,
                 get_flow_liters,
                 pour_threshold_l_per_s=0.05,
                 pour_timeout_s=1.0,
                 loop_period_s=0.1,
                 logger=None,
                 db=None):
        #threading
        self._state_lock = threading.Lock()
        #inputs
        self._id = id
        self._get_flow_liters = get_flow_liters
        #configurable
        self._beer_id = beer_id
        self._consumed_l = 0.0
        self._capacity_l = 17.0
        #internal state
        self._this_pour_l = 0.0
        self._is_pouring = False
        self._flow_meter_last = self._get_flow_liters()
        self._pour_threshold_l_per_s = pour_threshold_l_per_s
        self._loop_period_s = loop_period_s
        self._time_last = time.time()
        self._flow_rate_l_per_s = 0.0
        self._pour_timeout_s = pour_timeout_s
        self._time_last_pouring = self._time_last - self._pour_timeout_s
        self._pour_start_time = self._time_last_pouring
        self._lager = logger
        self._db=db
        #database:
        db_entry = self._db.get(eid=self._id+1)
        if db_entry is None:
            insertId = self._db.insert(self._get_persistant_state())
            print('Inserted {}, id:{}'.format(insertId, self._id))
            assert insertId == self._id+1
            db_entry = self._db.get(eid=self._id+1)
            if db_entry is None:
                raise KeyError()
        self.set_state(db_entry)

    def loop(self):
        with self._state_lock:
            #time
            time_now = time.time()
            delta_t = time_now - self._time_last
            self._time_last = time_now

            #flow
            flow_meter_now = self._get_flow_liters()
            delta_flow = flow_meter_now - self._flow_meter_last
            self._flow_meter_last = flow_meter_now

            #flow rate
            self._flow_rate_l_per_s = delta_flow / delta_t

            if self._flow_rate_l_per_s >= self._pour_threshold_l_per_s:
                if not self._is_pouring:
                    self._is_pouring = True
                    self._pour_start_time = time_now
                self._time_last_pouring = time_now
                self._this_pour_l += delta_flow
                self._consumed_l += delta_flow
            else:
                #reset if not flowing so that we don't count spurious ticks
                self._flow_meter_last = flow_meter_now

            if self._has_pour_stopped(time_now):
                self._on_stop_pour(time_now)
                self._is_pouring = False

    def _has_pour_stopped(self, time_now):
        return (time_now - self._time_last_pouring) >= self._pour_timeout_s

    def _on_stop_pour(self, time_now):
        if self._lager:
            self._lager.log_event(lager.Event.pouredBeer, {'kegId': self._id,
                                                           'beerId': self._beer_id,
                                                           'volumeL':self._this_pour_l,
                                                           'startTime': self._pour_start_time,
                                                           'stopTime': time_now})
        self._db.update(self._get_persistant_state(), eid=self._id+1)


    def _get_persistant_state(self):
        return  {'beerId': self._beer_id,
                 'consumedL': self._consumed_l,
                 'capacityL': self._capacity_l}

    def get_state(self):
        with self._state_lock:
            ret = self._get_persistant_state()
            ret.update({'flowRateLitersPerSec': self._flow_rate_l_per_s})
            return ret


    def set_state(self, state):
        with self._state_lock:
            self._beer_id = state['beerId']
            self._consumed_l = state['consumedL']
            self._capacity_l = state['capacityL']
            self._db.update(self._get_persistant_state(), eids=[self._id+1])

    def __str__(self):
        with self._state_lock:
            return "Keg {}: capacity:{:2.1f}l \
                    consumed:{:2.2f}l ({:2.1f}%) \
                    rate:{:2.1f}l/s isPouring:{}".format(self._id,
                                                         self._capacity_l,
                                                         self._consumed_l,
                                                         (self._capacity_l - self._consumed_l)/self._capacity_l*100.0,
                                                         self._flow_rate_l_per_s,
                                                         self._is_pouring)
