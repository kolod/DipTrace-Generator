#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator import PadStyle, MainStackShape, Side, MountType, TerminalShape


class TestPadStyle(unittest.TestCase):
    def test_pad_style_0(self):
        pad_style = PadStyle(xml("<PadStyle/>"))

        self.assertEqual(None, pad_style.name)
        self.assertEqual(None, pad_style.type)
        self.assertEqual(None, pad_style.side)
        self.assertEqual(None, pad_style.main_stack)

        self.assertListEqual([], pad_style.terminals)

    def test_pad_style_1(self):
        pad_style = PadStyle(
            xml(
                '<PadStyle Name="PadT0" Type="Surface" Side="Top">\n'
                '  <MainStack Shape="Rectangle" Width="1.13" Height="1.82" Corner="22.1239"/>\n'
                "  <Terminals>\n"
                '    <Terminal Shape="Rectangle" X="0.12" Y="0" Angle="0" Width="0.5" Height="1.6" Corner="0"/>\n'
                "  </Terminals>\n"
                "</PadStyle>\n"
            )
        )

        self.assertEqual("PadT0", pad_style.name)
        self.assertEqual(MountType.Surface, pad_style.type)
        self.assertEqual(Side.Top, pad_style.side)

        self.assertEqual(MainStackShape.Rectangle, pad_style.main_stack.shape)
        self.assertEqual(1.13, pad_style.main_stack.width)
        self.assertEqual(1.82, pad_style.main_stack.height)
        self.assertEqual(22.1239, pad_style.main_stack.corner)

        self.assertEqual(1, len(pad_style.terminals))
        self.assertEqual(TerminalShape.Rectangle, pad_style.terminals[0].shape)
        self.assertEqual(0.12, pad_style.terminals[0].x)
        self.assertEqual(0.0, pad_style.terminals[0].y)
        self.assertEqual(0.0, pad_style.terminals[0].angle)
        self.assertEqual(0.5, pad_style.terminals[0].width)
        self.assertEqual(1.6, pad_style.terminals[0].height)
        self.assertEqual(0.0, pad_style.terminals[0].corner)
