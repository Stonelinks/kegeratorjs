__author__ = 'nwiles'
from tinydb import TinyDB, where
import time
from enum import Enum

class Event(Enum):
    addKeg=1 #new keg on tap
    finishedKeg=2 #keg is finished
    pouredBeer=3 #someone poured a beer
    sensorSnapshot=4 #current sensor state
    settingsSnapshot=5 #kegerator settings changed
    newUser=6 # added a new user (coming in 1.0)


class Lager:
    def __init__(self, event_log_path):
        self.lastEventId = 0
        self.event_db = TinyDB(event_log_path)
        #cache one of each of the last event types
        self.latestData = {}

    #TODO: this need to be thread safe
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
    def find_events(self, start_time, end_time, type_filter):
        if type_filter is None:
            type_filter = []
        if not hasattr(type_filter, '__iter__'):
            type_filter = [type_filter]  #make a list if not one
        if start_time == 'now':
            #get latest value
            if len(type_filter):
                ret = []
                for t in type_filter:
                    ret.append(self.latestData[t])
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
                filters.append(where('time') >= start_time)
            if end_time is not None and end_time is not 'now':
                filters.append(where('time') <= end_time)
        query = None
        for f in filters:
            if query is None:
                query = f
            else:
                query = f & query
        return self.event_db.search(query)