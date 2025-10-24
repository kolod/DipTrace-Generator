#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Origin.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Origin tests/test_Component_Origin.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator.Component.Origin import Origin
from DipTraceGenerator import Units


class TestComponentOrigin(TestCase):
    """Test cases for Component Origin class"""

    def test_default_initialization(self):
        """Test Origin initializes with default values"""
        origin = Origin()
        self.assertEqual(origin.x, 0.0)
        self.assertEqual(origin.y, 0.0)

    def test_initialization_with_values(self):
        """Test Origin initialization with explicit values"""
        origin = Origin(x=10.5, y=-20.3)
        self.assertEqual(origin.x, 10.5)
        self.assertEqual(origin.y, -20.3)

    def test_initialization_negative_values(self):
        """Test Origin can be initialized with negative values"""
        origin = Origin(x=-15.0, y=-12.5)
        self.assertEqual(origin.x, -15.0)
        self.assertEqual(origin.y, -12.5)

    def test_from_xml_default_units(self):
        """Test creating Origin from XML with default MM units"""
        xml_str = '<Origin X="10.5" Y="20.3"/>'
        element = xml(xml_str)
        origin = Origin.from_xml(element)
        
        self.assertEqual(origin.x, 10.5)
        self.assertEqual(origin.y, 20.3)

    def test_from_xml_negative_coordinates(self):
        """Test creating Origin from XML with negative coordinates"""
        xml_str = '<Origin X="-590.5512" Y="-492.126"/>'
        element = xml(xml_str)
        origin = Origin.from_xml(element, units=Units.MIL)
        
        # -590.5512 MIL = -15.0 mm, -492.126 MIL = -12.5 mm (approximately)
        self.assertAlmostEqual(origin.x, -15.0, places=1)
        self.assertAlmostEqual(origin.y, -12.5, places=1)

    def test_from_xml_mil_units(self):
        """Test creating Origin from XML with MIL units"""
        xml_str = '<Origin X="100.0" Y="200.0"/>'
        element = xml(xml_str)
        origin = Origin.from_xml(element, units=Units.MIL)
        
        # 100 MIL = 2.54 mm, 200 MIL = 5.08 mm
        self.assertAlmostEqual(origin.x, 2.54, places=2)
        self.assertAlmostEqual(origin.y, 5.08, places=2)

    def test_from_xml_inch_units(self):
        """Test creating Origin from XML with INCH units"""
        xml_str = '<Origin X="1.0" Y="2.0"/>'
        element = xml(xml_str)
        origin = Origin.from_xml(element, units=Units.INCH)
        
        # 1 INCH = 25.4 mm, 2 INCH = 50.8 mm
        self.assertAlmostEqual(origin.x, 25.4, places=1)
        self.assertAlmostEqual(origin.y, 50.8, places=1)

    def test_from_xml_zero_values(self):
        """Test creating Origin from XML with zero values"""
        xml_str = '<Origin X="0.0" Y="0.0"/>'
        element = xml(xml_str)
        origin = Origin.from_xml(element)
        
        self.assertEqual(origin.x, 0.0)
        self.assertEqual(origin.y, 0.0)

    def test_from_xml_missing_attributes(self):
        """Test creating Origin from XML with missing attributes defaults to 0"""
        xml_str = '<Origin/>'
        element = xml(xml_str)
        origin = Origin.from_xml(element)
        
        self.assertEqual(origin.x, 0.0)
        self.assertEqual(origin.y, 0.0)

    def test_to_xml_default_units(self):
        """Test converting Origin to XML with default MM units"""
        origin = Origin(x=10.5, y=20.3)
        element = origin.to_xml()
        
        self.assertEqual(element.tag, "Origin")
        self.assertEqual(element.get("X"), "10.5000")
        self.assertEqual(element.get("Y"), "20.3000")

    def test_to_xml_mil_units(self):
        """Test converting Origin to XML with MIL units"""
        origin = Origin(x=2.54, y=5.08)  # in mm
        element = origin.to_xml(units=Units.MIL)
        
        # 2.54 mm = 100 MIL, 5.08 mm = 200 MIL
        x_val = float(element.get("X"))
        y_val = float(element.get("Y"))
        self.assertAlmostEqual(x_val, 100.0, places=2)
        self.assertAlmostEqual(y_val, 200.0, places=2)

    def test_to_xml_inch_units(self):
        """Test converting Origin to XML with INCH units"""
        origin = Origin(x=25.4, y=50.8)  # in mm
        element = origin.to_xml(units=Units.INCH)
        
        # 25.4 mm = 1 INCH, 50.8 mm = 2 INCH
        x_val = float(element.get("X"))
        y_val = float(element.get("Y"))
        self.assertAlmostEqual(x_val, 1.0, places=4)
        self.assertAlmostEqual(y_val, 2.0, places=4)

    def test_to_xml_negative_values(self):
        """Test converting Origin with negative values to XML"""
        origin = Origin(x=-15.0, y=-12.5)
        element = origin.to_xml(units=Units.MIL)
        
        x_val = float(element.get("X"))
        y_val = float(element.get("Y"))
        self.assertLess(x_val, 0)
        self.assertLess(y_val, 0)

    def test_to_xml_zero_values(self):
        """Test converting Origin with zero values to XML"""
        origin = Origin(x=0.0, y=0.0)
        element = origin.to_xml()
        
        self.assertEqual(element.get("X"), "0.0000")
        self.assertEqual(element.get("Y"), "0.0000")

    def test_to_xml_mm_exact_formatting(self):
        """Test MM units use exactly 4 decimal places"""
        origin = Origin(x=1.0, y=2.5)
        element = origin.to_xml(units=Units.MM)
        
        x_str = element.get("X")
        y_str = element.get("Y")
        
        # Check format has exactly 4 decimal places
        self.assertEqual(x_str, "1.0000")
        self.assertEqual(y_str, "2.5000")
        self.assertEqual(len(x_str.split('.')[1]), 4)
        self.assertEqual(len(y_str.split('.')[1]), 4)

    def test_to_xml_mil_exact_formatting(self):
        """Test MIL units use exactly 4 decimal places"""
        origin = Origin(x=2.54, y=5.08)  # 100 MIL, 200 MIL
        element = origin.to_xml(units=Units.MIL)
        
        x_str = element.get("X")
        y_str = element.get("Y")
        
        # Check format has exactly 4 decimal places
        self.assertEqual(len(x_str.split('.')[1]), 4)
        self.assertEqual(len(y_str.split('.')[1]), 4)

    def test_to_xml_inch_exact_formatting(self):
        """Test INCH units use exactly 6 decimal places"""
        origin = Origin(x=25.4, y=50.8)  # 1 INCH, 2 INCH
        element = origin.to_xml(units=Units.INCH)
        
        x_str = element.get("X")
        y_str = element.get("Y")
        
        # Check format has exactly 6 decimal places
        self.assertEqual(len(x_str.split('.')[1]), 6)
        self.assertEqual(len(y_str.split('.')[1]), 6)

    def test_round_trip_mm(self):
        """Test round-trip: Origin -> XML -> Origin with MM units"""
        original = Origin(x=10.5, y=20.3)
        element = original.to_xml(units=Units.MM)
        recovered = Origin.from_xml(element, units=Units.MM)
        
        self.assertAlmostEqual(recovered.x, original.x, places=4)
        self.assertAlmostEqual(recovered.y, original.y, places=4)

    def test_round_trip_mil(self):
        """Test round-trip: Origin -> XML -> Origin with MIL units"""
        original = Origin(x=15.0, y=12.5)
        element = original.to_xml(units=Units.MIL)
        recovered = Origin.from_xml(element, units=Units.MIL)
        
        self.assertAlmostEqual(recovered.x, original.x, places=4)
        self.assertAlmostEqual(recovered.y, original.y, places=4)

    def test_round_trip_inch(self):
        """Test round-trip: Origin -> XML -> Origin with INCH units"""
        original = Origin(x=25.4, y=50.8)
        element = original.to_xml(units=Units.INCH)
        recovered = Origin.from_xml(element, units=Units.INCH)
        
        self.assertAlmostEqual(recovered.x, original.x, places=4)
        self.assertAlmostEqual(recovered.y, original.y, places=4)

    def test_round_trip_negative_values(self):
        """Test round-trip with negative coordinates"""
        original = Origin(x=-15.0, y=-12.5)
        element = original.to_xml(units=Units.MIL)
        recovered = Origin.from_xml(element, units=Units.MIL)
        
        self.assertAlmostEqual(recovered.x, original.x, places=4)
        self.assertAlmostEqual(recovered.y, original.y, places=4)

    def test_round_trip_zero_values(self):
        """Test round-trip with zero coordinates"""
        original = Origin(x=0.0, y=0.0)
        element = original.to_xml(units=Units.MM)
        recovered = Origin.from_xml(element, units=Units.MM)
        
        self.assertEqual(recovered.x, 0.0)
        self.assertEqual(recovered.y, 0.0)

    def test_equality_same_values(self):
        """Test two Origins with same values are equal"""
        origin1 = Origin(x=10.5, y=20.3)
        origin2 = Origin(x=10.5, y=20.3)
        
        self.assertEqual(origin1.x, origin2.x)
        self.assertEqual(origin1.y, origin2.y)

    def test_different_origins_not_equal(self):
        """Test two Origins with different values are not equal"""
        origin1 = Origin(x=10.5, y=20.3)
        origin2 = Origin(x=15.0, y=25.0)
        
        self.assertNotEqual(origin1.x, origin2.x)
        self.assertNotEqual(origin1.y, origin2.y)

    def test_large_values(self):
        """Test Origin with large coordinate values"""
        origin = Origin(x=1000.0, y=2000.0)
        element = origin.to_xml(units=Units.MM)
        recovered = Origin.from_xml(element, units=Units.MM)
        
        self.assertAlmostEqual(recovered.x, 1000.0, places=4)
        self.assertAlmostEqual(recovered.y, 2000.0, places=4)

    def test_small_values(self):
        """Test Origin with very small coordinate values"""
        origin = Origin(x=0.001, y=0.002)
        element = origin.to_xml(units=Units.MM)
        recovered = Origin.from_xml(element, units=Units.MM)
        
        self.assertAlmostEqual(recovered.x, 0.001, places=4)
        self.assertAlmostEqual(recovered.y, 0.002, places=4)

    def test_user_example_coordinates(self):
        """Test with the user's example: <Origin X="-590.5512" Y="-492.126"/>"""
        xml_str = '<Origin X="-590.5512" Y="-492.126"/>'
        element = xml(xml_str)
        origin = Origin.from_xml(element, units=Units.MIL)
        
        # Verify values are converted correctly
        self.assertAlmostEqual(origin.x, -15.0, places=1)
        self.assertAlmostEqual(origin.y, -12.5, places=1)
        
        # Test round-trip
        element_out = origin.to_xml(units=Units.MIL)
        x_val = float(element_out.get("X"))
        y_val = float(element_out.get("Y"))
        
        self.assertAlmostEqual(x_val, -590.5512, places=2)
        self.assertAlmostEqual(y_val, -492.126, places=2)


if __name__ == "__main__":
    main()
