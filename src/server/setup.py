#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
__author__ = 'nwiles'
from distutils.core import setup

setup(name='ike',
      version='1.0',
      description='Modules for building a web-enabled smart kegerator',
      author='Nicholas Wiles',
      author_email='nhwiles@gmail.com',
      url='http://www.nicholaswiles.com',
      packages=['ike', 'api'],
      )
