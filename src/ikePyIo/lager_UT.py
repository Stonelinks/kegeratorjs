#!/usr/bin/env python
import unittest
import lager
import os
import time
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
        matches = log.find_events('now', None, lager.Event.addKeg)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['id'], 0)
        self.assertEqual(matches[0]['data']['id'], 1)
        self.assertEqual(matches[0]['data']['beerId'], 5)
        self.assertEqual(matches[0]['data']['litersConsumed'], 0.0)
        self.assertEqual(matches[0]['data']['litersTotal'], 18.9271)
        matches = log.find_events('now', None, None)
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
        matches = log.find_events(time.time()-1, time.time(), lager.Event.pouredBeer)
        self.assertEqual(len(matches), 5)
        time.sleep(1.0)
        matches = log.find_events(time.time()-1, time.time(), lager.Event.pouredBeer)
        self.assertEqual(len(matches), 0)

if __name__ == '__main__':
    unittest.main()