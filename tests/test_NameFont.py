#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from DipTraceGenerator import NameFont


class TestNameFont(unittest.TestCase):
    def test_001(self):
        font = NameFont()
        self.assertIsNone(font.size)
        self.assertIsNone(font.width)
        self.assertIsNone(font.scale)
        self.assertEqual("<NameFont/>\n", str(font))

    def test_002(self):
        font = NameFont(size=10, width=-3, scale=0.8)
        self.assertEqual('<NameFont Size="10" Width="-3" Scale="0.8"/>\n', str(font))
        self.assertEqual(10, font.size)
        self.assertEqual(-3, font.width)
        self.assertEqual(0.8, font.scale)

    def test_003(self):
        font = NameFont()
        font.size = 10
        font.width = -3
        font.scale = 0.8
        self.assertEqual('<NameFont Size="10" Width="-3" Scale="0.8"/>\n', str(font))
        self.assertEqual(10, font.size)
        self.assertEqual(-3, font.width)
        self.assertEqual(0.8, font.scale)


if __name__ == "__main__":
    unittest.main()
