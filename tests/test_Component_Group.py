#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Group.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Group tests/test_Component_Group.py -v --cov-report=term --cov-report=term-missing

from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator.Component.Group import Group
from DipTraceGenerator import Units


class TestGroup(TestCase):
    """Test cases for Group class"""

    def test_group_default_initialization(self):
        """Test Group initializes with default values"""
        group = Group()
        self.assertEqual(group.id, 0)
        self.assertEqual(group.x, 0.0)
        self.assertEqual(group.y, 0.0)

    def test_group_initialization_with_values(self):
        """Test Group initialization with explicit values"""
        group = Group(id=5, x=10.0, y=20.0)
        self.assertEqual(group.id, 5)
        self.assertEqual(group.x, 10.0)
        self.assertEqual(group.y, 20.0)

    def test_group_initialization_negative_values(self):
        """Test Group can be initialized with negative coordinates"""
        group = Group(id=1, x=-15.0, y=-7.5)
        self.assertEqual(group.id, 1)
        self.assertEqual(group.x, -15.0)
        self.assertEqual(group.y, -7.5)

    def test_from_xml_default_units(self):
        """Test creating Group from XML with default MM units"""
        xml_str = '<Group Id="3" X="10.5" Y="20.3"/>'
        element = xml(xml_str)
        group = Group.from_xml(element)
        
        self.assertEqual(group.id, 3)
        self.assertEqual(group.x, 10.5)
        self.assertEqual(group.y, 20.3)

    def test_from_xml_mil_units(self):
        """Test creating Group from XML with MIL units"""
        xml_str = '<Group Id="0" X="-590.5512" Y="-295.2756"/>'
        element = xml(xml_str)
        group = Group.from_xml(element, units=Units.MIL)
        
        self.assertEqual(group.id, 0)
        self.assertAlmostEqual(group.x, -15.0, places=1)
        self.assertAlmostEqual(group.y, -7.5, places=1)

    def test_from_xml_inch_units(self):
        """Test creating Group from XML with INCH units"""
        xml_str = '<Group Id="2" X="1.0" Y="2.0"/>'
        element = xml(xml_str)
        group = Group.from_xml(element, units=Units.INCH)
        
        # 1 INCH = 25.4 mm, 2 INCH = 50.8 mm
        self.assertAlmostEqual(group.x, 25.4, places=1)
        self.assertAlmostEqual(group.y, 50.8, places=1)

    def test_from_xml_zero_coordinates(self):
        """Test creating Group from XML with zero coordinates"""
        xml_str = '<Group Id="5" X="0.0" Y="0.0"/>'
        element = xml(xml_str)
        group = Group.from_xml(element)
        
        self.assertEqual(group.id, 5)
        self.assertEqual(group.x, 0.0)
        self.assertEqual(group.y, 0.0)

    def test_from_xml_missing_attributes(self):
        """Test Group defaults when XML attributes are missing"""
        xml_str = '<Group/>'
        element = xml(xml_str)
        group = Group.from_xml(element)
        
        self.assertEqual(group.id, 0)
        self.assertEqual(group.x, 0.0)
        self.assertEqual(group.y, 0.0)

    def test_to_xml_default_units(self):
        """Test converting Group to XML with default MM units"""
        group = Group(id=1, x=10.5, y=20.3)
        element = group.to_xml()
        
        self.assertEqual(element.tag, "Group")
        self.assertEqual(element.get("Id"), "1")
        self.assertEqual(element.get("X"), "10.5000")
        self.assertEqual(element.get("Y"), "20.3000")

    def test_to_xml_mil_units(self):
        """Test converting Group to XML with MIL units"""
        group = Group(id=0, x=-15.0, y=-7.5)
        element = group.to_xml(units=Units.MIL)
        
        self.assertEqual(element.get("Id"), "0")
        
        x_val = float(element.get("X"))
        y_val = float(element.get("Y"))
        self.assertAlmostEqual(x_val, -590.55, places=1)
        self.assertAlmostEqual(y_val, -295.28, places=1)

    def test_to_xml_inch_units(self):
        """Test converting Group to XML with INCH units"""
        group = Group(id=2, x=25.4, y=50.8)
        element = group.to_xml(units=Units.INCH)
        
        x_val = float(element.get("X"))
        y_val = float(element.get("Y"))
        
        # 25.4 mm = 1 inch, 50.8 mm = 2 inch
        self.assertAlmostEqual(x_val, 1.0, places=4)
        self.assertAlmostEqual(y_val, 2.0, places=4)

    def test_to_xml_mm_exact_formatting(self):
        """Test MM units use exactly 4 decimal places"""
        group = Group(id=1, x=1.0, y=2.5)
        element = group.to_xml(units=Units.MM)
        
        x_str = element.get("X")
        y_str = element.get("Y")
        
        self.assertEqual(x_str, "1.0000")
        self.assertEqual(y_str, "2.5000")
        self.assertEqual(len(x_str.split('.')[1]), 4)
        self.assertEqual(len(y_str.split('.')[1]), 4)

    def test_to_xml_mil_exact_formatting(self):
        """Test MIL units use exactly 4 decimal places"""
        group = Group(id=0, x=2.54, y=5.08)  # 100 MIL, 200 MIL
        element = group.to_xml(units=Units.MIL)
        
        x_str = element.get("X")
        y_str = element.get("Y")
        
        self.assertEqual(len(x_str.split('.')[1]), 4)
        self.assertEqual(len(y_str.split('.')[1]), 4)

    def test_to_xml_inch_exact_formatting(self):
        """Test INCH units use exactly 6 decimal places"""
        group = Group(id=1, x=25.4, y=50.8)  # 1 INCH, 2 INCH
        element = group.to_xml(units=Units.INCH)
        
        x_str = element.get("X")
        y_str = element.get("Y")
        
        self.assertEqual(len(x_str.split('.')[1]), 6)
        self.assertEqual(len(y_str.split('.')[1]), 6)

    def test_round_trip_mm(self):
        """Test round-trip: Group -> XML -> Group with MM units"""
        original = Group(id=3, x=15.0, y=25.0)
        element = original.to_xml(units=Units.MM)
        recovered = Group.from_xml(element, units=Units.MM)
        
        self.assertEqual(recovered.id, original.id)
        self.assertAlmostEqual(recovered.x, original.x, places=4)
        self.assertAlmostEqual(recovered.y, original.y, places=4)

    def test_round_trip_mil(self):
        """Test round-trip: Group -> XML -> Group with MIL units"""
        original = Group(id=0, x=-15.0, y=-7.5)
        element = original.to_xml(units=Units.MIL)
        recovered = Group.from_xml(element, units=Units.MIL)
        
        self.assertEqual(recovered.id, original.id)
        self.assertAlmostEqual(recovered.x, original.x, places=4)
        self.assertAlmostEqual(recovered.y, original.y, places=4)

    def test_round_trip_inch(self):
        """Test round-trip: Group -> XML -> Group with INCH units"""
        original = Group(id=2, x=25.4, y=50.8)
        element = original.to_xml(units=Units.INCH)
        recovered = Group.from_xml(element, units=Units.INCH)
        
        self.assertEqual(recovered.id, original.id)
        self.assertAlmostEqual(recovered.x, original.x, places=4)
        self.assertAlmostEqual(recovered.y, original.y, places=4)

    def test_multiple_groups_different_ids(self):
        """Test creating multiple groups with different IDs"""
        group1 = Group(id=0, x=10.0, y=20.0)
        group2 = Group(id=1, x=30.0, y=40.0)
        group3 = Group(id=2, x=50.0, y=60.0)
        
        self.assertEqual(group1.id, 0)
        self.assertEqual(group2.id, 1)
        self.assertEqual(group3.id, 2)

    def test_xml_element_structure(self):
        """Test that Group XML element has correct structure"""
        group = Group(id=1, x=10.0, y=20.0)
        element = group.to_xml()
        
        # Should have no child elements
        self.assertEqual(len(element), 0)
        
        # Should have exactly 3 attributes
        self.assertEqual(len(element.attrib), 3)
        self.assertIn("Id", element.attrib)
        self.assertIn("X", element.attrib)
        self.assertIn("Y", element.attrib)

    def test_large_group_id(self):
        """Test Group with large ID value"""
        group = Group(id=9999, x=0.0, y=0.0)
        element = group.to_xml()
        recovered = Group.from_xml(element)
        
        self.assertEqual(recovered.id, 9999)

    def test_shapes_elixml_sample_group(self):
        """Test parsing the actual group from shapes.elixml sample"""
        xml_str = '<Group Id="0" X="-590.5512" Y="-295.2756"/>'
        element = xml(xml_str)
        group = Group.from_xml(element, units=Units.MIL)
        
        self.assertEqual(group.id, 0)
        self.assertAlmostEqual(group.x, -15.0, places=1)
        self.assertAlmostEqual(group.y, -7.5, places=1)
        
        # Test round-trip
        element_out = group.to_xml(units=Units.MIL)
        x_val = float(element_out.get("X"))
        y_val = float(element_out.get("Y"))
        
        self.assertAlmostEqual(x_val, -590.5512, places=2)
        self.assertAlmostEqual(y_val, -295.2756, places=2)


if __name__ == "__main__":
    main()
