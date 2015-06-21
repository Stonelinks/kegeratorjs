__author__ = 'nwiles'
#!/usr/bin/env python
import unittest
import requests
import json

host_addr = 'http://localhost:5000'

class TestApi(unittest.TestCase):
    def post(self, url, payload):
        header = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=header)
        try:
            id = r.json()['id']
        except KeyError:
            id = 0
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
        return r, r.status_code

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
                   'costPerPint':1.40}
        id, status = self.post(host_addr + '/beers/',  payload)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/beers/' + str(id))
        self.assertEqual(reply.json()['data'], payload)

        #put
        delta =  {'name': 'Nic W'}
        reply, status = self.put(host_addr+'/beers/'+ str(id), delta)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/beers/' + str(id))
        self.assertEqual(status, 200)
        self.assertEqual(reply.json()['data']['name'], 'Nic W')

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
        id, status = self.put(host_addr + '/kegs/0',  payload)
        self.assertEqual(status, 400)
        #bad field
        payload = {'beerId': 5,
                   'litersRemaining': 'a',
                   'litersCapacity': 1.0}
        reply, status = self.put(host_addr + '/kegs/0',  payload)
        self.assertEqual(status, 400)
        #bad field
        payload = {'beerId': 5,
                   'litersRemaining': 0.0,
                   'litersCapacity': 'a'}
        reply, status = self.put(host_addr + '/kegs/0',  payload)
        self.assertEqual(status, 400)
        #succeed:
        payload = {'beerId': 5,
                   'litersRemaining': 0.0,
                   'litersCapacity': 1.0}
        reply, status = self.put(host_addr + '/kegs/0',  payload)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/kegs/0')
        self.assertEqual(reply.json()['data'], payload)

        #put
        delta =  {'beerId': 6,
                  'litersCapacity': 3.0}
        reply, status = self.put(host_addr+'/kegs/0', delta)
        self.assertEqual(status, 200)

        payload.update(delta)

        reply, status = self.get(host_addr + '/kegs/0' )
        self.assertEqual(status, 200)
        self.assertEqual(reply.json()['data'], payload)

        delta = {'beerId': 6,
                'litersCapacity': 'b'}
        reply, status = self.put(host_addr+'/kegs/0', delta)
        self.assertEqual(status, 400)

        delta = {'beerId': 7}
        reply, status = self.put(host_addr+'/kegs/0', delta)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/kegs/0' )
        self.assertEqual(reply.json()['data']['beerId'], 7)
        self.assertEqual(status, 200)


    def test_users(self):
        #succeed:
        payload = {'name': 'Nic',
                   'email': 'nhwiles@gmail.com',
                   'rfidId': '1',
                   'nfcId':'',
                    'rfidId':'',
                    'untappedName':''}
        id, status = self.post(host_addr + '/users/',  payload)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/users/' + str(id))
        self.assertEqual(reply.json()['data'], payload)

        #put
        delta =  {'name': 'Nic W'}
        reply, status = self.put(host_addr+'/users/'+ str(id), delta)
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/users/' + str(id))
        self.assertEqual(status, 200)
        self.assertEqual(reply.json()['data']['name'], 'Nic W')

        #delete
        status = self.delete(host_addr+'/users/'+ str(id))
        self.assertEqual(status, 200)
        reply, status = self.get(host_addr + '/users/' + str(id))
        self.assertEqual(status, 404)
        status = self.delete(host_addr+'/users/'+ str(id))
        self.assertEqual(status, 404)

if __name__ == '__main__':
    unittest.main()

