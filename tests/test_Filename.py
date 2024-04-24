#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator import Filename
from DipTraceGenerator.Filename import FilenameMixin


class TestFilename(unittest.TestCase):
    def test_001(self):
        filename = Filename()

        self.assertEqual(None, filename.path)
        self.assertEqual(None, filename.variant)

    def test_002(self):
        filename = Filename(xml("<Filename><Path/><Var/></Filename>"))

        self.assertEqual(None, filename.path)
        self.assertEqual(None, filename.variant)

    def test_003(self):
        filename = Filename(
            xml("<Filename>\n" "  <Path>WF-02_Stright.wrl</Path>\n" "  <Var>WF-02_Stright.wrl</Var>\n" "</Filename>\n")
        )

        self.assertEqual("WF-02_Stright.wrl", filename.path.name)
        self.assertEqual("WF-02_Stright.wrl", filename.variant.name)

    def test_004(self):
        filename = Filename(
            xml("<Filename>\n" "  <Path>WF-02_Stright.wrl</Path>\n" "  <Var>WF-02_Stright.wrl</Var>\n" "</Filename>\n")
        )

        filename.path = None
        filename.variant = None

        self.assertEqual(None, filename.path)
        self.assertEqual(None, filename.variant)

        actual = str(filename)
        expected = "<Filename>\n</Filename>\n"

        self.assertEqual(expected, actual)

    def test_005(self):
        filename = Filename()
        filename.path = "to_220.wrl"
        filename.variant = "to_220-stright.wrl"

        expected = "<Filename>\n" "  <Path>to_220.wrl</Path>\n" "  <Var>to_220-stright.wrl</Var>\n" "</Filename>\n"
        actual = str(filename)

        self.assertEqual(expected, actual)

    def test_mixin_001(self):
        class Model3D(FilenameMixin):
            pass

        model = Model3D()

        self.assertIsNone(model.filename)

        model.filename = Filename()

        self.assertIsNotNone(model.filename)
        self.assertEqual(None, model.filename.path)
        self.assertEqual(None, model.filename.variant)

        model.filename.path = "test.wrl"
        model.filename.variant = "variant.wrl"

        self.assertEqual("test.wrl", str(model.filename.path))
        self.assertEqual("variant.wrl", str(model.filename.variant))

        expected = (
            "<Model3D>\n"
            "  <Filename>\n"
            "    <Path>test.wrl</Path>\n"
            "    <Var>variant.wrl</Var>\n"
            "  </Filename>\n"
            "</Model3D>\n"
        )
        actual = str(model)

        self.assertEqual(expected, actual)

        model.filename = None

        self.assertIsNone(model.filename)


if __name__ == "__main__":
    unittest.main()
