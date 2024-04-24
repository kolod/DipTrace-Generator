#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.PatternOrigin import PatternOrigin, PatternOriginMixin, Boolean, Visible


class TestPatternOrigin(unittest.TestCase):
    def test_001(self):
        origin = PatternOrigin()

        self.assertIsNone(origin.x)
        self.assertIsNone(origin.y)
        self.assertIsNone(origin.cross)
        self.assertIsNone(origin.circle)
        self.assertIsNone(origin.common)
        self.assertIsNone(origin.courtyard)

    def test_002(self):
        origin = PatternOrigin(xml('<Origin X="-0.2228" Y="0" Cross="Y" Circle="N" Common="Hide" Courtyard="Show"/>'))

        self.assertEqual(-0.2228, origin.x)
        self.assertEqual(0.0, origin.y)
        self.assertEqual(Boolean.Yes, origin.cross)
        self.assertEqual(Boolean.No, origin.circle)
        self.assertEqual(Visible.Hide, origin.common)
        self.assertEqual(Visible.Show, origin.courtyard)

    def test_003(self):
        origin = PatternOrigin(xml('<Origin X="0" Y="2.22" Cross="N" Circle="Y" Common="Show" Courtyard="Hide"/>'))

        self.assertEqual(0.0, origin.x)
        self.assertEqual(2.22, origin.y)
        self.assertEqual(Boolean.No, origin.cross)
        self.assertEqual(Boolean.Yes, origin.circle)
        self.assertEqual(Visible.Show, origin.common)
        self.assertEqual(Visible.Hide, origin.courtyard)

    def test_004(self):
        origin = PatternOrigin(xml('<Origin X="0" Y="2.22" Cross="N" Circle="Y" Common="Show" Courtyard="Hide"/>'))

        origin.x = None
        self.assertIsNone(origin.x)
        self.assertEqual(2.22, origin.y)
        self.assertEqual(Boolean.No, origin.cross)
        self.assertEqual(Boolean.Yes, origin.circle)
        self.assertEqual(Visible.Show, origin.common)
        self.assertEqual(Visible.Hide, origin.courtyard)
        origin.x = 0.0

        origin.y = None
        self.assertEqual(0.0, origin.x)
        self.assertIsNone(origin.y)
        self.assertEqual(Boolean.No, origin.cross)
        self.assertEqual(Boolean.Yes, origin.circle)
        self.assertEqual(Visible.Show, origin.common)
        self.assertEqual(Visible.Hide, origin.courtyard)
        origin.y = 2.22

        origin.cross = None
        self.assertEqual(0.0, origin.x)
        self.assertEqual(2.22, origin.y)
        self.assertIsNone(origin.cross)
        self.assertEqual(Boolean.Yes, origin.circle)
        self.assertEqual(Visible.Show, origin.common)
        self.assertEqual(Visible.Hide, origin.courtyard)
        origin.cross = Boolean.No

        origin.circle = None
        self.assertEqual(0.0, origin.x)
        self.assertEqual(2.22, origin.y)
        self.assertEqual(Boolean.No, origin.cross)
        self.assertIsNone(origin.circle)
        self.assertEqual(Visible.Show, origin.common)
        self.assertEqual(Visible.Hide, origin.courtyard)
        origin.circle = Boolean.Yes

        origin.common = None
        self.assertEqual(0.0, origin.x)
        self.assertEqual(2.22, origin.y)
        self.assertEqual(Boolean.No, origin.cross)
        self.assertEqual(Boolean.Yes, origin.circle)
        self.assertIsNone(origin.common)
        self.assertEqual(Visible.Hide, origin.courtyard)
        origin.common = Visible.Show

        origin.courtyard = None
        self.assertEqual(0.0, origin.x)
        self.assertEqual(2.22, origin.y)
        self.assertEqual(Boolean.No, origin.cross)
        self.assertEqual(Boolean.Yes, origin.circle)
        self.assertEqual(Visible.Show, origin.common)
        self.assertIsNone(origin.courtyard)
        origin.courtyard = Visible.Hide

        self.assertEqual(0.0, origin.x)
        self.assertEqual(2.22, origin.y)
        self.assertEqual(Boolean.No, origin.cross)
        self.assertEqual(Boolean.Yes, origin.circle)
        self.assertEqual(Visible.Show, origin.common)
        self.assertEqual(Visible.Hide, origin.courtyard)

    def test_004(self):
        origin = PatternOrigin()
        origin.x = 0.22
        origin.y = 0.31
        origin.cross = Boolean.Yes
        origin.circle = Boolean.No
        origin.common = Visible.Show
        origin.courtyard = Visible.Hide

        expected = '<Origin X="0.22" Y="0.31" Cross="Y" Circle="N" Common="Show" Courtyard="Hide"/>\n'
        actual = str(origin)

        self.assertEqual(expected, actual)

        origin.circle = None
        origin.common = None
        origin.courtyard = None
        origin.cross = None

        self.assertIsNone(origin.circle)
        self.assertIsNone(origin.common)
        self.assertIsNone(origin.courtyard)
        self.assertIsNone(origin.cross)

    def test_mixin_001(self):
        class Pattern(PatternOriginMixin):
            pass

        pattern = Pattern()

        self.assertIsNone(pattern.origin)

        pattern.origin = PatternOrigin(
            xml('<Origin X="0.22" Y="0.31" Cross="Y" Circle="N" Common="Show" Courtyard="Hide"/>')
        )

        self.assertEqual(0.22, pattern.origin.x)
        self.assertEqual(0.31, pattern.origin.y)
        self.assertEqual(Boolean.Yes, pattern.origin.cross)
        self.assertEqual(Visible.Show, pattern.origin.common)

        pattern.origin = None

        self.assertIsNone(pattern.origin)


if __name__ == "__main__":
    unittest.main()
