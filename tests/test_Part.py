#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Part import Part, PartsMixin


class TestPart(unittest.TestCase):
    def test_001(self):
        part = Part()
        self.assertIsNone(part.part_name)
        self.assertIsNone(part.part_type)
        self.assertIsNone(part.pattern)
        self.assertIsNone(part.style)
        self.assertIsNone(part.show_numbers)
        self.assertIsNone(part.locked)
        self.assertIsNone(part.sub_folder_index)
        self.assertIsNone(part.parameters)

    def test_002(self):
        part = Part(xml("<Part></Part>"))

    def test_mixin_001(self):
        class Component(PartsMixin):
            pass

        component = Component()

        self.assertIsNotNone(component.parts)
        self.assertListEqual([], component.parts)


if __name__ == "__main__":
    unittest.main()
