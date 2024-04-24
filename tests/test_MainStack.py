#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.MainStack import MainStack, MainStackMixin
from DipTraceGenerator.Enums import MainStackShape


class TestMainStack(unittest.TestCase):
    def test_001(self):
        main_stack = MainStack(xml("<MainStack/>"))

        self.assertEqual(None, main_stack.shape)
        self.assertEqual(None, main_stack.width)
        self.assertEqual(None, main_stack.height)
        self.assertEqual(None, main_stack.corner)
        self.assertEqual(None, main_stack.x_offset)
        self.assertEqual(None, main_stack.y_offset)

        self.assertEqual(None, main_stack.points)

    def test_002(self):
        main_stack = MainStack(xml('<MainStack Shape="Obround" Width="10" Height="0.5" XOff="0" YOff="0"/>'))

        self.assertEqual(MainStackShape.Obround, main_stack.shape)
        self.assertEqual(10.0, main_stack.width)
        self.assertEqual(0.5, main_stack.height)
        self.assertEqual(None, main_stack.corner)
        self.assertEqual(0.0, main_stack.x_offset)
        self.assertEqual(0.0, main_stack.y_offset)

        self.assertEqual(None, main_stack.points)

    def test_003(self):
        main_stack = MainStack(
            xml('<MainStack Shape="Rectangle" Width="1.5" Height="1.5" XOff="1" YOff="1.2" Corner="1"/>')
        )

        self.assertEqual(MainStackShape.Rectangle, main_stack.shape)
        self.assertEqual(1.5, main_stack.width)
        self.assertEqual(1.5, main_stack.height)
        self.assertEqual(1.0, main_stack.corner)
        self.assertEqual(1.0, main_stack.x_offset)
        self.assertEqual(1.2, main_stack.y_offset)

        self.assertEqual(None, main_stack.points)

    def test_004(self):
        main_stack = MainStack(xml('<MainStack Shape="D-shape" Width="1.5" Height="1.5" XOff="0" YOff="0"/>'))

        self.assertEqual(MainStackShape.DShape, main_stack.shape)
        self.assertEqual(1.5, main_stack.width)
        self.assertEqual(1.5, main_stack.height)
        self.assertEqual(None, main_stack.corner)
        self.assertEqual(0.0, main_stack.x_offset)
        self.assertEqual(0.0, main_stack.y_offset)

        self.assertEqual(None, main_stack.points)

    def test_005(self):
        main_stack = MainStack(
            xml(
                '<MainStack Shape="Polygon" Width="1.4967" Height="1.4967">\n'
                "	<Points>\n"
                '		<Item X="0.7483" Y="0.31"/>\n'
                '		<Item X="0.7483" Y="-0.31"/>\n'
                '		<Item X="0.31" Y="-0.7483"/>\n'
                '		<Item X="-0.31" Y="-0.7483"/>\n'
                '		<Item X="-0.7483" Y="-0.31"/>\n'
                '		<Item X="-0.7483" Y="0.31"/>\n'
                '		<Item X="-0.31" Y="0.7483"/>\n'
                '		<Item X="0.31" Y="0.7483"/>\n'
                "	</Points>\n"
                "</MainStack>\n"
            )
        )

        self.assertEqual(MainStackShape.Polygon, main_stack.shape)
        self.assertEqual(1.4967, main_stack.width)
        self.assertEqual(1.4967, main_stack.height)
        self.assertEqual(None, main_stack.corner)
        self.assertEqual(None, main_stack.x_offset)
        self.assertEqual(None, main_stack.y_offset)

        self.assertEqual(8, len(main_stack.points))
        self.assertEqual(0.7483, main_stack.points[0].x)
        self.assertEqual(-0.31, main_stack.points[1].y)

    def test_006(self):
        main_stack = MainStack(xml('<MainStack Shape="Ellipse" Width="2.2" Height="2.2" XOff="0" YOff="0"/>'))

        self.assertEqual(MainStackShape.Ellipse, main_stack.shape)
        self.assertEqual(2.2, main_stack.width)
        self.assertEqual(2.2, main_stack.height)
        self.assertEqual(None, main_stack.corner)
        self.assertEqual(0.0, main_stack.x_offset)
        self.assertEqual(0.0, main_stack.y_offset)

        self.assertEqual(None, main_stack.points)

    def test_007(self):
        main_stack = MainStack(xml('<MainStack Shape="Ellipse" Width="2.2" Height="2.2" XOff="0" YOff="0"/>'))

        self.assertEqual(MainStackShape.Ellipse, main_stack.shape)

        main_stack.shape = None

        self.assertIsNone(main_stack.shape)

    def test_mixin_001(self):
        class Pattern(MainStackMixin):
            pass

        pattern = Pattern()

        self.assertIsNone(pattern.main_stack)

        pattern.main_stack = MainStack()

        self.assertIsNotNone(pattern.main_stack)
        self.assertIsNone(pattern.main_stack.shape)
        self.assertIsNone(pattern.main_stack.width)
        self.assertIsNone(pattern.main_stack.height)
        self.assertIsNone(pattern.main_stack.corner)
        self.assertIsNone(pattern.main_stack.x_offset)
        self.assertIsNone(pattern.main_stack.y_offset)

        pattern.main_stack.shape = MainStackShape.Obround
        pattern.main_stack.width = 2.5
        pattern.main_stack.height = 2
        pattern.main_stack.x_offset = 0.1
        pattern.main_stack.y_offset = 0.2
        pattern.main_stack.corner = 0.5

        self.assertEqual(MainStackShape.Obround, pattern.main_stack.shape)
        self.assertEqual(2.5, pattern.main_stack.width)
        self.assertEqual(2.0, pattern.main_stack.height)
        self.assertEqual(0.1, pattern.main_stack.x_offset)
        self.assertEqual(0.2, pattern.main_stack.y_offset)
        self.assertEqual(0.5, pattern.main_stack.corner)

        expected = (
            "<Pattern>\n"
            '  <MainStack Shape="Obround" Width="2.5" Height="2" XOff="0.1" YOff="0.2" Corner="0.5"/>\n'
            "</Pattern>\n"
        )
        actual = str(pattern)
        self.assertEqual(expected, actual)

        pattern.main_stack = None

        self.assertIsNone(pattern.main_stack)


if __name__ == "__main__":
    unittest.main()
