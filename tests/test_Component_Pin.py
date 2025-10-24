#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Pin.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Pin tests/test_Component_Pin.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator.Component.Pin import Pin, PinType, ElectricType, Boolean, NameFont
from DipTraceGenerator import Units


class TestNameFont(TestCase):
    """Test cases for NameFont class"""

    def test_namefont_default_initialization(self):
        """Test NameFont initializes with default values"""
        font = NameFont()
        self.assertEqual(font.size, 5)
        self.assertEqual(font.width, -2)
        self.assertEqual(font.scale, 1.0)

    def test_namefont_initialization_with_values(self):
        """Test NameFont initialization with explicit values"""
        font = NameFont(size=10, width=-3, scale=1.5)
        self.assertEqual(font.size, 10)
        self.assertEqual(font.width, -3)
        self.assertEqual(font.scale, 1.5)

    def test_namefont_from_xml(self):
        """Test creating NameFont from XML"""
        xml_str = '<NameFont Size="12" Width="-4" Scale="2.0"/>'
        element = xml(xml_str)
        font = NameFont.from_xml(element)
        
        self.assertEqual(font.size, 12)
        self.assertEqual(font.width, -4)
        self.assertEqual(font.scale, 2.0)

    def test_namefont_to_xml(self):
        """Test converting NameFont to XML"""
        font = NameFont(size=8, width=-1, scale=1.2)
        element = font.to_xml()
        
        self.assertEqual(element.tag, "NameFont")
        self.assertEqual(element.get("Size"), "8")
        self.assertEqual(element.get("Width"), "-1")
        self.assertEqual(element.get("Scale"), "1.2")


