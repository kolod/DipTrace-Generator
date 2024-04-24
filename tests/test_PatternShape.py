#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import math
import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.PatternShape import PatternShape, PatternShapesMixin
from DipTraceGenerator.Enums import Boolean, Layer, ShapeType, HorizontalAlignment, VerticalAlignment, TextShow
from DipTraceGenerator.Point import Point
from DipTraceGenerator.Pattern import Pattern


class TestPatternShape(unittest.TestCase):
    def test_001(self):
        shape = PatternShape()

        self.assertEqual(None, shape.id)
        self.assertEqual(None, shape.type)
        self.assertEqual(None, shape.locked)
        self.assertEqual(None, shape.layer)
        self.assertEqual(None, shape.all_layers)
        self.assertEqual(None, shape.angle)

        self.assertEqual(None, shape.font_vector)
        self.assertEqual(None, shape.font_name)
        self.assertEqual(None, shape.font_size)
        self.assertEqual(None, shape.font_scale)
        self.assertEqual(None, shape.font_width)
        self.assertEqual(None, shape.horizontal_alignment)
        self.assertEqual(None, shape.vertical_alignment)
        self.assertEqual(None, shape.line_spacing)

        self.assertEqual(None, shape.points)
        self.assertEqual(None, shape.lines)

    def test_002(self):
        shape = PatternShape(
            xml(
                '<Shape Id="1" Type="Polygon" Locked="N" Layer="Top" AllLayers="N">\n'
                "    <Points>\n"
                '        <Item X="-6.5542" Y="2.6118"/>\n'
                '        <Item X="-6.5542" Y="1.9919"/>\n'
                '        <Item X="-6.9926" Y="1.5535"/>\n'
                '        <Item X="-7.62" Y="1.3494"/>\n'
                '        <Item X="-8.0509" Y="1.9919"/>\n'
                '        <Item X="-8.0509" Y="2.6118"/>\n'
                '        <Item X="-7.6125" Y="3.0502"/>\n'
                '        <Item X="-6.9926" Y="3.0502"/>\n'
                "    </Points>\n"
                "</Shape>\n"
            )
        )

        self.assertEqual(1, shape.id)
        self.assertEqual(ShapeType.Polygon, shape.type)
        self.assertEqual(Boolean.No, shape.locked)
        self.assertEqual(Layer.Top, shape.layer)
        self.assertEqual(Boolean.No, shape.all_layers)
        self.assertEqual(None, shape.angle)

        self.assertEqual(None, shape.font_vector)
        self.assertEqual(None, shape.font_name)
        self.assertEqual(None, shape.font_size)
        self.assertEqual(None, shape.font_scale)
        self.assertEqual(None, shape.font_width)
        self.assertEqual(None, shape.horizontal_alignment)
        self.assertEqual(None, shape.vertical_alignment)
        self.assertEqual(None, shape.line_spacing)

        self.assertEqual(8, len(shape.points))
        self.assertEqual(-6.5542, shape.points[0].x)
        self.assertEqual(3.0502, shape.points[7].y)

        self.assertEqual(None, shape.lines)

    def test_003(self):
        shape = PatternShape(
            xml(
                '<Shape Id="4" Type="Text" Locked="N" Layer="Top Silk"\n'
                '    FontVector="N" FontName="Tahoma" FontSize="12" FontScale="1" FontWidth="-2"\n'
                '    TextShow="Any Text" HorzAlign="Center" VertAlign="Center" TextAlign="Center"\n'
                '    LineSpacing="1.2" Angle="1.5708" AllLayers="N">\n'
                "    <Lines>\n"
                "        <Item>123</Item>\n"
                "        <Item>567</Item>\n"
                "    </Lines>\n"
                "    <Points>\n"
                '        <Item X="10.5002" Y="10.4548"/>\n'
                "    </Points>\n"
                "</Shape>\n"
            )
        )

        self.assertEqual(4, shape.id)
        self.assertEqual(ShapeType.Text, shape.type)
        self.assertEqual(Boolean.No, shape.locked)
        self.assertEqual(Layer.TopSilk, shape.layer)
        self.assertEqual(Boolean.No, shape.all_layers)
        self.assertEqual(1.5708, shape.angle)

        self.assertEqual(Boolean.No, shape.font_vector)
        self.assertEqual("Tahoma", shape.font_name)
        self.assertEqual(12, shape.font_size)
        self.assertEqual(1.0, shape.font_scale)
        self.assertEqual(-2.0, shape.font_width)
        self.assertEqual(HorizontalAlignment.Center, shape.horizontal_alignment)
        self.assertEqual(VerticalAlignment.Center, shape.vertical_alignment)
        self.assertEqual(1.2, shape.line_spacing)

        self.assertEqual(1, len(shape.points))
        self.assertEqual(10.5002, shape.points[0].x)
        self.assertEqual(10.4548, shape.points[0].y)

        self.assertListEqual(["123", "567"], shape.lines)

    def test_004(self):
        shape = PatternShape(
            xml(
                '<Shape Id="4" Type="Text" Locked="N" Layer="Top Silk"\n'
                '  FontVector="N" FontName="Tahoma" FontSize="12" FontScale="1" FontWidth="-2"\n'
                '  TextShow="Any Text" HorzAlign="Center" VertAlign="Center" TextAlign="Center"\n'
                '  LineSpacing="1.2" Angle="1.5708" AllLayers="N">\n'
                "  <Lines>\n"
                "    <Item>123</Item>\n"
                "    <Item>567</Item>\n"
                "  </Lines>\n"
                "  <Points>\n"
                '    <Item X="10.5002" Y="10.4548"/>\n'
                "  </Points>\n"
                "</Shape>\n"
            )
        )

        shape.lines = ["test"]

        self.assertListEqual(["test"], shape.lines)

    def test_005(self):
        shape = PatternShape(
            xml(
                '<Shape Id="4" Type="Text" Locked="N" Layer="Top Silk"\n'
                '  FontVector="N" FontName="Tahoma" FontSize="12" FontScale="1" FontWidth="-2"\n'
                '  TextShow="Any Text" HorzAlign="Center" VertAlign="Center" TextAlign="Center"\n'
                '  LineSpacing="1.2" Angle="1.5708" AllLayers="N">\n'
                "  <Lines>\n"
                "    <Item>123</Item>\n"
                "    <Item>567</Item>\n"
                "  </Lines>\n"
                "  <Points>\n"
                '    <Item X="10.5002" Y="10.4548"/>\n'
                "  </Points>\n"
                "</Shape>\n"
            )
        )

        shape.type = None
        self.assertEqual(None, shape.type)
        self.assertEqual(TextShow.Text, shape.text_show)
        self.assertEqual(HorizontalAlignment.Center, shape.text_alignment)
        self.assertEqual(HorizontalAlignment.Center, shape.horizontal_alignment)
        self.assertEqual(VerticalAlignment.Center, shape.vertical_alignment)
        self.assertEqual(1.2, shape.line_spacing)

        shape.text_show = None
        self.assertIsNone(shape.text_show)

        shape.text_alignment = None
        self.assertIsNone(shape.text_alignment)

        shape.horizontal_alignment = None
        self.assertIsNone(shape.horizontal_alignment)

        shape.vertical_alignment = None
        self.assertIsNone(shape.vertical_alignment)

        shape.line_spacing = None
        self.assertIsNone(shape.line_spacing)

        shape.text_show = TextShow.Value
        self.assertEqual(TextShow.Value, shape.text_show)

        shape.text_alignment = HorizontalAlignment.Right
        self.assertEqual(HorizontalAlignment.Right, shape.text_alignment)

        shape.horizontal_alignment = HorizontalAlignment.Left
        self.assertEqual(HorizontalAlignment.Left, shape.horizontal_alignment)

        shape.vertical_alignment = VerticalAlignment.Top
        self.assertEqual(VerticalAlignment.Top, shape.vertical_alignment)

        shape.line_spacing = 1.0
        self.assertEqual(1.0, shape.line_spacing)

    def test_006(self):
        r = 1.5
        x1 = r * math.cos(math.radians(45))
        y1 = r * math.sin(math.radians(45))
        x2 = r * math.cos(math.radians(45))
        y2 = r * math.sin(math.radians(45))

        r3 = 3.85 / 2
        x3 = 1.6
        y3 = math.sqrt(math.pow(r3, 2) - math.pow(x3, 2))

        point_1 = Point()
        point_1.x = -x1
        point_1.y = -y1

        point_2 = Point()
        point_2.x = 0.0
        point_2.y = -r

        point_3 = Point()
        point_3.x = -x2
        point_3.y = -y2

        point_4 = Point()
        point_4.x = -x1
        point_4.y = y1

        point_5 = Point()
        point_5.x = 0.0
        point_5.y = r

        point_6 = Point()
        point_6.x = x2
        point_6.y = y2

        point_7 = Point()
        point_7.x = -x3
        point_7.y = -y3

        point_8 = Point()
        point_8.x = 0.0
        point_8.y = -r3

        point_9 = Point()
        point_9.x = -x3
        point_9.y = y3

        shape_1 = PatternShape()
        shape_1.points = [point_1, point_2, point_3]
        shape_1.all_layers = Boolean.No
        shape_1.locked = Boolean.Yes
        shape_1.type = ShapeType.Arc
        shape_1.layer = Layer.TopSilk

        shape_2 = PatternShape()
        shape_2.points = [point_4, point_5, point_6]
        shape_2.all_layers = Boolean.No
        shape_2.locked = Boolean.Yes
        shape_2.type = ShapeType.Arc
        shape_2.layer = Layer.TopSilk

        shape_3 = PatternShape()
        shape_3.points = [point_7, point_8, point_9]
        shape_3.all_layers = Boolean.No
        shape_3.locked = Boolean.Yes
        shape_3.type = ShapeType.Arc
        shape_3.layer = Layer.TopCourtyard

        shape_4 = PatternShape()
        shape_4.points = [point_7, point_9]
        shape_4.all_layers = Boolean.No
        shape_4.locked = Boolean.Yes
        shape_4.type = ShapeType.Line
        shape_4.layer = Layer.TopCourtyard

        shape_5 = PatternShape()
        shape_5.points = [point_7, point_8, point_9]
        shape_5.all_layers = Boolean.No
        shape_5.locked = Boolean.Yes
        shape_5.type = ShapeType.Arc
        shape_5.layer = Layer.TopAssembly

        shape_6 = PatternShape()
        shape_6.points = [point_7, point_9]
        shape_6.all_layers = Boolean.No
        shape_6.locked = Boolean.Yes
        shape_6.type = ShapeType.Line
        shape_6.layer = Layer.TopAssembly

        pattern = Pattern()
        pattern.shapes = [shape_1, shape_2, shape_3, shape_4, shape_5, shape_6]

        actual = str(pattern)
        expected = (
            "<Pattern>\n"
            "  <Shapes>\n"
            '    <Shape AllLayers="N" Locked="Y" Type="Arc" Layer="Top Silk">\n'
            "      <Points>\n"
            '        <Item X="-1.0607" Y="-1.0607"/>\n'
            '        <Item X="0" Y="-1.5"/>\n'
            '        <Item X="-1.0607" Y="-1.0607"/>\n'
            "      </Points>\n"
            "    </Shape>\n"
            '    <Shape AllLayers="N" Locked="Y" Type="Arc" Layer="Top Silk">\n'
            "      <Points>\n"
            '        <Item X="-1.0607" Y="1.0607"/>\n'
            '        <Item X="0" Y="1.5"/>\n'
            '        <Item X="1.0607" Y="1.0607"/>\n'
            "      </Points>\n"
            "    </Shape>\n"
            '    <Shape AllLayers="N" Locked="Y" Type="Arc" Layer="Top Courtyard">\n'
            "      <Points>\n"
            '        <Item X="-1.6" Y="-1.0703"/>\n'
            '        <Item X="0" Y="-1.925"/>\n'
            '        <Item X="-1.6" Y="1.0703"/>\n'
            "      </Points>\n"
            "    </Shape>\n"
            '    <Shape AllLayers="N" Locked="Y" Type="Line" Layer="Top Courtyard">\n'
            "      <Points>\n"
            '        <Item X="-1.6" Y="-1.0703"/>\n'
            '        <Item X="-1.6" Y="1.0703"/>\n'
            "      </Points>\n"
            "    </Shape>\n"
            '    <Shape AllLayers="N" Locked="Y" Type="Arc" Layer="Top Assy">\n'
            "      <Points>\n"
            '        <Item X="-1.6" Y="-1.0703"/>\n'
            '        <Item X="0" Y="-1.925"/>\n'
            '        <Item X="-1.6" Y="1.0703"/>\n'
            "      </Points>\n"
            "    </Shape>\n"
            '    <Shape AllLayers="N" Locked="Y" Type="Line" Layer="Top Assy">\n'
            "      <Points>\n"
            '        <Item X="-1.6" Y="-1.0703"/>\n'
            '        <Item X="-1.6" Y="1.0703"/>\n'
            "      </Points>\n"
            "    </Shape>\n"
            "  </Shapes>\n"
            "</Pattern>\n"
        )

        self.assertEqual(expected, actual)

    def test_mixin_001(self):
        class Pattern(PatternShapesMixin):
            pass

        pattern = Pattern()

        self.assertListEqual([], pattern.shapes)

        pattern.shapes = [
            PatternShape(
                xml(
                    '<Shape AllLayers="N" Locked="Y" Type="Arc" Layer="Top Silk">\n'
                    "  <Points>\n"
                    '    <Item X="-1.06066" Y="-1.06066"/>\n'
                    '    <Item X="0" Y="-1.5"/>\n'
                    '    <Item X="-1.06066" Y="-1.06066"/>\n'
                    "  </Points>\n"
                    "</Shape>\n"
                )
            ),
            PatternShape(
                xml(
                    '<Shape AllLayers="N" Locked="Y" Type="Arc" Layer="Top Silk">\n'
                    "  <Points>\n"
                    '    <Item X="-1.06066" Y="1.06066"/>\n'
                    '    <Item X="0" Y="1.5"/>\n'
                    '    <Item X="1.06066" Y="1.06066"/>\n'
                    "  </Points>\n"
                    "</Shape>\n"
                )
            ),
        ]

        self.assertEqual(2, len(pattern.shapes))
        self.assertEqual(-1.06066, pattern.shapes[0].points[2].x)
        self.assertEqual(1.06066, pattern.shapes[1].points[2].y)

        pattern.shapes = None

        self.assertListEqual([], pattern.shapes)


if __name__ == "__main__":
    unittest.main()
