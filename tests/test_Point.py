#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Point.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Point tests/test_Point.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from DipTraceGenerator import Point, Units
from lxml.etree import fromstring as xml


class TestPoint(TestCase):
    """Test cases for Point dataclass"""

    def test_point_default_initialization(self):
        """Test that Point initializes with default values (0.0, 0.0)"""
        point = Point()
        self.assertEqual(point.x, 0.0)
        self.assertEqual(point.y, 0.0)

    def test_point_initialization_with_values(self):
        """Test Point initialization with explicit x and y values"""
        point = Point(x=10.5, y=20.3)
        self.assertEqual(point.x, 10.5)
        self.assertEqual(point.y, 20.3)

    def test_point_initialization_negative_values(self):
        """Test Point initialization with negative coordinates"""
        point = Point(x=-5.0, y=-10.0)
        self.assertEqual(point.x, -5.0)
        self.assertEqual(point.y, -10.0)

    def test_from_xml_default_units_mm(self):
        """Test creating a Point from XML with default units (mm)"""
        element = xml('<Point X="12.5" Y="34.5"/>')
        point = Point.from_xml(element)
        self.assertEqual(point.x, 12.5)
        self.assertEqual(point.y, 34.5)

    def test_from_xml_explicit_mm_units(self):
        """Test creating a Point from XML with explicit MM units"""
        element = xml('<Point X="25.4" Y="50.8"/>')
        point = Point.from_xml(element, units=Units.MM)
        self.assertEqual(point.x, 25.4)
        self.assertEqual(point.y, 50.8)

    def test_from_xml_inch_units(self):
        """Test creating a Point from XML with INCH units (converts to mm internally)"""
        element = xml('<Point X="1.0" Y="2.0"/>')
        point = Point.from_xml(element, units=Units.INCH)
        # 1 inch = 25.4 mm
        self.assertAlmostEqual(point.x, 25.4, places=10)
        self.assertAlmostEqual(point.y, 50.8, places=10)

    def test_from_xml_mil_units(self):
        """Test creating a Point from XML with MIL units (converts to mm internally)"""
        element = xml('<Point X="1000.0" Y="2000.0"/>')
        point = Point.from_xml(element, units=Units.MIL)
        # 1000 mil = 25.4 mm
        self.assertAlmostEqual(point.x, 25.4, places=10)
        self.assertAlmostEqual(point.y, 50.8, places=10)

    def test_from_xml_missing_x_attribute(self):
        """Test creating a Point from XML with missing X attribute (defaults to 0.0)"""
        element = xml('<Point Y="10.0"/>')
        point = Point.from_xml(element)
        self.assertEqual(point.x, 0.0)
        self.assertEqual(point.y, 10.0)

    def test_from_xml_missing_y_attribute(self):
        """Test creating a Point from XML with missing Y attribute (defaults to 0.0)"""
        element = xml('<Point X="10.0"/>')
        point = Point.from_xml(element)
        self.assertEqual(point.x, 10.0)
        self.assertEqual(point.y, 0.0)

    def test_from_xml_missing_both_attributes(self):
        """Test creating a Point from XML with missing X and Y attributes"""
        element = xml('<Point/>')
        point = Point.from_xml(element)
        self.assertEqual(point.x, 0.0)
        self.assertEqual(point.y, 0.0)

    def test_from_xml_negative_coordinates(self):
        """Test creating a Point from XML with negative coordinates"""
        element = xml('<Point X="-10.5" Y="-20.3"/>')
        point = Point.from_xml(element)
        self.assertEqual(point.x, -10.5)
        self.assertEqual(point.y, -20.3)

    def test_to_xml_default_units_mm(self):
        """Test converting a Point to XML with default units (mm)"""
        point = Point(x=56.7, y=89.1)
        element = point.to_xml()
        self.assertEqual(element.tag, "Point")
        self.assertEqual(element.get("X"), "56.7000")
        self.assertEqual(element.get("Y"), "89.1000")

    def test_to_xml_explicit_mm_units(self):
        """Test converting a Point to XML with explicit MM units"""
        point = Point(x=25.4, y=50.8)
        element = point.to_xml(units=Units.MM)
        self.assertEqual(element.tag, "Point")
        self.assertEqual(element.get("X"), "25.4000")
        self.assertEqual(element.get("Y"), "50.8000")

    def test_to_xml_inch_units(self):
        """Test converting a Point to XML with INCH units"""
        point = Point(x=25.4, y=50.8)  # Internal representation in mm
        element = point.to_xml(units=Units.INCH)
        self.assertEqual(element.tag, "Point")
        # 25.4 mm = 1 inch, should have 6 decimal places for INCH
        self.assertEqual(element.get("X"), "1.000000")
        self.assertEqual(element.get("Y"), "2.000000")

    def test_to_xml_mil_units(self):
        """Test converting a Point to XML with MIL units"""
        point = Point(x=25.4, y=50.8)  # Internal representation in mm
        element = point.to_xml(units=Units.MIL)
        self.assertEqual(element.tag, "Point")
        # 25.4 mm = 1000 mil
        self.assertEqual(element.get("X"), "1000.0000")
        self.assertEqual(element.get("Y"), "2000.0000")

    def test_to_xml_rounding_mm_4_decimals(self):
        """Test that MM units use 4 decimal places"""
        point = Point(x=12.345678, y=23.456789)
        element = point.to_xml(units=Units.MM)
        # Should be rounded to 4 decimal places
        self.assertEqual(element.get("X"), "12.3457")
        self.assertEqual(element.get("Y"), "23.4568")

    def test_to_xml_rounding_inch_6_decimals(self):
        """Test that INCH units use 6 decimal places"""
        point = Point(x=12.345678, y=23.456789)
        element = point.to_xml(units=Units.INCH)
        # Convert to inches and format to 6 decimal places
        x_inch = 12.345678 / 25.4
        y_inch = 23.456789 / 25.4
        self.assertEqual(element.get("X"), f"{x_inch:.6f}")
        self.assertEqual(element.get("Y"), f"{y_inch:.6f}")

    def test_to_xml_rounding_mil_4_decimals(self):
        """Test that MIL units use 4 decimal places"""
        point = Point(x=1.0, y=2.0)
        element = point.to_xml(units=Units.MIL)
        # 1mm = 39.3701 mil, rounded to 4 decimals
        self.assertEqual(element.get("X"), "39.3701")
        self.assertEqual(element.get("Y"), "78.7402")

    def test_to_xml_zero_coordinates(self):
        """Test converting Point with zero coordinates to XML"""
        point = Point(x=0.0, y=0.0)
        element = point.to_xml()
        self.assertEqual(element.get("X"), "0.0000")
        self.assertEqual(element.get("Y"), "0.0000")

    def test_to_xml_negative_coordinates(self):
        """Test converting Point with negative coordinates to XML"""
        point = Point(x=-10.5, y=-20.3)
        element = point.to_xml()
        self.assertEqual(element.get("X"), "-10.5000")
        self.assertEqual(element.get("Y"), "-20.3000")

    def test_round_trip_mm_to_xml_and_back(self):
        """Test round-trip: Point -> XML -> Point with MM units"""
        original = Point(x=12.3456, y=23.4567)
        element = original.to_xml(units=Units.MM)
        recovered = Point.from_xml(element, units=Units.MM)
        # After rounding to 4 decimals
        self.assertAlmostEqual(recovered.x, 12.3456, places=4)
        self.assertAlmostEqual(recovered.y, 23.4567, places=4)

    def test_round_trip_inch_to_xml_and_back(self):
        """Test round-trip: Point -> XML -> Point with INCH units"""
        original = Point(x=25.4, y=50.8)  # 1 and 2 inches in mm
        element = original.to_xml(units=Units.INCH)
        recovered = Point.from_xml(element, units=Units.INCH)
        self.assertAlmostEqual(recovered.x, 25.4, places=5)
        self.assertAlmostEqual(recovered.y, 50.8, places=5)

    def test_round_trip_mil_to_xml_and_back(self):
        """Test round-trip: Point -> XML -> Point with MIL units"""
        original = Point(x=25.4, y=50.8)  # 1000 and 2000 mils in mm
        element = original.to_xml(units=Units.MIL)
        recovered = Point.from_xml(element, units=Units.MIL)
        self.assertAlmostEqual(recovered.x, 25.4, places=4)
        self.assertAlmostEqual(recovered.y, 50.8, places=4)

    def test_real_world_pcb_coordinate(self):
        """Test with real-world PCB coordinates (e.g., 2.54mm pitch)"""
        point = Point(x=2.54, y=5.08)
        element = point.to_xml(units=Units.MIL)
        # 2.54mm = 100mil, 5.08mm = 200mil
        self.assertEqual(element.get("X"), "100.0000")
        self.assertEqual(element.get("Y"), "200.0000")

    def test_dataclass_equality(self):
        """Test that two Points with same coordinates are equal"""
        point1 = Point(x=10.0, y=20.0)
        point2 = Point(x=10.0, y=20.0)
        self.assertEqual(point1, point2)

    def test_dataclass_inequality(self):
        """Test that two Points with different coordinates are not equal"""
        point1 = Point(x=10.0, y=20.0)
        point2 = Point(x=10.0, y=21.0)
        self.assertNotEqual(point1, point2)

    def test_to_xml_exact_mm_4_digits_with_trailing_zeros(self):
        """Test that MM units always produce exactly 4 digits after decimal point"""
        point = Point(x=1.0, y=2.5)
        element = point.to_xml(units=Units.MM)
        # Should have exactly 4 digits, including trailing zeros
        self.assertEqual(element.get("X"), "1.0000")
        self.assertEqual(element.get("Y"), "2.5000")

    def test_to_xml_exact_inch_6_digits_with_trailing_zeros(self):
        """Test that INCH units always produce exactly 6 digits after decimal point"""
        point = Point(x=25.4, y=50.8)  # 1.0 and 2.0 inches
        element = point.to_xml(units=Units.INCH)
        # Should have exactly 6 digits, including trailing zeros
        self.assertEqual(element.get("X"), "1.000000")
        self.assertEqual(element.get("Y"), "2.000000")

    def test_to_xml_exact_mil_4_digits_with_trailing_zeros(self):
        """Test that MIL units always produce exactly 4 digits after decimal point"""
        point = Point(x=25.4, y=50.8)  # 1000.0 and 2000.0 mils
        element = point.to_xml(units=Units.MIL)
        # Should have exactly 4 digits, including trailing zeros
        self.assertEqual(element.get("X"), "1000.0000")
        self.assertEqual(element.get("Y"), "2000.0000")

    def test_to_xml_zero_has_exact_digits_mm(self):
        """Test that zero coordinates have exact 4 digits for MM"""
        point = Point(x=0.0, y=0.0)
        element = point.to_xml(units=Units.MM)
        self.assertEqual(element.get("X"), "0.0000")
        self.assertEqual(element.get("Y"), "0.0000")

    def test_to_xml_zero_has_exact_digits_inch(self):
        """Test that zero coordinates have exact 6 digits for INCH"""
        point = Point(x=0.0, y=0.0)
        element = point.to_xml(units=Units.INCH)
        self.assertEqual(element.get("X"), "0.000000")
        self.assertEqual(element.get("Y"), "0.000000")

    def test_to_xml_floating_point_edge_case_2675(self):
        """Test that 2.675 rounds correctly (binary float edge case)"""
        # 2.675 can't be represented exactly in binary, tests proper rounding
        point = Point(x=2.675, y=3.675)
        element = point.to_xml(units=Units.MM)
        # Should round to 4 decimals consistently
        x_val = element.get("X")
        y_val = element.get("Y")
        # Verify format has exactly 4 decimals
        self.assertEqual(len(x_val.split('.')[-1]), 4)
        self.assertEqual(len(y_val.split('.')[-1]), 4)

    def test_to_xml_floating_point_edge_case_3_thirds(self):
        """Test that 1/3 (0.333...) formats correctly"""
        point = Point(x=1.0/3.0, y=2.0/3.0)
        element = point.to_xml(units=Units.MM)
        x_val = element.get("X")
        y_val = element.get("Y")
        # Verify format has exactly 4 decimals
        self.assertEqual(len(x_val.split('.')[-1]), 4)
        self.assertEqual(len(y_val.split('.')[-1]), 4)
        # Values should be truncated/rounded to 4 decimals
        self.assertTrue(x_val.startswith("0.3333"))
        self.assertTrue(y_val.startswith("0.6667"))

    def test_to_xml_negative_has_exact_digits(self):
        """Test that negative coordinates have exact digit formatting"""
        point = Point(x=-1.5, y=-2.5)
        element = point.to_xml(units=Units.MM)
        self.assertEqual(element.get("X"), "-1.5000")
        self.assertEqual(element.get("Y"), "-2.5000")

    def test_to_xml_very_small_value_formatting(self):
        """Test formatting of very small values (near zero)"""
        point = Point(x=0.00001, y=0.00009)
        element = point.to_xml(units=Units.MM)
        x_val = element.get("X")
        y_val = element.get("Y")
        # Should have exactly 4 decimals
        self.assertEqual(len(x_val.split('.')[-1]), 4)
        self.assertEqual(len(y_val.split('.')[-1]), 4)
        self.assertEqual(x_val, "0.0000")  # Rounds to 0.0000
        self.assertEqual(y_val, "0.0001")  # Rounds to 0.0001

    def test_to_xml_large_value_formatting(self):
        """Test formatting of large values"""
        point = Point(x=12345.6789, y=98765.4321)
        element = point.to_xml(units=Units.MM)
        x_val = element.get("X")
        y_val = element.get("Y")
        # Should have exactly 4 decimals even for large numbers
        self.assertEqual(len(x_val.split('.')[-1]), 4)
        self.assertEqual(len(y_val.split('.')[-1]), 4)
        self.assertEqual(x_val, "12345.6789")
        self.assertEqual(y_val, "98765.4321")


if __name__ == "__main__":
    main()