#!/usr/bin/env python
__author__ = 'nwiles'
import unittest
import requests
import json
import subprocess
import time

host_addr = 'http://localhost:5000/api/v1'

class TestApi(unittest.TestCase):
    def setUp(self):
        self.apiProc = subprocess.Popen('./src/server/main.py')
        time.sleep(0.5)

    def tearDown(self):
        self.apiProc.terminate()

    def post(self, url, payload):
        header = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=header)
        id=0
        try:
            id = r.json()['id']
        except ValueError:
            pass
        except KeyError:
            pass
        return id, r.status_code

    def put(self, url, payload):
        header = {'Content-type': 'application/json'}
        r = requests.put(url, data=json.dumps(payload), headers=header)
        try:
            reply = r.json()
        except:
            reply = {}
        return reply, r.status_code

    def get(self, url):
        r = requests.get(url)
        try:
            reply = r.json()
        except:
            reply = {}
        return reply, r.status_code

    def delete(self, url):
        header = {'Content-type': 'application/json'}
        r = requests.delete(url)
        return r.status_code

    def test_beers(self):
        #succeed:
        payload = {'name': 'Nic',
                   'description': 'This is a description of a beer',
                   'brewedBy': 'Nic Wiles',
                   'style':'IPA',
                   'abv':5.9,
                   'rating':4.9,
                   'srm':30,
                   'costPerPint':1.40,
                   'ibu':100}
        id, status = self.post(host_addr + '/beers/',  payload)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/beers/' + str(id))
        payload['id'] = id
        self.assertEqual(reply, payload)

        #put
        delta =  {'name': 'Nic W'}
        reply, status = self.put(host_addr+'/beers/'+ str(id), delta)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/beers/' + str(id))
        self.assertEqual(status, 200)
        self.assertEqual(reply['name'], 'Nic W')

        #delete
        status = self.delete(host_addr+'/beers/'+ str(id))
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/beers/' + str(id))
        self.assertEqual(status, 404)
        status = self.delete(host_addr+'/beers/'+ str(id))
        self.assertEqual(status, 404)


    def test_kegs(self):
        #post
        payload = {'beerId': 'a'}
        id, status = self.put(host_addr + '/kegs/1',  payload)
        self.assertEqual(status, 400)
        #bad field
        payload = {'beerId': 5,
                   'consumedL': 'a',
                   'capacityL': 1.0}
        reply, status = self.put(host_addr + '/kegs/1',  payload)
        self.assertEqual(status, 400)
        #bad field
        payload = {'beerId': 5,
                   'consumedL': 0.0,
                   'capacityL': 'a'}
        reply, status = self.put(host_addr + '/kegs/1',  payload)
        self.assertEqual(status, 400)
        #succeed:
        payload = {'beerId': 5,
                   'consumedL': 0.0,
                   'capacityL': 1.0}
        reply, status = self.put(host_addr + '/kegs/1',  payload)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/kegs/1')
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)

        #put
        delta =  {'beerId': 6,
                  'capacityL': 3.0}
        reply, status = self.put(host_addr+'/kegs/1', delta)
        self.assertEqual(status, 200)

        payload.update(delta)

        reply, status = self.get(host_addr + '/kegs/1' )
        self.assertEqual(status, 200)
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)

        delta = {'beerId': 6,
                'capacityL': 'b'}
        reply, status = self.put(host_addr+'/kegs/1', delta)
        self.assertEqual(status, 400)

        delta = {'beerId': 7}
        reply, status = self.put(host_addr+'/kegs/1', delta)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/kegs/1' )
        self.assertEqual(reply['beerId'], 7)
        self.assertEqual(status, 200)


    def test_users(self):
        #succeed:
        payload = { 'name': 'Nic',
                    'email': 'nhwiles@gmail.com',
                    'nfcId':'',
                    'rfidId':'',
                    'untappedName':''}
        id, status = self.post(host_addr + '/users/',  payload)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/users/' + str(id))
        self.assertEqual(status, 200)
        payload['id'] = id
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)

        #put
        delta =  {'name': 'Nic W'}
        reply, status = self.put(host_addr+'/users/'+ str(id), delta)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/users/' + str(id))
        self.assertEqual(status, 200)
        self.assertEqual(reply['name'], 'Nic W')

        #delete
        status = self.delete(host_addr+'/users/'+ str(id))
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/users/' + str(id))
        self.assertEqual(status, 404)
        status = self.delete(host_addr+'/users/'+ str(id))
        self.assertEqual(status, 404)

    def test_thermostat(self):
        #put should succeed:
        payload = { "setPointDegC": 2.0,
                    "deadBandDegC": 1.0,
                    "onAddsHeat": True}
        reply, status = self.put(host_addr + '/thermostat/',  payload)
        self.assertEqual(status, 200)
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)

        #change set point:
        payload["setPointDegC"] = 0.0
        reply, status = self.put(host_addr + '/thermostat/',  payload)
        self.assertEqual(status, 200)
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)

        #change deadband:
        payload["deadBandDegC"]= 2.0
        reply, status = self.put(host_addr + '/thermostat/',  payload)
        self.assertEqual(status, 200)
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)

        #change on adds heat:
        payload["onAddsHeat"]= False
        reply, status = self.put(host_addr + '/thermostat/',  payload)
        self.assertEqual(status, 200)
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)

        #GET==PUT
        reply, status = self.get(host_addr + '/thermostat/')
        self.assertEqual(status, 200)
        self.assertEqual(set(payload.items()).issubset( set(reply.items()) ), True)


        #post should fail
        reply, status = self.post(host_addr+'/thermostat/', payload)
        self.assertEqual(status, 405)

        #delete should fail
        status = self.delete(host_addr+'/thermostat/')
        self.assertEqual(status, 405)


if __name__ == '__main__':
    unittest.main()
