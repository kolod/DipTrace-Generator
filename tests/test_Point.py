#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Point import Point, PointsMixin


class TestPoint(unittest.TestCase):
    def test_001(self):
        point = Point(xml("<Item/>"))

        self.assertEqual(None, point.x)
        self.assertEqual(None, point.y)

    def test_002(self):
        point = Point(xml('<Item X="-3.3825" Y="3.3825"/>'))

        self.assertEqual(-3.3825, point.x)
        self.assertEqual(3.3825, point.y)

    def test_003(self):
        point = Point(xml('<Item X="0" Y="-4"/>'))

        self.assertEqual(0.0, point.x)
        self.assertEqual(-4.0, point.y)

    def test_004(self):
        point = Point()
        point.x = 2.5
        point.y = 2.0

        expected = '<Item X="2.5" Y="2"/>\n'
        actual = str(point)

        self.assertEqual(expected, actual)

    def test_005(self):
        point = Point(x=1.0, y=2.5)

        expected = '<Item X="1" Y="2.5"/>\n'
        actual = str(point)

        self.assertEqual(expected, actual)

    def test_mixin_001(self):
        class Shape(PointsMixin):
            pass

        shape = Shape()

        self.assertIsNone(shape.points)

        shape.points = [Point(xml('<Item X="-3.3825" Y="3.3825"/>')), Point(xml('<Item X="0" Y="-4"/>'))]

        self.assertIsNotNone(shape.points)

        self.assertEqual(-3.3825, shape.points[0].x)
        self.assertEqual(-4.0, shape.points[1].y)

        shape.points = None

        self.assertIsNone(shape.points)


if __name__ == "__main__":
    unittest.main()
