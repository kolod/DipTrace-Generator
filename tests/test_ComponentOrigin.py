#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.ComponentOrigin import ComponentOrigin, ComponentOriginMixin


class TestComponentOrigin(unittest.TestCase):
    def test_001(self):
        origin = ComponentOrigin()

        self.assertEqual(None, origin.x)
        self.assertEqual(None, origin.y)

    def test_002(self):
        origin = ComponentOrigin(xml('<Origin X="0" Y="0"/>'))

        self.assertEqual(0.0, origin.x)
        self.assertEqual(0.0, origin.y)

    def test_003(self):
        origin = ComponentOrigin()
        origin.x = 1.0
        origin.y = -2.0

        expected = '<Origin X="1" Y="-2"/>\n'
        actual = str(origin)

        self.assertEqual(expected, actual)

    def test_mixin_001(self):
        class Component(ComponentOriginMixin):
            pass

        component = Component()

        self.assertIsNone(component.origin)

        component.origin = ComponentOrigin(x=1.5, y=2.0)
        self.assertIsNotNone(component.origin)
        self.assertEqual(1.5, component.origin.x)
        self.assertEqual(2.0, component.origin.y)

        component.origin = None
        self.assertIsNone(component.origin)


if __name__ == "__main__":
    unittest.main()
