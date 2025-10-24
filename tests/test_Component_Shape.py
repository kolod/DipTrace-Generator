#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Shape.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Shape tests/test_Component_Shape.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator import Shape, ShapeType, Boolean, HorizontalAlign, VerticalAlign, TextAlign, TextShow, \
    Point, Units


class TestComponentShape(TestCase):
    """Test cases for Component Shape class"""

    def test_shape_default_initialization(self):
        """Test Shape initializes with default values"""
        shape = Shape()
        self.assertEqual(shape.id, 0)
        self.assertEqual(shape.type, ShapeType.Line)
        self.assertEqual(shape.line_width, 0.25)
        self.assertEqual(shape.locked, Boolean.No)
        self.assertIsNone(shape.group)
        self.assertEqual(shape.points, [])

    def test_shape_initialization_with_values(self):
        """Test Shape initialization with explicit values"""
        points = [Point(x=0, y=0), Point(x=10, y=10)]
        shape = Shape(
            id=5,
            type=ShapeType.Line,
            line_width=5.0,
            locked=Boolean.Yes,
            group=1,
            points=points
        )
        self.assertEqual(shape.id, 5)
        self.assertEqual(shape.type, ShapeType.Line)
        self.assertEqual(shape.line_width, 5.0)
        self.assertEqual(shape.locked, Boolean.Yes)
        self.assertEqual(shape.group, 1)
        self.assertEqual(len(shape.points), 2)

    def test_from_xml_line_shape(self):
        """Test creating Line shape from XML"""
        xml_str = '''<Shape Id="0" Type="Line" LineWidth="9.8425" Locked="N" Group="0">
            <Points>
                <Point X="-787.4016" Y="-98.4252"/>
                <Point X="-393.7008" Y="-98.4252"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 0)
        self.assertEqual(shape.type, ShapeType.Line)
        self.assertAlmostEqual(shape.line_width, 9.8425, places=4)
        self.assertEqual(shape.locked, Boolean.No)
        self.assertEqual(shape.group, 0)
        self.assertEqual(len(shape.points), 2)

    def test_from_xml_arc_shape(self):
        """Test creating Arc shape from XML"""
        xml_str = '''<Shape Id="1" Type="Arc" LineWidth="9.8425" Locked="N" Group="0">
            <Points>
                <Point X="-393.7008" Y="-492.126"/>
                <Point X="-590.5512" Y="-295.2756"/>
                <Point X="-787.4016" Y="-492.126"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 1)
        self.assertEqual(shape.type, ShapeType.Arc)
        self.assertEqual(len(shape.points), 3)

    def test_from_xml_arrow_shape(self):
        """Test creating Arrow shape from XML"""
        xml_str = '''<Shape Id="2" Type="Arrow" LineWidth="9.8425" Locked="N" Group="0">
            <Points>
                <Point X="-590.5512" Y="-885.8268"/>
                <Point X="-590.5512" Y="-492.126"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 2)
        self.assertEqual(shape.type, ShapeType.Arrow)
        self.assertEqual(len(shape.points), 2)

    def test_from_xml_rectangle_shape(self):
        """Test creating Rectangle shape from XML"""
        xml_str = '''<Shape Id="3" Type="Rectangle" LineWidth="9.8425" Locked="N" Group="0">
            <Points>
                <Point X="-984.252" Y="98.4252"/>
                <Point X="-196.8504" Y="-1082.6772"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 3)
        self.assertEqual(shape.type, ShapeType.Rectangle)
        self.assertEqual(len(shape.points), 2)

    def test_from_xml_fillrect_shape(self):
        """Test creating FillRect shape from XML"""
        xml_str = '''<Shape Id="4" Type="FillRect" LineWidth="9.8425" Locked="N" Group="0">
            <Points>
                <Point X="-984.252" Y="-1279.5276"/>
                <Point X="-196.8504" Y="-1476.378"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 4)
        self.assertEqual(shape.type, ShapeType.FillRect)

    def test_from_xml_obround_shape(self):
        """Test creating Obround shape from XML"""
        xml_str = '''<Shape Id="5" Type="Obround" LineWidth="9.8425" Locked="N" Group="0">
            <Points>
                <Point X="-984.252" Y="492.126"/>
                <Point X="-196.8504" Y="295.2756"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 5)
        self.assertEqual(shape.type, ShapeType.Obround)

    def test_from_xml_fillobround_shape(self):
        """Test creating FillObround shape from XML"""
        xml_str = '''<Shape Id="6" Type="FillObround" LineWidth="9.8425" Locked="N" Group="0">
            <Points>
                <Point X="-984.252" Y="885.8268"/>
                <Point X="-196.8504" Y="688.9764"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 6)
        self.assertEqual(shape.type, ShapeType.FillObround)

    def test_from_xml_polyline_shape(self):
        """Test creating Polyline shape from XML"""
        xml_str = '''<Shape Id="7" Type="Polyline" LineWidth="9.8425" Locked="N">
            <Points>
                <Point X="-1181.1024" Y="1082.6772"/>
                <Point X="0" Y="1082.6772"/>
                <Point X="196.8504" Y="-1673.2283"/>
                <Point X="0" Y="-1870.0787"/>
                <Point X="-1181.1024" Y="-1870.0787"/>
                <Point X="-1377.9528" Y="-1673.2283"/>
                <Point X="-1181.1024" Y="1082.6772"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 7)
        self.assertEqual(shape.type, ShapeType.Polyline)
        self.assertEqual(len(shape.points), 7)
        self.assertIsNone(shape.group)  # No group specified

    def test_from_xml_polygon_shape(self):
        """Test creating Polygon shape from XML"""
        xml_str = '''<Shape Id="8" Type="Polygon" LineWidth="9.8425" Locked="N">
            <Points>
                <Point X="-1181.1024" Y="1870.0787"/>
                <Point X="0" Y="1870.0787"/>
                <Point X="-1181.1024" Y="1279.5276"/>
                <Point X="0" Y="1279.5276"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 8)
        self.assertEqual(shape.type, ShapeType.Polygon)
        self.assertEqual(len(shape.points), 4)

    def test_from_xml_text_shape_vector(self):
        """Test creating Text shape with vector font from XML"""
        xml_str = '''<Shape Id="10" Type="Text" Locked="N" FontVector="Y" FontSize="12" FontColor="8388608" TextShow="Any Text" FontName="Tahoma" FontWidth="-2" FontScale="1" Angle="0" HorzAlign="Center" VertAlign="Center" TextAlign="Left" LineSpacing="1.2">
            <TextLines>
                <TextLine>Vector</TextLine>
            </TextLines>
            <Points>
                <Point X="-590.5512" Y="-1673.2283"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 10)
        self.assertEqual(shape.type, ShapeType.Text)
        self.assertEqual(shape.locked, Boolean.No)
        self.assertEqual(shape.font_vector, Boolean.Yes)
        self.assertEqual(shape.font_size, 12)
        self.assertEqual(shape.font_color, 8388608)
        self.assertEqual(shape.text_show, TextShow.AnyText)
        self.assertEqual(shape.font_name, "Tahoma")
        self.assertEqual(shape.font_width, -2)
        self.assertEqual(shape.font_scale, 1.0)
        self.assertEqual(shape.angle, 0.0)
        self.assertEqual(shape.horz_align, HorizontalAlign.Center)
        self.assertEqual(shape.vert_align, VerticalAlign.Center)
        self.assertEqual(shape.text_align, TextAlign.Left)
        self.assertEqual(shape.line_spacing, 1.2)
        self.assertEqual(len(shape.text_lines), 1)
        self.assertEqual(shape.text_lines[0], "Vector")
        self.assertEqual(len(shape.points), 1)

    def test_from_xml_text_shape_truetype(self):
        """Test creating Text shape with TrueType font from XML"""
        xml_str = '''<Shape Id="11" Type="Text" Locked="N" FontVector="N" FontSize="12" FontColor="8388608" TextShow="Any Text" FontName="Fira Code" FontWidth="-2" FontScale="1" Angle="0" HorzAlign="Center" VertAlign="Center" TextAlign="Center" LineSpacing="1.2">
            <TextLines>
                <TextLine>TrueType</TextLine>
            </TextLines>
            <Points>
                <Point X="-590.5512" Y="-2066.9291"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(shape.id, 11)
        self.assertEqual(shape.type, ShapeType.Text)
        self.assertEqual(shape.font_vector, Boolean.No)
        self.assertEqual(shape.font_name, "Fira Code")
        self.assertEqual(shape.text_align, TextAlign.Center)
        self.assertEqual(len(shape.text_lines), 1)
        self.assertEqual(shape.text_lines[0], "TrueType")

    def test_from_xml_no_points(self):
        """Test shape with no points"""
        xml_str = '''<Shape Id="0" Type="Line" LineWidth="5.0" Locked="N"/>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element)
        
        self.assertEqual(len(shape.points), 0)

    def test_from_xml_locked_yes(self):
        """Test shape with locked=Yes"""
        xml_str = '''<Shape Id="0" Type="Line" LineWidth="5.0" Locked="Y">
            <Points>
                <Point X="0" Y="0"/>
                <Point X="10" Y="10"/>
            </Points>
        </Shape>'''
        element = xml(xml_str)
        shape = Shape.from_xml(element)
        
        self.assertEqual(shape.locked, Boolean.Yes)

    def test_to_xml_line_shape(self):
        """Test converting Line shape to XML"""
        shape = Shape(
            id=0,
            type=ShapeType.Line,
            line_width=9.8425,
            locked=Boolean.No,
            group=0,
            points=[
                Point(x=-20.0, y=-2.5),
                Point(x=-10.0, y=-2.5)
            ]
        )
        element = shape.to_xml(units=Units.MIL)
        
        self.assertEqual(element.tag, "Shape")
        self.assertEqual(element.get("Id"), "0")
        self.assertEqual(element.get("Type"), "Line")
        self.assertEqual(element.get("LineWidth"), "9.8425")
        self.assertEqual(element.get("Locked"), "N")
        self.assertEqual(element.get("Group"), "0")
        
        points_elem = element.find("Points")
        self.assertIsNotNone(points_elem)
        point_elems = points_elem.findall("Point")
        self.assertEqual(len(point_elems), 2)

    def test_to_xml_arc_shape(self):
        """Test converting Arc shape to XML"""
        shape = Shape(
            id=1,
            type=ShapeType.Arc,
            line_width=9.8425,
            locked=Boolean.No,
            group=0,
            points=[
                Point(x=-10.0, y=-12.5),
                Point(x=-15.0, y=-7.5),
                Point(x=-20.0, y=-12.5)
            ]
        )
        element = shape.to_xml(units=Units.MIL)
        
        self.assertEqual(element.get("Type"), "Arc")
        points_elem = element.find("Points")
        point_elems = points_elem.findall("Point")
        self.assertEqual(len(point_elems), 3)

    def test_to_xml_text_shape(self):
        """Test converting Text shape to XML"""
        shape = Shape(
            id=10,
            type=ShapeType.Text,
            locked=Boolean.No,
            line_width=9.8425,
            font_vector=Boolean.Yes,
            font_size=12,
            font_color=8388608,
            text_show=TextShow.AnyText,
            font_name="Tahoma",
            font_width=-2,
            font_scale=1.0,
            angle=0.0,
            horz_align=HorizontalAlign.Center,
            vert_align=VerticalAlign.Center,
            text_align=TextAlign.Left,
            line_spacing=1.2,
            text_lines=["Vector"],
            points=[Point(x=-15.0, y=-42.5)]
        )
        element = shape.to_xml(units=Units.MIL)
        
        self.assertEqual(element.get("Type"), "Text")
        self.assertEqual(element.get("FontVector"), "Y")
        self.assertEqual(element.get("FontSize"), "12")
        self.assertEqual(element.get("FontColor"), "8388608")
        self.assertEqual(element.get("TextShow"), "Any Text")
        self.assertEqual(element.get("FontName"), "Tahoma")
        self.assertEqual(element.get("FontWidth"), "-2")
        self.assertEqual(element.get("FontScale"), "1.0")
        self.assertEqual(element.get("Angle"), "0.0")
        self.assertEqual(element.get("HorzAlign"), "Center")
        self.assertEqual(element.get("VertAlign"), "Center")
        self.assertEqual(element.get("TextAlign"), "Left")
        self.assertEqual(element.get("LineSpacing"), "1.2")
        
        # Check text lines
        text_lines_elem = element.find("TextLines")
        self.assertIsNotNone(text_lines_elem)
        line_elems = text_lines_elem.findall("TextLine")
        self.assertEqual(len(line_elems), 1)
        self.assertEqual(line_elems[0].text, "Vector")

    def test_to_xml_no_group(self):
        """Test shape without group attribute"""
        shape = Shape(
            id=7,
            type=ShapeType.Polyline,
            line_width=9.8425,
            locked=Boolean.No,
            points=[Point(x=0, y=0), Point(x=10, y=10)]
        )
        element = shape.to_xml()
        
        self.assertIsNone(element.get("Group"))

    def test_to_xml_empty_points(self):
        """Test shape with no points"""
        shape = Shape(
            id=0,
            type=ShapeType.Line,
            line_width=5.0,
            locked=Boolean.No
        )
        element = shape.to_xml()
        
        # Should not have Points element if no points
        points_elem = element.find("Points")
        self.assertIsNone(points_elem)

    def test_round_trip_line_shape(self):
        """Test round-trip: Shape -> XML -> Shape for Line"""
        original = Shape(
            id=0,
            type=ShapeType.Line,
            line_width=9.8425,
            locked=Boolean.No,
            group=0,
            points=[Point(x=-20.0, y=-2.5), Point(x=-10.0, y=-2.5)]
        )
        element = original.to_xml(units=Units.MIL)
        recovered = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(recovered.id, original.id)
        self.assertEqual(recovered.type, original.type)
        self.assertAlmostEqual(recovered.line_width, original.line_width, places=4)
        self.assertEqual(recovered.locked, original.locked)
        self.assertEqual(recovered.group, original.group)
        self.assertEqual(len(recovered.points), len(original.points))

    def test_round_trip_text_shape(self):
        """Test round-trip: Shape -> XML -> Shape for Text"""
        original = Shape(
            id=10,
            type=ShapeType.Text,
            locked=Boolean.No,
            line_width=9.8425,
            font_vector=Boolean.Yes,
            font_size=12,
            font_color=8388608,
            text_show=TextShow.AnyText,
            font_name="Tahoma",
            font_width=-2,
            font_scale=1.0,
            angle=0.0,
            horz_align=HorizontalAlign.Center,
            vert_align=VerticalAlign.Center,
            text_align=TextAlign.Left,
            line_spacing=1.2,
            text_lines=["Test", "Text"],
            points=[Point(x=-15.0, y=-42.5)]
        )
        element = original.to_xml(units=Units.MIL)
        recovered = Shape.from_xml(element, units=Units.MIL)
        
        self.assertEqual(recovered.font_vector, original.font_vector)
        self.assertEqual(recovered.font_size, original.font_size)
        self.assertEqual(recovered.font_name, original.font_name)
        self.assertEqual(recovered.text_lines, original.text_lines)


if __name__ == "__main__":
    main()
