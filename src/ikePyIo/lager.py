__author__ = 'nwiles'
from tinydb import TinyDB, where
import time
import threading

class Event():
    addKeg='addKeg' #new keg on tap
    finishedKeg='finishedKeg' #keg is finished
    pouredBeer='pouredBeer' #someone poured a beer
    sensors='sensor' #current sensor state
    settings='setting' #kegerator settings changed
    newUser='newUser' # added a new user (coming in 1.0)

class Lager:
    def __init__(self, event_log_path):
        self.lastEventId = 0
        self.event_db = TinyDB(event_log_path)
        #cache one of each of the last event types
        self.latestData = {}
        self._api_lock = threading.Lock()

    def __del__(self):
        self.event_db.close()

    def log_event(self, type, data):
            this_entry = {'id': self.lastEventId,
                          'type': str(type),
                          'time': time.time(),
                          'data': data}
            self.latestData.update({type: this_entry})
            #TODO: need this to be unique across runs?
            self.lastEventId+=1
            #TODO: need to determine when to log to file...likely need to decimate?
            self.event_db.insert(this_entry)

    #TODO: this need to be thread safe
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
                    return ret
                else:
                    return self.latestData.values()
            else:
                #search log history
                filters = []
                if type_filter is not None:
                    for t in type_filter:
                        filters.append (where('type') == str(t))
                if start_time is not None:
                    filters.append(where('time') >= float(start_time))
                if end_time is not None and end_time is not 'now':
                    filters.append(where('time') <= float(end_time))
            query = None
            for f in filters:
                if query is None:
                    query = f
                else:
                    query = f & query
            if query:
                return self.event_db.search(query)
            else:
                return self.event_db.all()