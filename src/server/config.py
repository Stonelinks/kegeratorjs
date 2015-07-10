#!/usr/bin/env python3
__author__ = 'ldoyle'
import socket
import os.path

def make_file_abspath(filename):
  return os.path.join(os.path.dirname(__file__), filename)

RELAY_PIN = 17
FLOW_1_PIN = 23
FLOW_2_PIN = 24

STATIC_FILES=make_file_abspath('../../build')

DB_ROOT = '/home/pi/' if socket.gethostname() is 'ike' else make_file_abspath('../../sampledata')
