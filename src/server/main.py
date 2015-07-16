#!/usr/bin/env python3
__author__ = 'nwiles'
import api.api as api
import socket
mock = socket.gethostname() != 'ike'
if mock:
    import ike.ikeStub as ike
else:
    import ike.ike as ike

my_ike = ike.Ike()
api.launch(my_ike)
