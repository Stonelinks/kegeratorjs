#!/usr/bin/env python3
__author__ = 'nwiles'
import api.api as api
import socket
mock = socket.gethostname() != 'ike'
if mock:
    import ike.ikeStub as ike
else:
    import ike.ike as ike

def main():
    my_ike = ike.Ike(relayPin=17, flow1Pin=23, flow2Pin=24)
    api.launch(my_ike)

if __name__ == "__main__":
    main()

