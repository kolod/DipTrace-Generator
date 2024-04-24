#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Hole import HolesMixin, Hole


class TestDimension(unittest.TestCase):
    def test_mixin_001(self):
        class Pattern(HolesMixin):
            pass

        pattern = Pattern()

        self.assertIsNotNone(pattern.holes)
        self.assertListEqual([], pattern.holes)

        pattern.holes = [Hole(id=0), Hole(id=1)]
        self.assertIsNotNone(pattern.holes)
        self.assertEqual(2, len(pattern.holes))

        pattern.holes = None
        self.assertIsNotNone(pattern.holes)
        self.assertListEqual([], pattern.holes)


if __name__ == "__main__":
    unittest.main()
