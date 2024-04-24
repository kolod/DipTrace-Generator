#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.SpiceModel import SpiceModel, SpiceModelType, SpiceModelMixin


class TestSpiceModel(unittest.TestCase):
    def test_001(self):
        spice = SpiceModel()
        self.assertIsNone(spice.type)
        self.assertIsNone(spice.model)
        self.assertIsNone(spice.details)

    def test_002(self):
        spice = SpiceModel(
            xml(
                '<SpiceModel Type="Voltage-Controlled Switch">\n'
                "    <Model>[][-1][*0**1*Initial!State(ON,OFF)= ]</Model>\n"
                "    <Details>\n"
                "        <Item>.model ModelName</Item>\n"
                "        <Item>+ (</Item>\n"
                "        <Item>+ )</Item>\n"
                "    </Details>\n"
                "</SpiceModel>\n"
            )
        )

        self.assertEqual(SpiceModelType.VoltageControlledSwitch, spice.type)
        self.assertEqual("[][-1][*0**1*Initial!State(ON,OFF)= ]", spice.model)
        self.assertListEqual([".model ModelName", "+ (", "+ )"], spice.details)

        spice.details = None
        self.assertIsNone(spice.details)

        spice.type = None
        self.assertIsNone(spice.type)

        spice.model = None
        self.assertIsNone(spice.model)

        spice.details = []
        self.assertListEqual([], spice.details)

    def test_003(self):
        spice = SpiceModel()
        spice.type = SpiceModelType.VoltageControlledSwitch
        spice.model = "[][-1][*0**1*Initial!State(ON,OFF)= ]"
        spice.details = [".model ModelName", "+ (", "+ )"]

        expected = (
            '<SpiceModel Type="Voltage-Controlled Switch">\n'
            "  <Model>[][-1][*0**1*Initial!State(ON,OFF)= ]</Model>\n"
            "  <Details>\n"
            "    <Item>.model ModelName</Item>\n"
            "    <Item>+ (</Item>\n"
            "    <Item>+ )</Item>\n"
            "  </Details>\n"
            "</SpiceModel>\n"
        )
        actual = str(spice)
        self.assertEqual(expected, actual)

    def test_mixin(self):
        class Part(SpiceModelMixin):
            pass

        part = Part()

        self.assertIsNone(part.spice)

        part.spice = SpiceModel(
            type=SpiceModelType.VoltageControlledSwitch,
            model="[][-1][*0**1*Initial!State(ON,OFF)= ]",
            details=[".model ModelName", "+ (", "+ )"],
        )

        self.assertEqual(SpiceModelType.VoltageControlledSwitch, part.spice.type)
        self.assertEqual("[][-1][*0**1*Initial!State(ON,OFF)= ]", part.spice.model)
        self.assertListEqual([".model ModelName", "+ (", "+ )"], part.spice.details)

        part.spice = None
        self.assertIsNone(part.spice)


if __name__ == "__main__":
    unittest.main()
