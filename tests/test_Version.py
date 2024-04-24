#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from DipTraceGenerator import __version__ as version


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual("0.1.0", version)
