#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from lxml import etree
from unittest import TestCase, main
from DipTraceGenerator.Pattern import MainStack, PadStackShape
from DipTraceGenerator import Units, Point


class TestMainStack(TestCase):
    """Test cases for Pattern.MainStack class."""

    def test_default_constructor(self):
        """Test creating MainStack with default values."""
        stack = MainStack()
        self.assertEqual(stack.shape, PadStackShape.Ellipse)
        self.assertEqual(stack.width, 0.0)
        self.assertEqual(stack.height, 0.0)
        self.assertIsNone(stack.xoff)
        self.assertIsNone(stack.yoff)
        self.assertIsNone(stack.corner)
        self.assertEqual(stack.points, [])

    def test_constructor_with_values(self):
        """Test creating MainStack with specific values."""
        stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=1.5,
            height=2.0,
            corner=25.0
        )
        self.assertEqual(stack.shape, PadStackShape.Rectangle)
        self.assertEqual(stack.width, 1.5)
        self.assertEqual(stack.height, 2.0)
        self.assertEqual(stack.corner, 25.0)
        self.assertIsNone(stack.xoff)
        self.assertIsNone(stack.yoff)

    def test_from_xml_rectangle_surface(self):
        """Test parsing Rectangle MainStack for surface pad."""
        xml = '<MainStack Shape="Rectangle" Width="0.6" Height="2" Corner="25"/>'
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element)
        
        self.assertEqual(stack.shape, PadStackShape.Rectangle)
        self.assertAlmostEqual(stack.width, 0.6, places=4)
        self.assertAlmostEqual(stack.height, 2.0, places=4)
        self.assertEqual(stack.corner, 25.0)
        self.assertIsNone(stack.xoff)
        self.assertIsNone(stack.yoff)

    def test_from_xml_ellipse_through(self):
        """Test parsing Ellipse MainStack for through-hole pad."""
        xml = '<MainStack Shape="Ellipse" Width="1.5" Height="1.5" XOff="0" YOff="0"/>'
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element)
        
        self.assertEqual(stack.shape, PadStackShape.Ellipse)
        self.assertAlmostEqual(stack.width, 1.5, places=4)
        self.assertAlmostEqual(stack.height, 1.5, places=4)
        self.assertAlmostEqual(stack.xoff, 0.0, places=4)
        self.assertAlmostEqual(stack.yoff, 0.0, places=4)
        self.assertIsNone(stack.corner)

    def test_from_xml_obround(self):
        """Test parsing Obround MainStack."""
        xml = '<MainStack Shape="Obround" Width="1.5" Height="1.5" XOff="0" YOff="0"/>'
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element)
        
        self.assertEqual(stack.shape, PadStackShape.Obround)
        self.assertAlmostEqual(stack.width, 1.5, places=4)
        self.assertAlmostEqual(stack.height, 1.5, places=4)

    def test_from_xml_polygon(self):
        """Test parsing Polygon MainStack with points."""
        xml = '''<MainStack Shape="Polygon" Width="2.54" Height="2.032">
            <Points>
                <Point X="1.27" Y="-1.016"/>
                <Point X="1.27" Y="1.016"/>
                <Point X="-1.27" Y="1.016"/>
                <Point X="-1.27" Y="-1.016"/>
            </Points>
        </MainStack>'''
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element)
        
        self.assertEqual(stack.shape, PadStackShape.Polygon)
        self.assertAlmostEqual(stack.width, 2.54, places=4)
        self.assertAlmostEqual(stack.height, 2.032, places=4)
        self.assertEqual(len(stack.points), 4)
        self.assertAlmostEqual(stack.points[0].x, 1.27, places=4)
        self.assertAlmostEqual(stack.points[0].y, -1.016, places=4)

    def test_from_xml_dshape(self):
        """Test parsing D-shape MainStack."""
        xml = '<MainStack Shape="D-shape" Width="1.8" Height="1.8" XOff="0" YOff="0"/>'
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element)
        
        self.assertEqual(stack.shape, PadStackShape.DShape)
        self.assertAlmostEqual(stack.width, 1.8, places=4)
        self.assertAlmostEqual(stack.height, 1.8, places=4)

    def test_from_xml_fiducial(self):
        """Test parsing Fiducial MainStack."""
        xml = '<MainStack Shape="Fiducial" Width="1.0" Height="1.0"/>'
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element)
        
        self.assertEqual(stack.shape, PadStackShape.Fiducial)
        self.assertAlmostEqual(stack.width, 1.0, places=4)
        self.assertAlmostEqual(stack.height, 1.0, places=4)

    def test_to_xml_rectangle_surface(self):
        """Test converting Rectangle MainStack to XML for surface pad."""
        stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=0.6,
            height=2.0,
            corner=25.0
        )
        element = stack.to_xml()
        
        self.assertEqual(element.tag, "MainStack")
        self.assertEqual(element.get("Shape"), "Rectangle")
        self.assertEqual(element.get("Width"), "0.6")
        self.assertEqual(element.get("Height"), "2")
        self.assertEqual(element.get("Corner"), "25")
        self.assertIsNone(element.get("XOff"))
        self.assertIsNone(element.get("YOff"))

    def test_to_xml_ellipse_through(self):
        """Test converting Ellipse MainStack to XML for through-hole pad."""
        stack = MainStack(
            shape=PadStackShape.Ellipse,
            width=1.5,
            height=1.5,
            xoff=0.0,
            yoff=0.0
        )
        element = stack.to_xml()
        
        self.assertEqual(element.tag, "MainStack")
        self.assertEqual(element.get("Shape"), "Ellipse")
        self.assertEqual(element.get("Width"), "1.5")
        self.assertEqual(element.get("Height"), "1.5")
        self.assertEqual(element.get("XOff"), "0")
        self.assertEqual(element.get("YOff"), "0")

    def test_to_xml_polygon(self):
        """Test converting Polygon MainStack to XML with points."""
        stack = MainStack(
            shape=PadStackShape.Polygon,
            width=2.54,
            height=2.032,
            points=[
                Point(1.27, -1.016),
                Point(1.27, 1.016),
                Point(-1.27, 1.016),
                Point(-1.27, -1.016)
            ]
        )
        element = stack.to_xml()
        
        self.assertEqual(element.tag, "MainStack")
        self.assertEqual(element.get("Shape"), "Polygon")
        points_element = element.find("Points")
        self.assertIsNotNone(points_element)
        point_elements = points_element.findall("Point")
        self.assertEqual(len(point_elements), 4)

    def test_unit_conversion_mil(self):
        """Test unit conversion to MIL."""
        stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=2.54,  # 100 mils
            height=1.27,  # 50 mils
            xoff=0.254,  # 10 mils
            yoff=0.508   # 20 mils
        )
        element = stack.to_xml(Units.MIL)
        
        self.assertEqual(element.get("Width"), "100")
        self.assertEqual(element.get("Height"), "50")
        self.assertEqual(element.get("XOff"), "10")
        self.assertEqual(element.get("YOff"), "20")

    def test_unit_conversion_inch(self):
        """Test unit conversion to INCH."""
        stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=2.54,  # 0.1 inches
            height=1.27   # 0.05 inches
        )
        element = stack.to_xml(Units.INCH)
        
        self.assertEqual(element.get("Width"), "0.1")
        self.assertEqual(element.get("Height"), "0.05")

    def test_from_xml_unit_conversion_mil(self):
        """Test parsing MainStack from XML in MIL units."""
        xml = '<MainStack Shape="Rectangle" Width="100" Height="50"/>'
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element, Units.MIL)
        
        # Internal storage should be in MM
        self.assertAlmostEqual(stack.width, 2.54, places=4)
        self.assertAlmostEqual(stack.height, 1.27, places=4)

    def test_from_xml_unit_conversion_inch(self):
        """Test parsing MainStack from XML in INCH units."""
        xml = '<MainStack Shape="Rectangle" Width="0.1" Height="0.05"/>'
        element = etree.fromstring(xml)
        stack = MainStack.from_xml(element, Units.INCH)
        
        # Internal storage should be in MM
        self.assertAlmostEqual(stack.width, 2.54, places=4)
        self.assertAlmostEqual(stack.height, 1.27, places=4)

    def test_roundtrip_conversion(self):
        """Test that parsing and generating XML produces identical result."""
        xml = '<MainStack Shape="Rectangle" Width="0.6" Height="2" Corner="25"/>'
        element1 = etree.fromstring(xml)
        stack = MainStack.from_xml(element1)
        element2 = stack.to_xml()
        
        self.assertEqual(element2.get("Shape"), element1.get("Shape"))
        self.assertEqual(element2.get("Width"), element1.get("Width"))
        self.assertEqual(element2.get("Height"), element1.get("Height"))
        self.assertEqual(element2.get("Corner"), element1.get("Corner"))

    def test_roundtrip_with_offset(self):
        """Test roundtrip with offset attributes."""
        xml = '<MainStack Shape="Ellipse" Width="1.5" Height="1.5" XOff="0.2" YOff="0.3"/>'
        element1 = etree.fromstring(xml)
        stack = MainStack.from_xml(element1)
        element2 = stack.to_xml()
        
        self.assertEqual(element2.get("XOff"), "0.2")
        self.assertEqual(element2.get("YOff"), "0.3")

    def test_corner_zero(self):
        """Test Rectangle with zero corner (sharp corners)."""
        stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=1.0,
            height=1.0,
            corner=0.0
        )
        element = stack.to_xml()
        
        self.assertEqual(element.get("Corner"), "0")

    def test_corner_fifty(self):
        """Test Rectangle with 50% corner (maximum rounding)."""
        stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=1.0,
            height=1.0,
            corner=50.0
        )
        element = stack.to_xml()
        
        self.assertEqual(element.get("Corner"), "50")

    def test_all_shapes(self):
        """Test all supported pad stack shapes."""
        shapes = [
            PadStackShape.Ellipse,
            PadStackShape.Obround,
            PadStackShape.Rectangle,
            PadStackShape.Polygon,
            PadStackShape.DShape,
            PadStackShape.Fiducial
        ]
        
        for shape in shapes:
            with self.subTest(shape=shape):
                stack = MainStack(shape=shape, width=1.0, height=1.0)
                element = stack.to_xml()
                self.assertEqual(element.get("Shape"), shape.value)
                
                # Parse back and verify
                stack2 = MainStack.from_xml(element)
                self.assertEqual(stack2.shape, shape)

    def test_empty_polygon_points(self):
        """Test Polygon shape with no points."""
        stack = MainStack(
            shape=PadStackShape.Polygon,
            width=1.0,
            height=1.0,
            points=[]
        )
        element = stack.to_xml()
        
        points_element = element.find("Points")
        self.assertIsNone(points_element)

    def test_negative_offset(self):
        """Test MainStack with negative offsets."""
        stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=1.0,
            height=1.0,
            xoff=-0.5,
            yoff=-0.3
        )
        element = stack.to_xml()
        
        self.assertEqual(element.get("XOff"), "-0.5")
        self.assertEqual(element.get("YOff"), "-0.3")


if __name__ == "__main__":
    main()
