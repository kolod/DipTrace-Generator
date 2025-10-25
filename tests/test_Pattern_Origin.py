#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Pattern_Origin.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Pattern.Origin tests/test_Pattern_Origin.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml import etree
from DipTraceGenerator.Pattern import Origin
from DipTraceGenerator import Units, Boolean


class TestOrigin(TestCase):
    """Test the Pattern.Origin class."""
    
    def test_create_origin_defaults(self):
        """Test creating an Origin with default values."""
        origin = Origin()
        self.assertEqual(origin.x, 0.0)
        self.assertEqual(origin.y, 0.0)
        self.assertEqual(origin.cross, Boolean.Yes)
        self.assertEqual(origin.circle, Boolean.Yes)
        self.assertEqual(origin.common, "Hide")
        self.assertEqual(origin.courtyard, "Show")
    
    def test_create_origin_with_values(self):
        """Test creating an Origin with specific values."""
        origin = Origin(
            x=-1.27,
            y=0.635,
            cross=Boolean.No,
            circle=Boolean.No,
            common="Show",
            courtyard="Hide"
        )
        self.assertAlmostEqual(origin.x, -1.27, places=4)
        self.assertAlmostEqual(origin.y, 0.635, places=4)
        self.assertEqual(origin.cross, Boolean.No)
        self.assertEqual(origin.circle, Boolean.No)
        self.assertEqual(origin.common, "Show")
        self.assertEqual(origin.courtyard, "Hide")
    
    def test_from_xml_centered_origin(self):
        """Test parsing a centered origin (0,0) from XML."""
        xml_element = etree.fromstring('''
            <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertAlmostEqual(origin.x, 0.0, places=4)
        self.assertAlmostEqual(origin.y, 0.0, places=4)
        self.assertEqual(origin.cross, Boolean.Yes)
        self.assertEqual(origin.circle, Boolean.Yes)
        self.assertEqual(origin.common, "Hide")
        self.assertEqual(origin.courtyard, "Show")
    
    def test_from_xml_offset_origin(self):
        """Test parsing an offset origin from XML."""
        xml_element = etree.fromstring('''
            <Origin X="-1.27" Y="0.635" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertAlmostEqual(origin.x, -1.27, places=4)
        self.assertAlmostEqual(origin.y, 0.635, places=4)
    
    def test_from_xml_negative_coordinates(self):
        """Test parsing origin with negative coordinates."""
        xml_element = etree.fromstring('''
            <Origin X="-0.1012" Y="-0.564" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertAlmostEqual(origin.x, -0.1012, places=4)
        self.assertAlmostEqual(origin.y, -0.564, places=4)
    
    def test_from_xml_cross_no(self):
        """Test parsing origin with Cross="N"."""
        xml_element = etree.fromstring('''
            <Origin X="0" Y="0" Cross="N" Circle="Y" Common="Hide" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertEqual(origin.cross, Boolean.No)
        self.assertEqual(origin.circle, Boolean.Yes)
    
    def test_from_xml_circle_no(self):
        """Test parsing origin with Circle="N"."""
        xml_element = etree.fromstring('''
            <Origin X="0" Y="0" Cross="Y" Circle="N" Common="Hide" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertEqual(origin.cross, Boolean.Yes)
        self.assertEqual(origin.circle, Boolean.No)
    
    def test_from_xml_common_show(self):
        """Test parsing origin with Common="Show"."""
        xml_element = etree.fromstring('''
            <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Show" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertEqual(origin.common, "Show")
    
    def test_from_xml_common_show_if_not_center(self):
        """Test parsing origin with Common="Show if not center"."""
        xml_element = etree.fromstring('''
            <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Show if not center" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertEqual(origin.common, "Show if not center")
    
    def test_from_xml_courtyard_hide(self):
        """Test parsing origin with Courtyard="Hide"."""
        xml_element = etree.fromstring('''
            <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Hide"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertEqual(origin.courtyard, "Hide")
    
    def test_from_xml_missing_attributes(self):
        """Test parsing origin with missing optional attributes (using defaults)."""
        xml_element = etree.fromstring('''
            <Origin X="1.5" Y="2.5"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MM)
        self.assertAlmostEqual(origin.x, 1.5, places=4)
        self.assertAlmostEqual(origin.y, 2.5, places=4)
        self.assertEqual(origin.cross, Boolean.Yes)
        self.assertEqual(origin.circle, Boolean.Yes)
        self.assertEqual(origin.common, "Hide")
        self.assertEqual(origin.courtyard, "Show")
    
    def test_to_xml_mm(self):
        """Test converting Origin to XML in MM units."""
        origin = Origin(
            x=-1.27,
            y=0.635,
            cross=Boolean.Yes,
            circle=Boolean.Yes,
            common="Hide",
            courtyard="Show"
        )
        xml_element = origin.to_xml(Units.MM)
        self.assertEqual(xml_element.tag, "Origin")
        self.assertAlmostEqual(float(xml_element.get("X")), -1.27, places=3)
        self.assertAlmostEqual(float(xml_element.get("Y")), 0.635, places=3)
        self.assertEqual(xml_element.get("Cross"), "Y")
        self.assertEqual(xml_element.get("Circle"), "Y")
        self.assertEqual(xml_element.get("Common"), "Hide")
        self.assertEqual(xml_element.get("Courtyard"), "Show")
    
    def test_to_xml_inch(self):
        """Test converting Origin to XML in INCH units."""
        # Internal: 25.4 mm = 1 inch
        origin = Origin(
            x=25.4,
            y=50.8,
            cross=Boolean.No,
            circle=Boolean.No,
            common="Show",
            courtyard="Hide"
        )
        xml_element = origin.to_xml(Units.INCH)
        self.assertAlmostEqual(float(xml_element.get("X")), 1.0, places=5)
        self.assertAlmostEqual(float(xml_element.get("Y")), 2.0, places=5)
        self.assertEqual(xml_element.get("Cross"), "N")
        self.assertEqual(xml_element.get("Circle"), "N")
        self.assertEqual(xml_element.get("Common"), "Show")
        self.assertEqual(xml_element.get("Courtyard"), "Hide")
    
    def test_to_xml_mil(self):
        """Test converting Origin to XML in MIL units."""
        # Internal: 2.54 mm = 100 mils
        origin = Origin(
            x=2.54,
            y=5.08,
            cross=Boolean.Yes,
            circle=Boolean.No,
            common="Hide",
            courtyard="Show"
        )
        xml_element = origin.to_xml(Units.MIL)
        self.assertAlmostEqual(float(xml_element.get("X")), 100.0, places=3)
        self.assertAlmostEqual(float(xml_element.get("Y")), 200.0, places=3)
    
    def test_to_xml_zero_coordinates(self):
        """Test converting Origin with zero coordinates."""
        origin = Origin(x=0.0, y=0.0)
        xml_element = origin.to_xml(Units.MM)
        self.assertAlmostEqual(float(xml_element.get("X")), 0.0, places=4)
        self.assertAlmostEqual(float(xml_element.get("Y")), 0.0, places=4)
    
    def test_to_xml_negative_coordinates(self):
        """Test converting Origin with negative coordinates."""
        origin = Origin(x=-0.1012, y=-0.564)
        xml_element = origin.to_xml(Units.MM)
        self.assertAlmostEqual(float(xml_element.get("X")), -0.1012, places=4)
        self.assertAlmostEqual(float(xml_element.get("Y")), -0.564, places=4)
    
    def test_roundtrip_mm(self):
        """Test roundtrip conversion from XML to Origin and back to XML (MM units)."""
        original_xml = '''
            <Origin X="-1.7857" Y="0.0722" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
        '''
        original_element = etree.fromstring(original_xml)
        origin = Origin.from_xml(original_element, Units.MM)
        new_element = origin.to_xml(Units.MM)
        
        self.assertAlmostEqual(float(new_element.get("X")), -1.7857, places=4)
        self.assertAlmostEqual(float(new_element.get("Y")), 0.0722, places=4)
        self.assertEqual(new_element.get("Cross"), "Y")
        self.assertEqual(new_element.get("Circle"), "Y")
        self.assertEqual(new_element.get("Common"), "Hide")
        self.assertEqual(new_element.get("Courtyard"), "Show")
    
    def test_roundtrip_inch(self):
        """Test roundtrip conversion with INCH units."""
        original_xml = '''
            <Origin X="0.05" Y="-0.025" Cross="N" Circle="Y" Common="Show" Courtyard="Hide"/>
        '''
        original_element = etree.fromstring(original_xml)
        origin = Origin.from_xml(original_element, Units.INCH)
        new_element = origin.to_xml(Units.INCH)
        
        self.assertAlmostEqual(float(new_element.get("X")), 0.05, places=5)
        self.assertAlmostEqual(float(new_element.get("Y")), -0.025, places=5)
        self.assertEqual(new_element.get("Cross"), "N")
        self.assertEqual(new_element.get("Circle"), "Y")
        self.assertEqual(new_element.get("Common"), "Show")
        self.assertEqual(new_element.get("Courtyard"), "Hide")
    
    def test_roundtrip_mil(self):
        """Test roundtrip conversion with MIL units."""
        original_xml = '''
            <Origin X="50" Y="-25.5" Cross="Y" Circle="N" Common="Hide" Courtyard="Show"/>
        '''
        original_element = etree.fromstring(original_xml)
        origin = Origin.from_xml(original_element, Units.MIL)
        new_element = origin.to_xml(Units.MIL)
        
        self.assertAlmostEqual(float(new_element.get("X")), 50.0, places=3)
        self.assertAlmostEqual(float(new_element.get("Y")), -25.5, places=3)
        self.assertEqual(new_element.get("Cross"), "Y")
        self.assertEqual(new_element.get("Circle"), "N")
    
    def test_from_xml_unit_conversion_inch_to_mm(self):
        """Test that coordinates are correctly converted from INCH to internal MM."""
        xml_element = etree.fromstring('''
            <Origin X="1" Y="2" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.INCH)
        # 1 inch = 25.4 mm
        self.assertAlmostEqual(origin.x, 25.4, places=3)
        self.assertAlmostEqual(origin.y, 50.8, places=3)
    
    def test_from_xml_unit_conversion_mil_to_mm(self):
        """Test that coordinates are correctly converted from MIL to internal MM."""
        xml_element = etree.fromstring('''
            <Origin X="100" Y="200" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
        ''')
        origin = Origin.from_xml(xml_element, Units.MIL)
        # 100 mils = 2.54 mm
        self.assertAlmostEqual(origin.x, 2.54, places=3)
        self.assertAlmostEqual(origin.y, 5.08, places=3)
    
    def test_cross_circle_combinations(self):
        """Test various combinations of cross and circle settings."""
        # Both Yes - target
        origin1 = Origin(cross=Boolean.Yes, circle=Boolean.Yes)
        self.assertEqual(origin1.cross, Boolean.Yes)
        self.assertEqual(origin1.circle, Boolean.Yes)
        
        # Cross only
        origin2 = Origin(cross=Boolean.Yes, circle=Boolean.No)
        self.assertEqual(origin2.cross, Boolean.Yes)
        self.assertEqual(origin2.circle, Boolean.No)
        
        # Circle only
        origin3 = Origin(cross=Boolean.No, circle=Boolean.Yes)
        self.assertEqual(origin3.cross, Boolean.No)
        self.assertEqual(origin3.circle, Boolean.Yes)
        
        # Neither
        origin4 = Origin(cross=Boolean.No, circle=Boolean.No)
        self.assertEqual(origin4.cross, Boolean.No)
        self.assertEqual(origin4.circle, Boolean.No)
    
    def test_common_values(self):
        """Test all valid common visibility values."""
        common_values = ["Show", "Hide", "Show if not center"]
        for value in common_values:
            origin = Origin(common=value)
            self.assertEqual(origin.common, value)
            xml = origin.to_xml()
            self.assertEqual(xml.get("Common"), value)
    
    def test_courtyard_values(self):
        """Test both courtyard visibility values."""
        # Show
        origin1 = Origin(courtyard="Show")
        self.assertEqual(origin1.courtyard, "Show")
        xml1 = origin1.to_xml()
        self.assertEqual(xml1.get("Courtyard"), "Show")
        
        # Hide
        origin2 = Origin(courtyard="Hide")
        self.assertEqual(origin2.courtyard, "Hide")
        xml2 = origin2.to_xml()
        self.assertEqual(xml2.get("Courtyard"), "Hide")
    
    def test_xml_is_self_closing(self):
        """Test that Origin XML element has no children (self-closing)."""
        origin = Origin()
        xml_element = origin.to_xml()
        
        # Should have no child elements
        children = list(xml_element)
        self.assertEqual(len(children), 0)
    
    def test_precision_mm_formatting(self):
        """Test MM precision formatting (4 decimal places)."""
        origin = Origin(x=1.23456789, y=-2.34567890)
        xml_element = origin.to_xml(Units.MM)
        
        x_str = xml_element.get("X")
        y_str = xml_element.get("Y")
        
        # Should have exactly 4 decimal places
        self.assertEqual(len(x_str.split('.')[-1]), 4)
        self.assertEqual(len(y_str.split('.')[-1]), 4)
    
    def test_precision_inch_formatting(self):
        """Test INCH precision formatting (6 decimal places)."""
        origin = Origin(x=25.4, y=50.8)  # 1 and 2 inches
        xml_element = origin.to_xml(Units.INCH)
        
        x_str = xml_element.get("X")
        y_str = xml_element.get("Y")
        
        # Should have exactly 6 decimal places
        self.assertEqual(len(x_str.split('.')[-1]), 6)
        self.assertEqual(len(y_str.split('.')[-1]), 6)
    
    def test_real_world_samples(self):
        """Test with actual values from general-mm.libxml."""
        # Sample 1: Centered origin
        xml1 = etree.fromstring(
            '<Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>'
        )
        origin1 = Origin.from_xml(xml1, Units.MM)
        self.assertAlmostEqual(origin1.x, 0.0, places=4)
        self.assertAlmostEqual(origin1.y, 0.0, places=4)
        
        # Sample 2: Offset origin
        xml2 = etree.fromstring(
            '<Origin X="-0.3177" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>'
        )
        origin2 = Origin.from_xml(xml2, Units.MM)
        self.assertAlmostEqual(origin2.x, -0.3177, places=4)
        self.assertAlmostEqual(origin2.y, 0.0, places=4)
        
        # Sample 3: Both coordinates offset
        xml3 = etree.fromstring(
            '<Origin X="-0.0905" Y="0.0022" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>'
        )
        origin3 = Origin.from_xml(xml3, Units.MM)
        self.assertAlmostEqual(origin3.x, -0.0905, places=4)
        self.assertAlmostEqual(origin3.y, 0.0022, places=4)


if __name__ == '__main__':
    main()