class TestComponentPin(TestCase):
    """Test cases for Component Pin class"""

    def test_pin_default_initialization(self):
        """Test Pin initializes with default values"""
        pin = Pin()
        self.assertEqual(pin.id, 0)
        self.assertEqual(pin.x, 0.0)
        self.assertEqual(pin.y, 0.0)
        self.assertEqual(pin.locked, Boolean.No)
        self.assertEqual(pin.type, PinType.Default)
        self.assertEqual(pin.electric_type, ElectricType.Undefined)
        self.assertEqual(pin.orientation, 0)
        self.assertEqual(pin.pad_id, 0)
        self.assertEqual(pin.length, 150.0)
        self.assertEqual(pin.show_name, Boolean.Yes)

    def test_pin_initialization_with_values(self):
        """Test Pin initialization with explicit values"""
        pin = Pin(
            id=5,
            x=10.0,
            y=20.0,
            locked=Boolean.Yes,
            type=PinType.Dot,
            electric_type=ElectricType.Input,
            orientation=90,
            pad_id=3,
            length=200.0,
            show_name=Boolean.No
        )
        self.assertEqual(pin.id, 5)
        self.assertEqual(pin.x, 10.0)
        self.assertEqual(pin.y, 20.0)
        self.assertEqual(pin.locked, Boolean.Yes)
        self.assertEqual(pin.type, PinType.Dot)
        self.assertEqual(pin.electric_type, ElectricType.Input)
        self.assertEqual(pin.orientation, 90)
        self.assertEqual(pin.pad_id, 3)
        self.assertEqual(pin.length, 200.0)
        self.assertEqual(pin.show_name, Boolean.No)

    def test_from_xml_default_pin(self):
        """Test creating Default pin from XML"""
        xml_str = '''<Pin Id="0" X="-977.2727" Y="2150" Locked="N" Type="Default" ElectricType="Undefined" Orientation="0" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
            <Name>1</Name>
            <PadNumber>1</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(pin.id, 0)
        self.assertEqual(pin.locked, Boolean.No)
        self.assertEqual(pin.type, PinType.Default)
        self.assertEqual(pin.electric_type, ElectricType.Undefined)
        self.assertEqual(pin.orientation, 0)
        self.assertEqual(pin.pad_id, 1)
        self.assertEqual(pin.show_name, Boolean.Yes)
        self.assertEqual(pin.signal_delay, 0.0)
        self.assertEqual(pin.num_orientation, 0)
        self.assertEqual(pin.name_orientation, 0)
        self.assertEqual(pin.name, "1")
        self.assertEqual(pin.pad_number, "1")
        self.assertEqual(pin.name_font.size, 5)

    def test_from_xml_dot_passive_pin(self):
        """Test creating Dot Passive pin from XML"""
        xml_str = '''<Pin Id="1" X="-931.8182" Y="2050" Locked="N" Type="Dot" ElectricType="Passive" Orientation="0" PadId="2" Length="150" ShowName="N" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0.762" NumOrientation="0" NameOrientation="0">
            <Name>2</Name>
            <PadNumber>2</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(pin.id, 1)
        self.assertEqual(pin.type, PinType.Dot)
        self.assertEqual(pin.electric_type, ElectricType.Passive)
        self.assertEqual(pin.show_name, Boolean.No)
        self.assertAlmostEqual(pin.signal_delay, 0.762, places=3)
        self.assertEqual(pin.name, "2")
        self.assertEqual(pin.pad_number, "2")

    def test_from_xml_polarity_in_input_pin(self):
        """Test creating Polarity In Input pin from XML"""
        xml_str = '''<Pin Id="2" X="-886.3636" Y="1950" Locked="N" Type="Polarity In" ElectricType="Input" Orientation="0" PadId="3" Length="150" ShowName="N" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
            <Name>3</Name>
            <PadNumber>3</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(pin.id, 2)
        self.assertEqual(pin.type, PinType.PolarityIn)
        self.assertEqual(pin.electric_type, ElectricType.Input)

    def test_from_xml_polarity_out_output_pin(self):
        """Test creating Polarity Out Output pin from XML"""
        xml_str = '''<Pin Id="3" X="-840.9091" Y="1850" Locked="N" Type="Polarity Out" ElectricType="Output" Orientation="0" PadId="4" Length="150" ShowName="N" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
            <Name>4</Name>
            <PadNumber>4</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(pin.id, 3)
        self.assertEqual(pin.type, PinType.PolarityOut)
        self.assertEqual(pin.electric_type, ElectricType.Output)

    def test_from_xml_non_logic_bidirectional_pin(self):
        """Test creating Non Logic Bidirectional pin from XML"""
        xml_str = '''<Pin Id="4" X="-795.4545" Y="1750" Locked="N" Type="Non Logic" ElectricType="Bidirectional" Orientation="0" PadId="5" Length="150" ShowName="N" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0.0076" NumOrientation="0" NameOrientation="0">
            <Name>5</Name>
            <PadNumber>5</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(pin.type, PinType.NonLogic)
        self.assertEqual(pin.electric_type, ElectricType.Bidirectional)
        self.assertAlmostEqual(pin.signal_delay, 0.0076, places=4)

    def test_from_xml_open_high_pin(self):
        """Test creating Open High pin from XML"""
        xml_str = '''<Pin Id="5" X="-750" Y="1650" Locked="N" Type="Open" ElectricType="Open High" Orientation="0" PadId="6" Length="150" ShowName="N" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
            <Name>6</Name>
            <PadNumber>6</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(pin.type, PinType.Open)
        self.assertEqual(pin.electric_type, ElectricType.OpenHigh)

    def test_from_xml_all_pin_types(self):
        """Test all pin types can be parsed"""
        pin_types = [
            ("Default", PinType.Default),
            ("Dot", PinType.Dot),
            ("Polarity In", PinType.PolarityIn),
            ("Polarity Out", PinType.PolarityOut),
            ("Non Logic", PinType.NonLogic),
            ("Open", PinType.Open),
            ("Open Low", PinType.OpenLow),
            ("3 State", PinType.ThreeState),
            ("Hysteresis", PinType.Hysteresis),
            ("Amplifier", PinType.Amplifier),
            ("Postponed", PinType.Postponed),
            ("Shift", PinType.Shift),
            ("Clock", PinType.Clock),
            ("Generator", PinType.Generator)
        ]
        
        for type_str, type_enum in pin_types:
            xml_str = f'''<Pin Id="0" X="0" Y="0" Locked="N" Type="{type_str}" ElectricType="Undefined" Orientation="0" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
                <Name>Test</Name>
                <PadNumber>1</PadNumber>
                <NameFont Size="5" Width="-2" Scale="1"/>
            </Pin>'''
            element = xml(xml_str)
            pin = Pin.from_xml(element, units=Units.MIL)
            self.assertEqual(pin.type, type_enum)

    def test_from_xml_all_electric_types(self):
        """Test all electric types can be parsed"""
        electric_types = [
            ("Undefined", ElectricType.Undefined),
            ("Passive", ElectricType.Passive),
            ("Input", ElectricType.Input),
            ("Output", ElectricType.Output),
            ("Bidirectional", ElectricType.Bidirectional),
            ("Open High", ElectricType.OpenHigh),
            ("Open Low", ElectricType.OpenLow),
            ("Passive High", ElectricType.PassiveHigh),
            ("Passive Low", ElectricType.PassiveLow),
            ("3 State", ElectricType.ThreeState),
            ("Power", ElectricType.Power)
        ]
        
        for type_str, type_enum in electric_types:
            xml_str = f'''<Pin Id="0" X="0" Y="0" Locked="N" Type="Default" ElectricType="{type_str}" Orientation="0" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
                <Name>Test</Name>
                <PadNumber>1</PadNumber>
                <NameFont Size="5" Width="-2" Scale="1"/>
            </Pin>'''
            element = xml(xml_str)
            pin = Pin.from_xml(element, units=Units.MIL)
            self.assertEqual(pin.electric_type, type_enum)

    def test_from_xml_locked_yes(self):
        """Test pin with locked=Yes"""
        xml_str = '''<Pin Id="0" X="0" Y="0" Locked="Y" Type="Default" ElectricType="Undefined" Orientation="0" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
            <Name>Test</Name>
            <PadNumber>1</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(pin.locked, Boolean.Yes)

    def test_from_xml_different_orientations(self):
        """Test pins with different orientations"""
        for orientation in [0, 90, 180, 270]:
            xml_str = f'''<Pin Id="0" X="0" Y="0" Locked="N" Type="Default" ElectricType="Undefined" Orientation="{orientation}" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
                <Name>Test</Name>
                <PadNumber>1</PadNumber>
                <NameFont Size="5" Width="-2" Scale="1"/>
            </Pin>'''
            element = xml(xml_str)
            pin = Pin.from_xml(element, units=Units.MIL)
            self.assertEqual(pin.orientation, orientation)

    def test_to_xml_default_pin(self):
        """Test converting Default pin to XML"""
        pin = Pin(
            id=0,
            x=-24.825,  # in mm
            y=54.61,    # in mm
            locked=Boolean.No,
            type=PinType.Default,
            electric_type=ElectricType.Undefined,
            orientation=0,
            pad_id=1,
            length=3.81,  # in mm
            show_name=Boolean.Yes,
            name="1",
            pad_number="1"
        )
        element = pin.to_xml(units=Units.MIL)
        
        self.assertEqual(element.tag, "Pin")
        self.assertEqual(element.get("Id"), "0")
        self.assertEqual(element.get("Locked"), "N")
        self.assertEqual(element.get("Type"), "Default")
        self.assertEqual(element.get("ElectricType"), "Undefined")
        self.assertEqual(element.get("Orientation"), "0")
        self.assertEqual(element.get("PadId"), "1")
        self.assertEqual(element.get("ShowName"), "Y")
        
        # Check name and pad number
        name_elem = element.find("Name")
        self.assertIsNotNone(name_elem)
        self.assertEqual(name_elem.text, "1")
        
        pad_num_elem = element.find("PadNumber")
        self.assertIsNotNone(pad_num_elem)
        self.assertEqual(pad_num_elem.text, "1")
        
        # Check name font
        font_elem = element.find("NameFont")
        self.assertIsNotNone(font_elem)

    def test_to_xml_dot_pin(self):
        """Test converting Dot pin to XML"""
        pin = Pin(
            id=1,
            type=PinType.Dot,
            electric_type=ElectricType.Passive,
            signal_delay=0.762,
            show_name=Boolean.No,
            name="2",
            pad_number="2"
        )
        element = pin.to_xml(units=Units.MIL)
        
        self.assertEqual(element.get("Type"), "Dot")
        self.assertEqual(element.get("ElectricType"), "Passive")
        self.assertEqual(element.get("SignalDelay"), "0.762")
        self.assertEqual(element.get("ShowName"), "N")

    def test_to_xml_custom_name_font(self):
        """Test pin with custom name font"""
        custom_font = NameFont(size=10, width=-3, scale=1.5)
        pin = Pin(
            id=0,
            name="Test",
            pad_number="1",
            name_font=custom_font
        )
        element = pin.to_xml()
        
        font_elem = element.find("NameFont")
        self.assertEqual(font_elem.get("Size"), "10")
        self.assertEqual(font_elem.get("Width"), "-3")
        self.assertEqual(font_elem.get("Scale"), "1.5")

    def test_to_xml_empty_name(self):
        """Test pin with empty name"""
        pin = Pin(id=0, name="", pad_number="")
        element = pin.to_xml()
        
        # Empty names should not create elements
        name_elem = element.find("Name")
        self.assertIsNone(name_elem)
        
        pad_num_elem = element.find("PadNumber")
        self.assertIsNone(pad_num_elem)

    def test_round_trip_default_pin(self):
        """Test round-trip: Pin -> XML -> Pin"""
        original = Pin(
            id=5,
            x=10.0,
            y=20.0,
            locked=Boolean.No,
            type=PinType.Clock,
            electric_type=ElectricType.Input,
            orientation=90,
            pad_id=3,
            length=5.0,
            show_name=Boolean.Yes,
            signal_delay=1.5,
            name="CLK",
            pad_number="5"
        )
        element = original.to_xml(units=Units.MIL)
        recovered = Pin.from_xml(element, units=Units.MIL)
        
        self.assertEqual(recovered.id, original.id)
        self.assertEqual(recovered.type, original.type)
        self.assertEqual(recovered.electric_type, original.electric_type)
        self.assertEqual(recovered.orientation, original.orientation)
        self.assertEqual(recovered.pad_id, original.pad_id)
        self.assertEqual(recovered.show_name, original.show_name)
        self.assertAlmostEqual(recovered.signal_delay, original.signal_delay, places=4)
        self.assertEqual(recovered.name, original.name)
        self.assertEqual(recovered.pad_number, original.pad_number)

    def test_unit_conversion_mm_to_mil(self):
        """Test unit conversion from MM to MIL"""
        pin = Pin(
            id=0,
            x=2.54,     # 100 mil
            y=5.08,     # 200 mil
            length=3.81  # 150 mil
        )
        element = pin.to_xml(units=Units.MIL)
        
        x_val = float(element.get("X"))
        y_val = float(element.get("Y"))
        length_val = float(element.get("Length"))
        
        self.assertAlmostEqual(x_val, 100.0, places=2)
        self.assertAlmostEqual(y_val, 200.0, places=2)
        self.assertAlmostEqual(length_val, 150.0, places=2)

    def test_unit_conversion_mil_to_mm(self):
        """Test unit conversion from MIL to MM"""
        xml_str = '''<Pin Id="0" X="100" Y="200" Locked="N" Type="Default" ElectricType="Undefined" Orientation="0" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
            <Name>1</Name>
            <PadNumber>1</PadNumber>
            <NameFont Size="5" Width="-2" Scale="1"/>
        </Pin>'''
        element = xml(xml_str)
        pin = Pin.from_xml(element, units=Units.MIL)
        
        # 100 mil = 2.54 mm, 200 mil = 5.08 mm, 150 mil = 3.81 mm
        self.assertAlmostEqual(pin.x, 2.54, places=2)
        self.assertAlmostEqual(pin.y, 5.08, places=2)
        self.assertAlmostEqual(pin.length, 3.81, places=2)


if __name__ == "__main__":
    main()
