__author__ = 'nwiles'
import tinydb
import tinydb.middlewares
import tinydb.storages
import time
import threading
import copy
import math

class CircularTable(tinydb.database.Table):
    """
    A Table that keeps a limited number of entries.

    Provides the same methods as :class:`~tinydb.database.Table`.

    The query cache gets updated on insert/update/remove. Useful when in cases
    where many searches are done but data isn't changed often.
    """
    def __init__(self, name, db, max_size):
        super(CircularTable, self).__init__(name, db)
        self._max_size = max_size

    def insert(self, element):
        """
        Insert a new element into the table, overwriting the oldest data if we are at capacity

        :param element: the element to insert
        :returns: the inserted element's ID
        """
        data = self._read()
        eid = self._get_next_id()
        if eid > self._max_size:
            eid = min(i for i in data.keys())
            self._last_id = eid
        data[eid] = element
        self._write(data)

        return eid

class Event():
    addKeg='addKeg' #new keg on tap
    finishedKeg='finishedKeg' #keg is finished
    pouredBeer='pouredBeer' #someone poured a beer
    thermostatSense='thermostatSense' #thermostat sense changed
    thermostatSettings='thermostatSettings' #thermostat settings changed
    newUser='newUser' # added a new user (coming in 1.0)

def temp_sense_is_note_worthy(lastSample, thisSample):
    return math.fabs(lastSample['data']['degC'] - thisSample['data']['degC']) >= 0.2

class Lager:
    MAX_TABLE_SIZE=1000
    def __init__(self, event_log_path):
        #create a DB for each type
        self.event_db = tinydb.TinyDB(event_log_path, storage=tinydb.middlewares.CachingMiddleware(tinydb.storages.JSONStorage))
        self.event_db.table_class = CircularTable
        #cache one of each of the last event types
        self.latestData = {}
        self._api_lock = threading.Lock()
        self._downsample_policy = {}
        self._downsample_policy[Event.thermostatSense] = temp_sense_is_note_worthy
    def __del__(self):
        self.event_db.close()

    def log_event(self, type, data):
        with self._api_lock:
            this_entry = {'type': str(type),
                          'time': time.time(),
                          'data': data}
            try:
                log_it = self._downsample_policy[type](self.latestData[type], this_entry)
            except KeyError:
                log_it=True;
            if log_it:
                self.latestData.update({type: this_entry})
            table = self.event_db.table(str(type), max_size=Lager.MAX_TABLE_SIZE)
            table.insert(this_entry)

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
                    return copy.deepcopy(self.latestData).values()
            else:
                #search log history
                filters = []
                tables = []
                if type_filter is not None:
                    for t in type_filter:
                        if t in self.event_db.tables():
                            tables.append(t)
                else:
                    tables = self.event_db.tables()
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
            results = []
            for t in tables:
                table = self.event_db.table(t)
                if query:
                    results += (table.search(query))
                else:
                    results += (table.all())

        return copy.deepcopy(results)