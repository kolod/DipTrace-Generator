#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Group import Group, GroupsMixin


class TestGroup(unittest.TestCase):
    def test_mixin_001(self):
        class Part(GroupsMixin):
            pass

        part = Part()

        self.assertIsNotNone(part.groups)
        self.assertListEqual([], part.groups)

        part.groups = [
            Group(xml('<Group Id="0" X="-7.5017" Y="-6.35"/>')),
            Group(xml('<Group Id="1" X="13.8375" Y="7.62"/>')),
        ]

        self.assertIsNotNone(part.groups)
        self.assertEqual(2, len(part.groups))
        self.assertEqual(0, part.groups[0].id)
        self.assertEqual(-7.5017, part.groups[0].x)
        self.assertEqual(7.62, part.groups[1].y)

        part.groups = None

        self.assertIsNotNone(part.groups)
        self.assertListEqual([], part.groups)


if __name__ == "__main__":
    unittest.main()
