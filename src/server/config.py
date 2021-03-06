#!/usr/bin/env python2
from __future__ import absolute_import, division, print_function
__author__ = 'ldoyle'
import socket
import os.path

def make_file_abspath(filename):
  return os.path.join(os.path.dirname(__file__), filename)

#Note these pinouts are BROADCOM pin numbers, not Rasbery PI IDC pin connector numbers
RELAY_PIN = 17
FLOW_1_PIN = 23
FLOW_2_PIN = 24

STATIC_FILES=make_file_abspath('../../build')
FLASK_DEBUG = False
DB_ROOT = '/home/pi/' if socket.gethostname() == 'ike' else make_file_abspath('../../sampledata')
