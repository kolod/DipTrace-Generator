#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from DipTraceGenerator import Units


class TestDipTraceEnum(unittest.TestCase):
    def test_units_1(self):
        expected = Units.mil
        actual = Units("mil")
        self.assertEqual(expected, actual)

    def test_units_2(self):
        expected = "mil"
        actual = Units.mil.value
        self.assertEqual(expected, actual)

    def test_units_3(self):
        expected = Units.mm
        actual = Units.default
        self.assertEqual(expected, actual)

    def test_units_4(self):
        expected = Units.mm
        actual = Units["mm"]
        self.assertEqual(expected, actual)
