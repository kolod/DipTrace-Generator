#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Pattern_Pad.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Pattern.Pad tests/test_Pattern_Pad.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml import etree
from DipTraceGenerator.Pattern import Pad
from DipTraceGenerator import Units, Boolean
from math import pi


class TestPad(TestCase):
    """Test the Pattern.Pad class."""
    
    def test_create_pad_defaults(self):
        """Test creating a Pad with default values."""
        pad = Pad()
        self.assertEqual(pad.id, 0)
        self.assertEqual(pad.style, "")
        self.assertEqual(pad.x, 0.0)
        self.assertEqual(pad.y, 0.0)
        self.assertEqual(pad.angle, 0.0)
        self.assertEqual(pad.locked, Boolean.No)
        self.assertEqual(pad.side, "Top")
        self.assertEqual(pad.number, "")
    
    def test_create_pad_with_values(self):
        """Test creating a Pad with specific values."""
        pad = Pad(
            id=5,
            style="PadT10",
            x=2.54,
            y=-1.27,
            angle=1.5708,
            locked=Boolean.Yes,
            side="Bottom",
            number="12"
        )
        self.assertEqual(pad.id, 5)
        self.assertEqual(pad.style, "PadT10")
        self.assertAlmostEqual(pad.x, 2.54, places=4)
        self.assertAlmostEqual(pad.y, -1.27, places=4)
        self.assertAlmostEqual(pad.angle, 1.5708, places=4)
        self.assertEqual(pad.locked, Boolean.Yes)
        self.assertEqual(pad.side, "Bottom")
        self.assertEqual(pad.number, "12")
    
    def test_pad_from_xml_basic(self):
        """Test parsing a basic pad from XML."""
        xml_element = etree.fromstring('''
            <Pad Id="1" Style="PadT0" X="-2.7" Y="1.905" Angle="1.5708" Locked="N" Side="Top">
                <Number>1</Number>
            </Pad>
        ''')
        pad = Pad.from_xml(xml_element, Units.MM)
        self.assertEqual(pad.id, 1)
        self.assertEqual(pad.style, "PadT0")
        self.assertAlmostEqual(pad.x, -2.7, places=4)
        self.assertAlmostEqual(pad.y, 1.905, places=4)
        self.assertAlmostEqual(pad.angle, 1.5708, places=4)
        self.assertEqual(pad.locked, Boolean.No)
        self.assertEqual(pad.side, "Top")
        self.assertEqual(pad.number, "1")
    
    def test_pad_from_xml_bottom_side(self):
        """Test parsing a bottom-side pad from XML."""
        xml_element = etree.fromstring('''
            <Pad Id="10" Style="PadB5" X="3.5" Y="-2.1" Angle="3.1416" Locked="Y" Side="Bottom">
                <Number>GND</Number>
            </Pad>
        ''')
        pad = Pad.from_xml(xml_element, Units.MM)
        self.assertEqual(pad.id, 10)
        self.assertEqual(pad.style, "PadB5")
        self.assertAlmostEqual(pad.x, 3.5, places=4)
        self.assertAlmostEqual(pad.y, -2.1, places=4)
        self.assertAlmostEqual(pad.angle, 3.1416, places=4)
        self.assertEqual(pad.locked, Boolean.Yes)
        self.assertEqual(pad.side, "Bottom")
        self.assertEqual(pad.number, "GND")
    
    def test_pad_from_xml_zero_angle(self):
        """Test parsing a pad with zero angle."""
        xml_element = etree.fromstring('''
            <Pad Id="9" Style="PadT1" X="0" Y="-0.1" Angle="0" Locked="N" Side="Top">
                <Number>9</Number>
            </Pad>
        ''')
        pad = Pad.from_xml(xml_element, Units.MM)
        self.assertEqual(pad.id, 9)
        self.assertEqual(pad.style, "PadT1")
        self.assertAlmostEqual(pad.x, 0.0, places=4)
        self.assertAlmostEqual(pad.y, -0.1, places=4)
        self.assertAlmostEqual(pad.angle, 0.0, places=4)
        self.assertEqual(pad.locked, Boolean.No)
        self.assertEqual(pad.side, "Top")
        self.assertEqual(pad.number, "9")
    
    def test_pad_from_xml_no_number(self):
        """Test parsing a pad without a number element."""
        xml_element = etree.fromstring('''
            <Pad Id="2" Style="PadT0" X="1.5" Y="0" Angle="0" Locked="N" Side="Top"/>
        ''')
        pad = Pad.from_xml(xml_element, Units.MM)
        self.assertEqual(pad.id, 2)
        self.assertEqual(pad.number, "")
    
    def test_pad_from_xml_empty_number(self):
        """Test parsing a pad with an empty number element."""
        xml_element = etree.fromstring('''
            <Pad Id="3" Style="PadT0" X="1.5" Y="0" Angle="0" Locked="N" Side="Top">
                <Number></Number>
            </Pad>
        ''')
        pad = Pad.from_xml(xml_element, Units.MM)
        self.assertEqual(pad.id, 3)
        self.assertEqual(pad.number, "")
    
    def test_pad_to_xml_mm(self):
        """Test converting a Pad to XML in MM units."""
        pad = Pad(
            id=5,
            style="PadT20",
            x=3.81,
            y=-2.54,
            angle=1.5708,
            locked=Boolean.No,
            side="Top",
            number="A1"
        )
        xml_element = pad.to_xml(Units.MM)
        self.assertEqual(xml_element.get("Id"), "5")
        self.assertEqual(xml_element.get("Style"), "PadT20")
        self.assertAlmostEqual(float(xml_element.get("X")), 3.81, places=3)
        self.assertAlmostEqual(float(xml_element.get("Y")), -2.54, places=3)
        self.assertAlmostEqual(float(xml_element.get("Angle")), 1.5708, places=3)
        self.assertEqual(xml_element.get("Locked"), "N")
        self.assertEqual(xml_element.get("Side"), "Top")
        
        number_elem = xml_element.find("Number")
        self.assertIsNotNone(number_elem)
        self.assertEqual(number_elem.text, "A1")
    
    def test_pad_to_xml_inch(self):
        """Test converting a Pad to XML in INCH units."""
        # Internal: 25.4 mm = 1 inch
        pad = Pad(
            id=1,
            style="PadT0",
            x=25.4,
            y=50.8,
            angle=0.0,
            locked=Boolean.Yes,
            side="Bottom",
            number="2"
        )
        xml_element = pad.to_xml(Units.INCH)
        self.assertAlmostEqual(float(xml_element.get("X")), 1.0, places=5)
        self.assertAlmostEqual(float(xml_element.get("Y")), 2.0, places=5)
        self.assertEqual(xml_element.get("Locked"), "Y")
        self.assertEqual(xml_element.get("Side"), "Bottom")
    
    def test_pad_to_xml_mil(self):
        """Test converting a Pad to XML in MIL units."""
        # Internal: 25.4 mm = 1000 mils
        pad = Pad(
            id=3,
            style="PadT5",
            x=2.54,
            y=5.08,
            angle=3.1416,
            locked=Boolean.No,
            side="Top",
            number="3"
        )
        xml_element = pad.to_xml(Units.MIL)
        self.assertAlmostEqual(float(xml_element.get("X")), 100.0, places=3)
        self.assertAlmostEqual(float(xml_element.get("Y")), 200.0, places=3)
        self.assertAlmostEqual(float(xml_element.get("Angle")), 3.1416, places=3)
    
    def test_pad_roundtrip_mm(self):
        """Test roundtrip conversion from XML to Pad and back to XML (MM units)."""
        original_xml = '''
            <Pad Id="7" Style="PadT12" X="4.5678" Y="-3.2109" Angle="0.7854" Locked="N" Side="Top">
                <Number>7</Number>
            </Pad>
        '''
        original_element = etree.fromstring(original_xml)
        pad = Pad.from_xml(original_element, Units.MM)
        new_element = pad.to_xml(Units.MM)
        
        self.assertEqual(new_element.get("Id"), "7")
        self.assertEqual(new_element.get("Style"), "PadT12")
        self.assertAlmostEqual(float(new_element.get("X")), 4.5678, places=4)
        self.assertAlmostEqual(float(new_element.get("Y")), -3.2109, places=4)
        self.assertAlmostEqual(float(new_element.get("Angle")), 0.7854, places=4)
        self.assertEqual(new_element.get("Locked"), "N")
        self.assertEqual(new_element.get("Side"), "Top")
        
        number_elem = new_element.find("Number")
        self.assertEqual(number_elem.text, "7")
    
    def test_pad_roundtrip_inch(self):
        """Test roundtrip conversion with INCH units."""
        original_xml = '''
            <Pad Id="2" Style="PadT3" X="0.15" Y="0.2" Angle="1.5708" Locked="Y" Side="Bottom">
                <Number>PWR</Number>
            </Pad>
        '''
        original_element = etree.fromstring(original_xml)
        pad = Pad.from_xml(original_element, Units.INCH)
        new_element = pad.to_xml(Units.INCH)
        
        self.assertEqual(new_element.get("Style"), "PadT3")
        self.assertAlmostEqual(float(new_element.get("X")), 0.15, places=5)
        self.assertAlmostEqual(float(new_element.get("Y")), 0.2, places=5)
        self.assertEqual(new_element.get("Side"), "Bottom")
        
        number_elem = new_element.find("Number")
        self.assertEqual(number_elem.text, "PWR")
    
    def test_pad_roundtrip_mil(self):
        """Test roundtrip conversion with MIL units."""
        original_xml = '''
            <Pad Id="15" Style="PadT25" X="500" Y="-250.5" Angle="2.3562" Locked="N" Side="Top">
                <Number>15</Number>
            </Pad>
        '''
        original_element = etree.fromstring(original_xml)
        pad = Pad.from_xml(original_element, Units.MIL)
        new_element = pad.to_xml(Units.MIL)
        
        self.assertEqual(new_element.get("Id"), "15")
        self.assertAlmostEqual(float(new_element.get("X")), 500.0, places=3)
        self.assertAlmostEqual(float(new_element.get("Y")), -250.5, places=3)
        self.assertAlmostEqual(float(new_element.get("Angle")), 2.3562, places=3)
    
    def test_pad_from_xml_unit_conversion_inch_to_mm(self):
        """Test that coordinates are correctly converted from INCH to internal MM."""
        xml_element = etree.fromstring('''
            <Pad Id="1" Style="PadT0" X="1" Y="2" Angle="0" Locked="N" Side="Top">
                <Number>1</Number>
            </Pad>
        ''')
        pad = Pad.from_xml(xml_element, Units.INCH)
        # 1 inch = 25.4 mm
        self.assertAlmostEqual(pad.x, 25.4, places=3)
        self.assertAlmostEqual(pad.y, 50.8, places=3)
    
    def test_pad_from_xml_unit_conversion_mil_to_mm(self):
        """Test that coordinates are correctly converted from MIL to internal MM."""
        xml_element = etree.fromstring('''
            <Pad Id="2" Style="PadT1" X="100" Y="200" Angle="0" Locked="N" Side="Top">
                <Number>2</Number>
            </Pad>
        ''')
        pad = Pad.from_xml(xml_element, Units.MIL)
        # 100 mils = 2.54 mm
        self.assertAlmostEqual(pad.x, 2.54, places=3)
        self.assertAlmostEqual(pad.y, 5.08, places=3)
    
    def test_pad_angle_values(self):
        """Test various angle values (in radians)."""
        # 0 degrees
        pad0 = Pad(angle=0.0)
        self.assertAlmostEqual(pad0.angle, 0.0, places=4)
        
        # 90 degrees = π/2 radians
        pad90 = Pad(angle=pi / 2)
        self.assertAlmostEqual(pad90.angle, 1.5708, places=4)
        
        # 180 degrees = π radians
        pad180 = Pad(angle=pi)
        self.assertAlmostEqual(pad180.angle, 3.1416, places=4)
        
        # 270 degrees = 3π/2 radians
        pad270 = Pad(angle=3 * pi / 2)
        self.assertAlmostEqual(pad270.angle, 4.7124, places=4)
    
    def test_pad_locked_values(self):
        """Test both locked values."""
        pad_unlocked = Pad(locked=Boolean.No)
        self.assertEqual(pad_unlocked.locked, Boolean.No)
        
        pad_locked = Pad(locked=Boolean.Yes)
        self.assertEqual(pad_locked.locked, Boolean.Yes)
    
    def test_pad_side_values(self):
        """Test both side values."""
        pad_top = Pad(side="Top")
        self.assertEqual(pad_top.side, "Top")
        
        pad_bottom = Pad(side="Bottom")
        self.assertEqual(pad_bottom.side, "Bottom")
    
    def test_pad_to_xml_empty_number(self):
        """Test that pads without numbers still create Number element if number is empty string."""
        pad = Pad(
            id=1,
            style="PadT0",
            x=0.0,
            y=0.0,
            angle=0.0,
            number=""
        )
        xml_element = pad.to_xml(Units.MM)
        
        # Empty number should not create a Number element
        number_elem = xml_element.find("Number")
        self.assertIsNone(number_elem)
    
    def test_pad_to_xml_with_number(self):
        """Test that pads with numbers create proper Number element."""
        pad = Pad(
            id=1,
            style="PadT0",
            x=0.0,
            y=0.0,
            angle=0.0,
            number="A5"
        )
        xml_element = pad.to_xml(Units.MM)
        
        number_elem = xml_element.find("Number")
        self.assertIsNotNone(number_elem)
        self.assertEqual(number_elem.text, "A5")


if __name__ == '__main__':
    main()
