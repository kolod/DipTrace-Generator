#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Terminal import Terminal, TerminalsMixin, TerminalShape


class TestTerminal(unittest.TestCase):
    def test_001(self):
        terminal = Terminal()

        self.assertIsNone(terminal.shape)
        self.assertIsNone(terminal.x)
        self.assertIsNone(terminal.y)
        self.assertIsNone(terminal.angle)
        self.assertIsNone(terminal.width)
        self.assertIsNone(terminal.height)
        self.assertIsNone(terminal.corner)

    def test_002(self):
        terminal = Terminal(
            xml('<Terminal Shape="Rectangle" X="0.12" Y="0" Angle="0" Width="0.5" Height="1.6" Corner="0.1"/>')
        )

        self.assertEqual(TerminalShape.Rectangle, terminal.shape)
        self.assertEqual(0.12, terminal.x)
        self.assertEqual(0.0, terminal.y)
        self.assertEqual(0.0, terminal.angle)
        self.assertEqual(0.5, terminal.width)
        self.assertEqual(1.6, terminal.height)
        self.assertEqual(0.1, terminal.corner)

        terminal.shape = TerminalShape.Obround

        self.assertEqual(TerminalShape.Obround, terminal.shape)
        self.assertIsNone(terminal.corner)

    def test_003(self):
        terminal = Terminal(
            xml(
                '<Terminal Shape="Polygon" X="0" Y="0" Angle="0" Width="0.1" Height="0.1">\n'
                "  <Points>\n"
                '    <Item X="0.6929" Y="0.287"/>\n'
                '    <Item X="0.6929" Y="-0.287"/>\n'
                '    <Item X="0.287" Y="-0.6929"/>\n'
                '    <Item X="-0.287" Y="-0.6929"/>\n'
                '    <Item X="-0.6929" Y="-0.287"/>\n'
                '    <Item X="-0.6929" Y="0.287"/>\n'
                '    <Item X="-0.287" Y="0.6929"/>\n'
                '    <Item X="0.287" Y="0.6929"/>\n'
                "  </Points>\n"
                "</Terminal>\n"
            )
        )

        self.assertEqual(TerminalShape.Polygon, terminal.shape)
        self.assertEqual(0.0, terminal.x)
        self.assertEqual(0.0, terminal.y)
        self.assertEqual(0.0, terminal.angle)
        self.assertEqual(0.1, terminal.width)
        self.assertEqual(0.1, terminal.height)
        self.assertIsNone(terminal.corner)
        self.assertEqual(8, len(terminal.points))
        self.assertEqual(0.6929, terminal.points[0].x)
        self.assertEqual(0.287, terminal.points[5].y)

        terminal.shape = None

        self.assertIsNone(terminal.shape)

    def test_mixin_001(self):
        class PadStyle(TerminalsMixin):
            pass

        pad_style = PadStyle()

        self.assertListEqual([], pad_style.terminals)

        pad_style.terminals = [
            Terminal(xml('<Terminal Shape="Rectangle" X="0.12" Y="0" Angle="0" Width="0.5" Height="1.6" Corner="0"/>')),
            Terminal(xml('<Terminal Shape="Obround" X="0" Y="0" Angle="0" Width="0.45" Height="0.45"/>')),
        ]

        self.assertEqual(2, len(pad_style.terminals))

        self.assertEqual(0.12, pad_style.terminals[0].x)
        self.assertEqual(0.45, pad_style.terminals[1].width)

        pad_style.terminals = None

        expected = "<PadStyle/>\n"
        actual = str(pad_style)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
