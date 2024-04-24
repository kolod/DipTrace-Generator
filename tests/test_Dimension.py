#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Dimension import Dimension, DimensionsMixin
from DipTraceGenerator.Enums import Boolean, DimensionType, PointerMode, Layer


class TestDimension(unittest.TestCase):
    def test_001(self):
        dimension = Dimension(xml("<Dimension/>"))

        self.assertIsNone(dimension.locked)
        self.assertIsNone(dimension.type)
        self.assertIsNone(dimension.point_1)
        self.assertIsNone(dimension.point_2)
        self.assertIsNone(dimension.point_d)
        self.assertIsNone(dimension.arrow_size)
        self.assertIsNone(dimension.layer)
        self.assertIsNone(dimension.font_vector)
        self.assertIsNone(dimension.angle)
        self.assertIsNone(dimension.font_name)
        self.assertIsNone(dimension.font_size)
        self.assertIsNone(dimension.font_scale)
        self.assertIsNone(dimension.font_width)
        self.assertIsNone(dimension.show_units)
        self.assertIsNone(dimension.external_radius)
        self.assertIsNone(dimension.pointer_mode)
        self.assertIsNone(dimension.pointer_text)

        self.assertIsNotNone(dimension.connection_1)
        self.assertIsNotNone(dimension.connection_2)

    def test_002(self):
        dimension = Dimension(
            xml(
                '<Dimension Locked="N" Type="Horizontal" Connected1="Pad" Object1="0" SubObject1="2" Point1="0"\n'
                '	Connected2="None" Object2="0" SubObject2="0" Point2="0" Layer="Bottom Dimension" X1="10.5002"\n'
                '	Y1="-6.0553" X2="4.4677" Y2="-8.2777" XD="10.5002" YD="-9.7065" ArrowSize="0.6667"\n'
                '	Units="Common" FontVector="Y" FontName="Tahoma" FontSize="2" FontScale="1" FontWidth="-2"\n'
                '	ShowUnits="N" Angle="0" ExternalRadius="0" PointerMode="0"/>\n'
            )
        )

        self.assertEqual(Boolean.No, dimension.locked)
        self.assertEqual(DimensionType.Horizontal, dimension.type)
        self.assertEqual(Dimension.Connection("Pad", 0, 2, 0), dimension.connection_1)
        self.assertEqual(Dimension.Connection("None", 0, 0, 0), dimension.connection_2)
        self.assertEqual(Dimension.Point(10.5002, -6.0553), dimension.point_1)
        self.assertEqual(Dimension.Point(4.4677, -8.2777), dimension.point_2)
        self.assertEqual(Dimension.Point(10.5002, -9.7065), dimension.point_d)
        self.assertEqual(0.6667, dimension.arrow_size)
        self.assertEqual(Layer.BottomDimension, dimension.layer)
        self.assertEqual(Boolean.Yes, dimension.font_vector)
        self.assertEqual(0.0, dimension.angle)
        self.assertEqual("Tahoma", dimension.font_name)
        self.assertEqual(2, dimension.font_size)
        self.assertEqual(1.0, dimension.font_scale)
        self.assertEqual(-2.0, dimension.font_width)
        self.assertEqual(Boolean.No, dimension.show_units)
        self.assertEqual(0.0, dimension.external_radius)
        self.assertEqual(PointerMode.Coordinates, dimension.pointer_mode)
        self.assertEqual(None, dimension.pointer_text)

    def test_003(self):
        dimension = Dimension(
            xml(
                '<Dimension Locked="N" Type="Pointer" Connected1="Pad" Object1="0" SubObject1="2" Point1="0"\n'
                '    Connected2="None" Object2="0" SubObject2="4" Point2="0" Layer="Bottom Dimension" X1="10.5002"\n'
                '    Y1="-6.0553" X2="18.1202" Y2="-9.5477" XD="18.1202" YD="-9.5477" ArrowSize="0.6667"\n'
                '    Units="Common" FontVector="Y" FontName="Tahoma" FontSize="2" FontScale="1" FontWidth="0.3"\n'
                '    ShowUnits="N" Angle="-0.2015" ExternalRadius="-1" PointerMode="1">\n'
                "  <PointerText>point</PointerText>\n"
                "</Dimension>\n"
            )
        )

        self.assertEqual(Boolean.No, dimension.locked)
        self.assertEqual(DimensionType.Pointer, dimension.type)
        self.assertEqual(Dimension.Connection("Pad", 0, 2, 0), dimension.connection_1)
        self.assertEqual(Dimension.Connection("None", 0, 4, 0), dimension.connection_2)
        self.assertEqual(Dimension.Point(10.5002, -6.0553), dimension.point_1)
        self.assertEqual(Dimension.Point(18.1202, -9.5477), dimension.point_2)
        self.assertEqual(Dimension.Point(18.1202, -9.5477), dimension.point_d)
        self.assertEqual(0.6667, dimension.arrow_size)
        self.assertEqual(Layer.BottomDimension, dimension.layer)
        self.assertEqual(Boolean.Yes, dimension.font_vector)
        self.assertEqual(-0.2015, dimension.angle)
        self.assertEqual("Tahoma", dimension.font_name)
        self.assertEqual(2, dimension.font_size)
        self.assertEqual(1.0, dimension.font_scale)
        self.assertEqual(0.3, dimension.font_width)
        self.assertEqual(Boolean.No, dimension.show_units)
        self.assertEqual(-1.0, dimension.external_radius)
        self.assertEqual(PointerMode.Comment, dimension.pointer_mode)
        self.assertEqual("point", dimension.pointer_text)

        self.assertEqual("Pad", dimension.connection_1.connected)
        self.assertEqual(0, dimension.connection_1.object)
        self.assertEqual(2, dimension.connection_1.sub_object)
        self.assertEqual(0, dimension.connection_1.point)

        self.assertEqual("None", dimension.connection_2.connected)
        self.assertEqual(0, dimension.connection_2.object)
        self.assertEqual(4, dimension.connection_2.sub_object)
        self.assertEqual(0, dimension.connection_2.point)

        dimension.type = DimensionType.Pointer
        self.assertEqual(DimensionType.Pointer, dimension.type)

        dimension.type = None
        self.assertIsNone(dimension.type)

        dimension.point_1 = Dimension.Point(-2.5, 5.2)
        self.assertEqual(-2.5, dimension.point_1.x)
        self.assertEqual(5.2, dimension.point_1.y)

        dimension.point_1 = None
        self.assertIsNone(dimension.point_1)

        dimension.point_2 = Dimension.Point(5.0, -2.0)
        self.assertEqual(5.0, dimension.point_2.x)
        self.assertEqual(-2.0, dimension.point_2.y)

        dimension.point_d = Dimension.Point(0.23, 56)
        self.assertEqual(0.23, dimension.point_d.x)
        self.assertEqual(56.0, dimension.point_d.y)

    def test_004(self):
        dimension = Dimension(
            connection_1=Dimension.Connection("Pad", 1, 2, 3), connection_2=Dimension.Connection("None", 0, 0, 0)
        )

        self.assertEqual("Pad", dimension.connection_1.connected)
        self.assertEqual(1, dimension.connection_1.object)
        self.assertEqual(2, dimension.connection_1.sub_object)
        self.assertEqual(3, dimension.connection_1.point)

        self.assertEqual("None", dimension.connection_2.connected)
        self.assertEqual(0, dimension.connection_2.object)
        self.assertEqual(0, dimension.connection_2.sub_object)
        self.assertEqual(0, dimension.connection_2.point)

        dimension.connection_1 = None
        self.assertIsNotNone(dimension.connection_1)
        self.assertIsNone(dimension.connection_1.connected)

        dimension.connection_2 = None
        self.assertIsNotNone(dimension.connection_2)
        self.assertIsNone(dimension.connection_2.connected)

    def test_mixin_001(self):
        class Pattern(DimensionsMixin):
            pass

        pattern = Pattern()

        self.assertIsNotNone(pattern.dimensions)
        self.assertListEqual([], pattern.dimensions)

        pattern.dimensions = [
            Dimension(
                xml(
                    '<Dimension Locked="N" Type="Pointer" Connected1="Pad" Object1="0" SubObject1="2" Point1="0"\n'
                    '    Connected2="None" Object2="0" SubObject2="4" Point2="0" Layer="Bottom Dimension" X1="10.5002"\n'
                    '    Y1="-6.0553" X2="18.1202" Y2="-9.5477" XD="18.1202" YD="-9.5477" ArrowSize="0.6667"\n'
                    '    Units="Common" FontVector="Y" FontName="Tahoma" FontSize="2" FontScale="1" FontWidth="0.3"\n'
                    '    ShowUnits="N" Angle="-0.2015" ExternalRadius="-1" PointerMode="1">\n'
                    "  <PointerText>point</PointerText>\n"
                    "</Dimension>\n"
                )
            )
        ]

        self.assertEqual(1, len(pattern.dimensions))
        self.assertEqual(-9.5477, pattern.dimensions[0].point_d.y)

        pattern.dimensions = None

        self.assertIsNotNone(pattern.dimensions)
        self.assertListEqual([], pattern.dimensions)


if __name__ == "__main__":
    unittest.main()
