#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Pad import Pad, PadsMixin
from DipTraceGenerator.Enums import Boolean, Side


class TestPad(unittest.TestCase):
    def test_001(self):
        pad = Pad()

        self.assertEqual(None, pad.style)
        self.assertEqual(None, pad.id)
        self.assertEqual(None, pad.x)
        self.assertEqual(None, pad.y)
        self.assertEqual(None, pad.angle)
        self.assertEqual(None, pad.locked)
        self.assertEqual(None, pad.side)
        self.assertEqual(None, pad.number)

    def test_002(self):
        pad = Pad(
            xml(
                '<Pad Id="1" Style="PadT1" X="-1.47" Y="0" Angle="0" Locked="N" Side="Top">\n'
                "  <Number>1</Number>\n"
                "</Pad>\n"
            )
        )

        self.assertEqual("PadT1", pad.style)
        self.assertEqual(1, pad.id)
        self.assertEqual(-1.47, pad.x)
        self.assertEqual(0.0, pad.y)
        self.assertEqual(0.0, pad.angle)
        self.assertEqual(Boolean.No, pad.locked)
        self.assertEqual(Side.Top, pad.side)
        self.assertEqual("1", pad.number)

    def test_003(self):
        pad = Pad(
            xml(
                '<Pad Id="4" Style="PadT5" X="-2.143" Y="-3.1387" Angle="1.5708" Locked="Y" Side="Bottom">\n'
                "	<Number>4</Number>\n"
                "</Pad>\n"
            )
        )

        self.assertEqual("PadT5", pad.style)
        self.assertEqual(4, pad.id)
        self.assertEqual(-2.143, pad.x)
        self.assertEqual(-3.1387, pad.y)
        self.assertEqual(1.5708, pad.angle)
        self.assertEqual(Boolean.Yes, pad.locked)
        self.assertEqual(Side.Bottom, pad.side)
        self.assertEqual("4", pad.number)

    def test_mixin_001(self):
        class Pattern(PadsMixin):
            pass

        pattern = Pattern()

        self.assertListEqual([], pattern.pads)

        pattern.pads = [
            Pad(
                xml(
                    '<Pad Id="4" Style="PadT4" X="-2.143" Y="-3.1387" Angle="1.5708" Locked="Y" Side="Bottom">\n'
                    "	<Number>4</Number>\n"
                    "</Pad>\n"
                )
            ),
            Pad(
                xml(
                    '<Pad Id="4" Style="PadT5" X="2.143" Y="3.1387" Angle="0" Locked="Y" Side="Bottom">\n'
                    "	<Number>4</Number>\n"
                    "</Pad>\n"
                )
            ),
        ]

        self.assertEqual(2, len(pattern.pads))
        self.assertEqual("PadT4", pattern.pads[0].style)
        self.assertEqual(2.143, pattern.pads[1].x)

        pattern.pads = None

        self.assertListEqual([], pattern.pads)

        pattern.pads = []

        self.assertListEqual([], pattern.pads)


if __name__ == "__main__":
    unittest.main()
