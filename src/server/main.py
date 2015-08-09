#!/usr/bin/env python2
from __future__ import absolute_import, division, print_function
import api.api as api
import socket
import sys
__author__ = 'nwiles'

mock = socket.gethostname() != 'ike'
if mock:
    import ike.ikeStub as ike
else:
    import ike.ike as ike

print("*** Starting ike ***", file=sys.stderr)
my_ike = ike.Ike()
api.launch(my_ike)
