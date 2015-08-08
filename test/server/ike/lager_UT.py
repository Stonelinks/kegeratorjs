#!/usr/bin/env python3
import unittest
import ike.lager as lager
import os
import time
import tinydb

class TestLager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLager, self).__init__(*args, **kwargs)
        self.db_file = "temp.temp"
    def test_addKeg(self):
        try:
            os.remove(self.db_file)
        except:
            pass
        log = lager.Lager(self.db_file)
        log.log_event(lager.Event.addKeg, {'id':1, 'beerId':5, 'litersConsumed':0.0, 'litersTotal':18.9271})
        log.log_event(lager.Event.pouredBeer, {'id':5, 'litersConsumed':0.5})
        matches = log.find_events(lager.Event.addKeg, 'now', None)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['data']['id'], 1)
        self.assertEqual(matches[0]['data']['beerId'], 5)
        self.assertEqual(matches[0]['data']['litersConsumed'], 0.0)
        self.assertEqual(matches[0]['data']['litersTotal'], 18.9271)
        matches = log.find_events("", 'now', None)
        self.assertEqual(len(matches), 2)

    def test_searchHistory(self):
        try:
            os.remove(self.db_file)
        except:
            pass
        log = lager.Lager(self.db_file)
        log.log_event(lager.Event.pouredBeer, {'id':5, 'litersConsumed':0.5})
        log.log_event(lager.Event.pouredBeer, {'id':5, 'litersConsumed':0.4})
        log.log_event(lager.Event.pouredBeer, {'id':5, 'litersConsumed':0.3})
        log.log_event(lager.Event.pouredBeer, {'id':5, 'litersConsumed':0.2})
        log.log_event(lager.Event.pouredBeer, {'id':5, 'litersConsumed':0.1})
        matches = log.find_events(lager.Event.pouredBeer, time.time()-1, time.time())
        log.find_events(None, None, None)
        self.assertEqual(len(matches), 5)
        time.sleep(1.0)
        matches = log.find_events(lager.Event.pouredBeer, time.time()-1, time.time())
        self.assertEqual(len(matches), 0)

    def test_circular_db(self):
        try:
            os.remove(self.db_file)
        except:
            pass
        event_db = tinydb.TinyDB(self.db_file, storage=tinydb.middlewares.CachingMiddleware(tinydb.storages.JSONStorage))
        event_db.table_class=lager.CircularTable
        tbl = event_db.table('test', max_size=4)
        tbl.insert({'foo':'1'})
        tbl.insert({'foo':'2'})
        tbl.insert({'foo':'3'})
        tbl.insert({'foo':'4'})
        tbl.insert({'foo':'5'})
        tbl.insert({'foo':'6'})
        values = tbl.all()
        self.assertEqual(len(values), 4)
        expected = [{'foo':'3'}, {'foo':'4'}, {'foo':'5'}, {'foo':'6'}]
        print(tbl.all())

        four = tbl.search((tinydb.where('foo') == '4'))
        tbl.remove(eids=[four[0].eid])
        values = tbl.all()
        self.assertEqual(len(values), 3)
        print(tbl.all())

        tbl.insert({'foo':'7'})
        expected = [{'foo':'5'}, {'foo':'6'}, {'foo':'7'}]
        values = tbl.all()
        print(tbl.all())
        self.assertEqual(len(values), 3)


if __name__ == '__main__':
    unittest.main()