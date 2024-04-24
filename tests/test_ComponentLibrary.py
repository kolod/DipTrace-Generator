#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


import unittest
from DipTraceGenerator import ComponentLibrary


class TestComponentLibrary(unittest.TestCase):
    def test_constructor_none(self):
        actual = ComponentLibrary()
        pass
