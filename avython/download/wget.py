#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import


from avython.download.driver import BaseDriver


class Driver(BaseDriver):
    command_to_get = 'wget -t 3 {} -O {}'
