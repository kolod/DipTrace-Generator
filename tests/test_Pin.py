#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Pin import Pin, PinsMixin, Shift
from DipTraceGenerator.Enums import Boolean, ElectricType, PinType


class TestPin(unittest.TestCase):
    def test_create_empty_pin(self):
        """Test creating an empty pin with default values."""
        pin = Pin()

        self.assertIsNone(pin.name)
        self.assertIsNone(pin.pad_number)
        self.assertIsNone(pin.x)
        self.assertIsNone(pin.y)
        self.assertIsNone(pin.locked)
        self.assertIsNone(pin.type)
        self.assertIsNone(pin.electric_type)
        self.assertIsNone(pin.orientation)
        self.assertIsNone(pin.pad_id)
        self.assertIsNone(pin.length)
        self.assertIsNone(pin.show_name)
        self.assertIsNone(pin.number_shift)
        self.assertIsNone(pin.name_shift)
        self.assertIsNone(pin.delay)

    def test_create_pin_from_xml(self):
        """Test creating a pin from XML with attributes."""
        pin = Pin(
            xml(
                '<Pin X="-14.1288" Y="9.8425" Locked="N" Type="Default" ElectricType="Passive" Orientation="0" '
                'PadId="1" Length="3.81" ShowName="N" SignalDelay="0" '
                'NameXShift="0" NameYShift="0" NameOrientation="0" '
                'NumXShift="0" NumYShift="0" NumOrientation="0">\n'
                "    <Name>in+</Name>\n"
                "    <PadNumber>A6</PadNumber>\n"
                '    <NameFont Size="5" Width="-2" Scale="1"/>\n'
                "</Pin>\n"
            )
        )

        self.assertEqual("in+", pin.name)
        self.assertEqual("A6", pin.pad_number)
        self.assertEqual(-14.1288, pin.x)
        self.assertEqual(9.8425, pin.y)
        self.assertEqual(Boolean.No, pin.locked)
        self.assertEqual(PinType.Default, pin.type)
        self.assertEqual(ElectricType.Passive, pin.electric_type)
        self.assertEqual(0.0, pin.orientation)
        self.assertEqual(1, pin.pad_id)
        self.assertEqual(3.81, pin.length)
        self.assertEqual(Boolean.No, pin.show_name)
        self.assertEqual(0.0, pin.number_shift.x)
        self.assertEqual(0.0, pin.number_shift.y)
        self.assertEqual(0.0, pin.number_shift.orientation)
        self.assertEqual(0.0, pin.name_shift.x)
        self.assertEqual(0.0, pin.name_shift.y)
        self.assertEqual(0.0, pin.name_shift.orientation)
        self.assertEqual(0.0, pin.delay)



    def test_create_pin_with_parameters(self):
        """Test creating a pin with explicit parameters."""
        pin = Pin(
            type=PinType.Open,
            electric_type=ElectricType.OpenHigh,
            length=2.54,
            name_shift=Shift(1.1, 2.0, 180.0),
            number_shift=Shift(1.5, -2.2),
        )

        self.assertEqual(PinType.Open, pin.type)
        self.assertEqual(ElectricType.OpenHigh, pin.electric_type)
        self.assertEqual(2.54, pin.length)
        self.assertIsNotNone(pin.name_shift)
        self.assertIsNotNone(pin.number_shift)
        self.assertEqual(1.1, pin.name_shift.x)
        self.assertEqual(2.0, pin.name_shift.y)
        self.assertEqual(180.0, pin.name_shift.orientation)
        self.assertEqual(1.5, pin.number_shift.x)
        self.assertEqual(-2.2, pin.number_shift.y)
        self.assertEqual(0.0, pin.number_shift.orientation)

    def test_pins_mixin(self):
        """Test the PinsMixin functionality."""
        class Part(PinsMixin):
            pass

        part = Part()

        self.assertIsNotNone(part.pins)
        self.assertListEqual([], part.pins)

        part.pins = [Pin(xml(
            '<Pin X="-13.4938" Y="3.175" Locked="N" Type="Dot" ElectricType="Undefined" '
            'Orientation="0" PadId="34" Length="3.81" ShowName="Y" NumXShift="0" NumYShift="0" '
            'NameXShift="0" NameYShift="0" SignalDelay="30" NumOrientation="0" NameOrientation="0">\n'
            '    <Name>2</Name>\n'
            '    <PadNumber>B5</PadNumber>\n'
            '    <NameFont Size="5" Width="-2" Scale="1"/>\n'
            '</Pin>\n'
        ))]

        self.assertIsNotNone(part.pins)
        self.assertEqual(1, len(part.pins))
        self.assertEqual(-13.4938, part.pins[0].x)
        self.assertEqual("2", part.pins[0].name)
        self.assertEqual("B5", part.pins[0].pad_number)

        part.pins = None

        self.assertIsNotNone(part.pins)
        self.assertListEqual([], part.pins)
        
    def test_pin_type_property(self):
        """Test the type property setter and getter."""
        pin = Pin(xml('<Pin Type="Default"></Pin>'))
        self.assertEqual(PinType.Default, pin.type)
        
        # Set to None
        pin.type = None
        self.assertIsNone(pin.type)

    def test_pin_pad_number_property(self):
        """Test the pad_number property setter and getter."""
        pin = Pin()
        
        # Set to a value
        pin.pad_number = "B2"
        self.assertEqual("B2", pin.pad_number)
        
        # Set to None
        pin.pad_number = None
        self.assertIsNone(pin.pad_number)
        
    def test_pin_electric_type_property(self):
        """Test the electric_type property setter and getter."""
        pin = Pin(xml('<Pin ElectricType="Passive"></Pin>'))
        self.assertEqual(ElectricType.Passive, pin.electric_type)
        
        # Set to None
        pin.electric_type = None
        self.assertIsNone(pin.electric_type)
        
    def test_pin_pad_id_property(self):
        """Test the pad_id property setter and getter."""
        pin = Pin()
        
        # Set to a value
        pin.pad_id = 42
        self.assertEqual(42, pin.pad_id)
        
        # Set to None
        pin.pad_id = None
        self.assertIsNone(pin.pad_id)
        
    def test_pin_length_property(self):
        """Test the length property setter and getter."""
        pin = Pin(xml('<Pin Length="3.81"></Pin>'))
        self.assertEqual(3.81, pin.length)
        
        # Set to None
        pin.length = None
        self.assertIsNone(pin.length)
        
    def test_pin_delay_property(self):
        """Test the delay property setter and getter."""
        pin = Pin()
        
        # Set to a value
        pin.delay = 5.0
        self.assertEqual(5.0, pin.delay)
        
        # Set to None
        pin.delay = None
        self.assertIsNone(pin.delay)
        
    def test_pin_show_name_property(self):
        """Test the show_name property setter and getter."""
        pin = Pin()
        
        # Set to a value
        pin.show_name = Boolean.Yes
        self.assertEqual(Boolean.Yes, pin.show_name)
        
        # Set to None
        pin.show_name = None
        self.assertIsNone(pin.show_name)
        
    def test_pin_number_shift_property(self):
        """Test the number_shift property setter and getter."""
        pin = Pin()
        
        # Set to a value
        pin.number_shift = Shift(1.0, 2.0, 3.0)
        self.assertEqual(1.0, pin.number_shift.x)
        self.assertEqual(2.0, pin.number_shift.y)
        self.assertEqual(3.0, pin.number_shift.orientation)
        
        # Set to None
        pin.number_shift = None
        self.assertIsNone(pin.number_shift)
        
    def test_pin_name_shift_property(self):
        """Test the name_shift property setter and getter."""
        pin = Pin()
        
        # Set to a value
        pin.name_shift = Shift(4.0, 5.0, 6.0)
        self.assertEqual(4.0, pin.name_shift.x)
        self.assertEqual(5.0, pin.name_shift.y)
        self.assertEqual(6.0, pin.name_shift.orientation)
        
        # Set to None
        pin.name_shift = None
        self.assertIsNone(pin.name_shift)
        
    def test_renumerate_pin_ids(self):
        """Test the renumerate_pin_ids method."""
        class Part(PinsMixin):
            pass
            
        part = Part()
        part.pins = [
            Pin(id=10),
            Pin(id=20),
            Pin(id=30)
        ]
        
        # Verify initial IDs
        self.assertEqual(10, part.pins[0].id)
        self.assertEqual(20, part.pins[1].id)
        self.assertEqual(30, part.pins[2].id)
        
        # Renumerate pin IDs
        part.renumerate_pin_ids()
        
        # Verify new IDs
        self.assertEqual(0, part.pins[0].id)
        self.assertEqual(1, part.pins[1].id)
        self.assertEqual(2, part.pins[2].id)


if __name__ == "__main__":
    unittest.main()
