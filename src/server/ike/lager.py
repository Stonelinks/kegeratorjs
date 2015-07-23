__author__ = 'nwiles'
import tinydb
import tinydb.middlewares
import tinydb.storages
import time
import threading
import copy

class Event():
    addKeg='addKeg' #new keg on tap
    finishedKeg='finishedKeg' #keg is finished
    pouredBeer='pouredBeer' #someone poured a beer
    thermostatSense='thermostatSense' #thermostat sense changed
    thermostatSettings='thermostatSettings' #thermostat settings changed
    newUser='newUser' # added a new user (coming in 1.0)

class Lager:
    def __init__(self, event_log_path):
        self.event_db = tinydb.TinyDB(event_log_path, storage=tinydb.middlewares.CachingMiddleware(tinydb.storages.JSONStorage))
        #cache one of each of the last event types
        self.latestData = {}
        self._api_lock = threading.Lock()

    def __del__(self):
        self.event_db.close()

    def log_event(self, type, data):
        with self._api_lock:
            this_entry = {'type': str(type),
                          'time': time.time(),
                          'data': data}
            self.latestData.update({type: this_entry})
            self.event_db.insert(this_entry)

    def find_events(self, type_filter, start_time, end_time=None):
        with self._api_lock:
            if type_filter is None:
                type_filter = ""
            type_filter = [x for x in type_filter.split(',') if x]
            if start_time == 'now':
                #get latest value
                if len(type_filter):
                    ret = []
                    for t in type_filter:
                        try:
                            ret.append(self.latestData[t])
                        except KeyError:
                            pass
                    return copy.deepcopy(ret)
                else:
                    return copy.deepcopy(self.latestData.values())
            else:
                #search log history
                filters = []
                if type_filter is not None:
                    for t in type_filter:
                        filters.append (tinydb.where('type') == str(t))
                if start_time is not None:
                    filters.append(tinydb.where('time') >= float(start_time))
                if end_time is not None and end_time is not 'now':
                    filters.append(tinydb.where('time') <= float(end_time))
            query = None
            for f in filters:
                if query is None:
                    query = f
                else:
                    query = f & query
            if query:
                return copy.deepcopy(self.event_db.search(query))
            else:
                return copy.deepcopy(self.event_db.all())