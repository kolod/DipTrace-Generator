#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Units.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator tests/test_Units.py -v --cov -report=term --cov-report=term-missing

from unittest import TestCase, main
from DipTraceGenerator import Units, convert_units


class TestUnits(TestCase):
    """Test cases for Units enum and convert_units function"""

    def test_units_enum_values(self):
        """Test that Units enum has correct values"""
        self.assertEqual(Units.MM.value, "mm")
        self.assertEqual(Units.INCH.value, "inch")
        self.assertEqual(Units.MIL.value, "mil")

    def test_convert_no_conversion_mm(self):
        """Test conversion from MM to MM (no conversion needed)"""
        result = convert_units(10.0, Units.MM, Units.MM)
        self.assertEqual(result, 10.0)

    def test_convert_no_conversion_inch(self):
        """Test conversion from INCH to INCH (no conversion needed)"""
        result = convert_units(5.0, Units.INCH, Units.INCH)
        self.assertEqual(result, 5.0)

    def test_convert_no_conversion_mil(self):
        """Test conversion from MIL to MIL (no conversion needed)"""
        result = convert_units(100.0, Units.MIL, Units.MIL)
        self.assertEqual(result, 100.0)

    def test_convert_mm_to_inch(self):
        """Test conversion from millimeters to inches"""
        result = convert_units(25.4, Units.MM, Units.INCH)
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_convert_mm_to_mil(self):
        """Test conversion from millimeters to mils"""
        result = convert_units(25.4, Units.MM, Units.MIL)
        self.assertAlmostEqual(result, 1000.0, places=10)

    def test_convert_inch_to_mm(self):
        """Test conversion from inches to millimeters"""
        result = convert_units(1.0, Units.INCH, Units.MM)
        self.assertAlmostEqual(result, 25.4, places=10)

    def test_convert_inch_to_mil(self):
        """Test conversion from inches to mils"""
        result = convert_units(1.0, Units.INCH, Units.MIL)
        self.assertAlmostEqual(result, 1000.0, places=10)

    def test_convert_mil_to_mm(self):
        """Test conversion from mils to millimeters"""
        result = convert_units(1000.0, Units.MIL, Units.MM)
        self.assertAlmostEqual(result, 25.4, places=10)

    def test_convert_mil_to_inch(self):
        """Test conversion from mils to inches"""
        result = convert_units(1000.0, Units.MIL, Units.INCH)
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_convert_zero_value(self):
        """Test conversion of zero value"""
        result = convert_units(0.0, Units.MM, Units.INCH)
        self.assertEqual(result, 0.0)

    def test_convert_negative_value(self):
        """Test conversion of negative value"""
        result = convert_units(-25.4, Units.MM, Units.INCH)
        self.assertAlmostEqual(result, -1.0, places=10)

    def test_convert_fractional_value(self):
        """Test conversion of fractional value"""
        result = convert_units(12.7, Units.MM, Units.INCH)
        self.assertAlmostEqual(result, 0.5, places=10)

    def test_convert_large_value(self):
        """Test conversion of large value"""
        result = convert_units(1000.0, Units.MM, Units.INCH)
        self.assertAlmostEqual(result, 39.3700787, places=6)

    def test_convert_small_value(self):
        """Test conversion of very small value"""
        result = convert_units(0.001, Units.MM, Units.MIL)
        self.assertAlmostEqual(result, 0.03937, places=5)

    def test_convert_precision_mm_inch_mm(self):
        """Test conversion precision: MM -> INCH -> MM"""
        original = 123.456
        to_inch = convert_units(original, Units.MM, Units.INCH)
        back_to_mm = convert_units(to_inch, Units.INCH, Units.MM)
        self.assertAlmostEqual(back_to_mm, original, places=10)

    def test_convert_precision_inch_mil_inch(self):
        """Test conversion precision: INCH -> MIL -> INCH"""
        original = 5.5
        to_mil = convert_units(original, Units.INCH, Units.MIL)
        back_to_inch = convert_units(to_mil, Units.MIL, Units.INCH)
        self.assertAlmostEqual(back_to_inch, original, places=10)

    def test_convert_precision_mil_mm_mil(self):
        """Test conversion precision: MIL -> MM -> MIL"""
        original = 500.0
        to_mm = convert_units(original, Units.MIL, Units.MM)
        back_to_mil = convert_units(to_mm, Units.MM, Units.MIL)
        self.assertAlmostEqual(back_to_mil, original, places=10)

    def test_convert_real_world_pcb_trace_width(self):
        """Test conversion of typical PCB trace width (0.2mm = 7.874mil)"""
        result = convert_units(0.2, Units.MM, Units.MIL)
        self.assertAlmostEqual(result, 7.874, places=3)

    def test_convert_real_world_component_pitch(self):
        """Test conversion of typical component pitch (2.54mm = 100mil = 0.1inch)"""
        mm_to_mil = convert_units(2.54, Units.MM, Units.MIL)
        self.assertAlmostEqual(mm_to_mil, 100.0, places=5)
        
        mm_to_inch = convert_units(2.54, Units.MM, Units.INCH)
        self.assertAlmostEqual(mm_to_inch, 0.1, places=5)

    def test_convert_real_world_via_diameter(self):
        """Test conversion of typical via diameter (0.3mm)"""
        result = convert_units(0.3, Units.MM, Units.MIL)
        self.assertAlmostEqual(result, 11.811, places=3)

    def test_can_import_units_and_convert_units(self):
        """Test that Units and convert_units can be imported"""
        # This test passes if the imports at the top of the file work
        self.assertTrue(callable(convert_units))
        self.assertTrue(hasattr(Units, 'MM'))
        self.assertTrue(hasattr(Units, 'INCH'))
        self.assertTrue(hasattr(Units, 'MIL'))

    def test_convert_unsupported_from_unit(self):
        """Test that ValueError is raised for unsupported from_unit"""
        # Create a mock unsupported unit by patching the enum check
        with self.assertRaises(ValueError) as cm:
            # Pass a string that's not one of the valid enum values
            # We need to bypass the enum type check, so we'll pass an invalid value
            convert_units(10.0, "invalid_unit", Units.MM)
        
        self.assertIn("Unsupported from_unit", str(cm.exception))

    def test_convert_unsupported_to_unit(self):
        """Test that ValueError is raised for unsupported to_unit"""
        with self.assertRaises(ValueError) as cm:
            # Pass a string that's not one of the valid enum values
            convert_units(10.0, Units.MM, "invalid_unit")
        
        self.assertIn("Unsupported to_unit", str(cm.exception))


if __name__ == "__main__":
    main()