#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Model3D import Model3D, Boolean, Units3D, Model3DType, Model3DMixin


class TestModel3D(unittest.TestCase):
    def test_model_3d_0(self):
        model = Model3D(xml("<Model3D/>"))

        self.assertEqual(None, model.type)
        self.assertEqual(None, model.units)
        self.assertEqual(None, model.mirror)
        self.assertEqual(None, model.no_search)
        self.assertEqual(None, model.x_offset)
        self.assertEqual(None, model.y_offset)
        self.assertEqual(None, model.keep_pins)

        self.assertEqual(None, model.filename)

        self.assertEqual(None, model.rotate)
        self.assertEqual(None, model.offset)
        self.assertEqual(None, model.zoom)

    def test_model_3d_1(self):
        model = Model3D(
            xml(
                '<Model3D Mirror="N" NoSearch="N" Units="Wings" IPC_XOff="1.6669" IPC_YOff="-2.4606"\n'
                '    AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">\n'
                '  <Rotate X="0" Y="1" Z="2"/>\n'
                '  <Offset X="3" Y="4" Z="5"/>\n'
                '  <Zoom X="6" Y="7" Z="8"/>\n'
                "</Model3D>\n"
            )
        )

        self.assertEqual(Model3DType.File, model.type)
        self.assertEqual(Units3D.wings, model.units)
        self.assertEqual(Boolean.No, model.mirror)
        self.assertEqual(Boolean.No, model.no_search)
        self.assertEqual(1.6669, model.x_offset)
        self.assertEqual(-2.4606, model.y_offset)
        self.assertEqual(Boolean.No, model.keep_pins)

        self.assertEqual(0.0, model.rotate.x)
        self.assertEqual(1.0, model.rotate.y)
        self.assertEqual(2.0, model.rotate.z)
        self.assertEqual(3.0, model.offset.x)
        self.assertEqual(4.0, model.offset.y)
        self.assertEqual(5.0, model.offset.z)
        self.assertEqual(6.0, model.zoom.x)
        self.assertEqual(7.0, model.zoom.y)
        self.assertEqual(8.0, model.zoom.z)

    def test_model_3d_2(self):
        model = Model3D(
            xml(
                '<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0.85"\n'
                '    AutoColor="4934475" Type="IPC-7351" KeepPins="N">\n'
                '  <Rotate X="0" Y="0" Z="0"/>\n'
                '  <Offset X="0" Y="0" Z="-0.05"/>\n'
                '  <Zoom X="1" Y="1" Z="1"/>\n'
                "</Model3D>\n"
            )
        )

        self.assertEqual(Units3D.mm, model.units)
        self.assertEqual(Boolean.No, model.mirror)
        self.assertEqual(Boolean.No, model.no_search)
        self.assertEqual(0.0, model.x_offset)
        self.assertEqual(0.0, model.y_offset)
        self.assertEqual(Boolean.No, model.keep_pins)

        self.assertEqual(0.0, model.rotate.x)
        self.assertEqual(0.0, model.rotate.y)
        self.assertEqual(0.0, model.rotate.z)
        self.assertEqual(0.0, model.offset.x)
        self.assertEqual(0.0, model.offset.y)
        self.assertEqual(-0.05, model.offset.z)
        self.assertEqual(1.0, model.zoom.x)
        self.assertEqual(1.0, model.zoom.y)
        self.assertEqual(1.0, model.zoom.z)

    def test_model_3d_3(self):
        model = Model3D(
            xml(
                '<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0"\n'
                '    AutoColor="4934475" Type="File" KeepPins="N">\n'
                "  <Filename>\n"
                "    <Path>2EDGRM-5.0_5.08-02P-14-00AH.STEP</Path>\n"
                "    <Var>2EDGRM-5.0_5.08-02P-14-00AH.STEP</Var>\n"
                "  </Filename>\n"
                '  <Rotate X="0" Y="0" Z="0"/>\n'
                '  <Offset X="0" Y="0" Z="0"/>\n'
                '  <Zoom X="1" Y="1" Z="1"/>\n'
                "</Model3D>\n"
            )
        )

        self.assertEqual(Units3D.mm, model.units)
        self.assertEqual(Boolean.No, model.mirror)
        self.assertEqual(Boolean.No, model.no_search)
        self.assertEqual(0.0, model.x_offset)
        self.assertEqual(0.0, model.y_offset)
        self.assertEqual(Boolean.No, model.keep_pins)
        self.assertEqual(0, model.auto_height)
        self.assertEqual(4934475, model.auto_color)

        self.assertEqual(0.0, model.rotate.x)
        self.assertEqual(0.0, model.rotate.y)
        self.assertEqual(0.0, model.rotate.z)
        self.assertEqual(0.0, model.offset.x)
        self.assertEqual(0.0, model.offset.y)
        self.assertEqual(0.0, model.offset.z)
        self.assertEqual(1.0, model.zoom.x)
        self.assertEqual(1.0, model.zoom.y)
        self.assertEqual(1.0, model.zoom.z)

        model.mirror = None
        self.assertIsNone(model.mirror)

        model.no_search = None
        self.assertIsNone(model.no_search)

        model.keep_pins = None
        self.assertIsNone(model.keep_pins)

        model.auto_height = None
        self.assertIsNone(model.auto_height)

        model.auto_color = None
        self.assertIsNone(model.auto_color)

        model.units = None
        self.assertIsNone(model.units)

        model.x_offset = None
        self.assertIsNone(model.x_offset)

        model.y_offset = None
        self.assertIsNone(model.y_offset)

        model.type = None
        self.assertIsNone(model.type)

        model.rotate = None
        self.assertIsNone(model.rotate)

        model.offset = None
        self.assertIsNone(model.offset)

        model.zoom = None
        self.assertIsNone(model.zoom)

    def test_mixin_001(self):
        class Pattern(Model3DMixin):
            pass

        pattern = Pattern()

        self.assertIsNone(pattern.model3d)

        pattern.model3d = Model3D(
            xml(
                '<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0.85"\n'
                '    AutoColor="4934475" Type="IPC-7351" KeepPins="N">\n'
                '  <Rotate X="0" Y="0" Z="0"/>\n'
                '  <Offset X="0" Y="0" Z="-0.05"/>\n'
                '  <Zoom X="1" Y="1" Z="1"/>\n'
                "</Model3D>\n"
            )
        )

        self.assertIsNotNone(pattern.model3d)
        self.assertEqual(4934475, pattern.model3d.auto_color)

        pattern.model3d = None

        self.assertIsNone(pattern.model3d)


if __name__ == "__main__":
    unittest.main()
