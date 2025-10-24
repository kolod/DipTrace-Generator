#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Part.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Part tests/test_Component_Part.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator.Component.Part import Part
from DipTraceGenerator.Component.Group import Group
from DipTraceGenerator.Component.Pin import Pin,  ElectricType
from DipTraceGenerator.Component.Shape import Shape, ShapeType
from DipTraceGenerator.Enums import PartType, ShowNumbers, ComponentType, Boolean
from DipTraceGenerator import Units


class TestComponentPart(TestCase):
    """Test cases for Component Part class"""

    def test_part_default_initialization(self):
        """Test Part initializes with default values"""
        part = Part()
        self.assertEqual(part.id, 0)
        self.assertEqual(part.part_type, PartType.Normal)
        self.assertEqual(part.show_numbers, ShowNumbers.Hide)
        self.assertEqual(part.type, ComponentType.Free)
        self.assertEqual(part.int1, 0)
        self.assertEqual(part.int2, 0)
        self.assertEqual(part.width, 0.0)
        self.assertEqual(part.height, 0.0)
        self.assertEqual(part.lock_type_change, Boolean.No)
        self.assertEqual(part.sub_folder_index, -1)
        self.assertEqual(part.name, "Untitled")
        self.assertEqual(part.part_name, "Part 1")
        self.assertEqual(len(part.pins), 0)
        self.assertEqual(len(part.shapes), 0)
        self.assertEqual(len(part.groups), 0)

    def test_part_initialization_with_values(self):
        """Test Part initialization with explicit values"""
        part = Part(
            id=5,
            part_type=PartType.Power,
            show_numbers=ShowNumbers.Show,
            type=ComponentType.Fixed,
            int1=1,
            int2=2,
            width=100.0,
            height=200.0,
            lock_type_change=Boolean.Yes,
            sub_folder_index=3,
            name="Test Component",
            part_name="Test Part"
        )
        
        self.assertEqual(part.id, 5)
        self.assertEqual(part.part_type, PartType.Power)
        self.assertEqual(part.show_numbers, ShowNumbers.Show)
        self.assertEqual(part.type, ComponentType.Fixed)
        self.assertEqual(part.int1, 1)
        self.assertEqual(part.int2, 2)
        self.assertEqual(part.width, 100.0)
        self.assertEqual(part.height, 200.0)
        self.assertEqual(part.lock_type_change, Boolean.Yes)
        self.assertEqual(part.sub_folder_index, 3)
        self.assertEqual(part.name, "Test Component")
        self.assertEqual(part.part_name, "Test Part")

    def test_from_xml_simple_part(self):
        """Test creating simple Part from XML"""
        xml_str = '''<Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="2755.9056" Height="3740.1574" LockTypeChange="N" SubFolderIndex="-1">
            <Name>Untitled</Name>
            <PartName>Part 1</PartName>
            <Origin X="-590.5512" Y="-492.126"/>
            <SpiceModel Type="SubCkt"/>
            <Pins/>
            <Shapes/>
            <Groups/>
        </Part>'''
        element = xml(xml_str)
        part = Part.from_xml(element, units=Units.MIL)
        
        self.assertEqual(part.id, 0)
        self.assertEqual(part.part_type, PartType.Normal)
        self.assertEqual(part.show_numbers, ShowNumbers.Hide)
        self.assertEqual(part.type, ComponentType.Free)
        self.assertEqual(part.name, "Untitled")
        self.assertEqual(part.part_name, "Part 1")
        self.assertAlmostEqual(part.width, 70.0, places=1)
        self.assertAlmostEqual(part.height, 95.0, places=1)

    def test_from_xml_part_with_pins(self):
        """Test creating Part with pins from XML"""
        xml_str = '''<Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
            <Name>Test</Name>
            <PartName>Part 1</PartName>
            <Origin X="0" Y="0"/>
            <SpiceModel Type="SubCkt"/>
            <Pins>
                <Pin Id="0" X="0" Y="0" Locked="N" Type="Default" ElectricType="Input" Orientation="0" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
                    <Name>1</Name>
                    <PadNumber>1</PadNumber>
                    <NameFont Size="5" Width="-2" Scale="1"/>
                </Pin>
            </Pins>
            <Shapes/>
            <Groups/>
        </Part>'''
        element = xml(xml_str)
        part = Part.from_xml(element, units=Units.MIL)
        
        self.assertEqual(len(part.pins), 1)
        self.assertEqual(part.pins[0].id, 0)
        self.assertEqual(part.pins[0].electric_type, ElectricType.Input)

    def test_from_xml_part_with_shapes(self):
        """Test creating Part with shapes from XML"""
        xml_str = '''<Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
            <Name>Test</Name>
            <PartName>Part 1</PartName>
            <Origin X="0" Y="0"/>
            <SpiceModel Type="SubCkt"/>
            <Pins/>
            <Shapes>
                <Shape Id="0" Type="Line" LineWidth="10" Locked="N" Group="0">
                    <Points>
                        <Point X="0" Y="0"/>
                        <Point X="100" Y="100"/>
                    </Points>
                </Shape>
            </Shapes>
            <Groups/>
        </Part>'''
        element = xml(xml_str)
        part = Part.from_xml(element, units=Units.MIL)
        
        self.assertEqual(len(part.shapes), 1)
        self.assertEqual(part.shapes[0].id, 0)
        self.assertEqual(part.shapes[0].type, ShapeType.Line)

    def test_from_xml_part_with_groups(self):
        """Test creating Part with groups from XML"""
        xml_str = '''<Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
            <Name>Test</Name>
            <PartName>Part 1</PartName>
            <Origin X="0" Y="0"/>
            <SpiceModel Type="SubCkt"/>
            <Pins/>
            <Shapes/>
            <Groups>
                <Group Id="0" X="10" Y="20"/>
                <Group Id="1" X="30" Y="40"/>
            </Groups>
        </Part>'''
        element = xml(xml_str)
        part = Part.from_xml(element, units=Units.MIL)
        
        self.assertEqual(len(part.groups), 2)
        self.assertEqual(part.groups[0].id, 0)
        self.assertEqual(part.groups[1].id, 1)

    def test_to_xml_simple_part(self):
        """Test converting simple Part to XML"""
        part = Part(
            id=0,
            name="Test Component",
            part_name="Test Part",
            width=70.0,
            height=95.0
        )
        element = part.to_xml(units=Units.MM)
        
        self.assertEqual(element.tag, "Part")
        self.assertEqual(element.get("Id"), "0")
        self.assertEqual(element.get("PartType"), "Normal")
        self.assertEqual(element.findtext("Name"), "Test Component")
        self.assertEqual(element.findtext("PartName"), "Test Part")

    def test_to_xml_part_with_pins(self):
        """Test converting Part with pins to XML"""
        pin = Pin(id=0, name="1", pad_number="1")
        part = Part(id=0, pins=[pin])
        element = part.to_xml(units=Units.MM)
        
        pins_elem = element.find("Pins")
        self.assertIsNotNone(pins_elem)
        self.assertEqual(len(pins_elem.findall("Pin")), 1)

    def test_to_xml_part_with_shapes(self):
        """Test converting Part with shapes to XML"""
        shape = Shape(id=0, type=ShapeType.Line)
        part = Part(id=0, shapes=[shape])
        element = part.to_xml(units=Units.MM)
        
        shapes_elem = element.find("Shapes")
        self.assertIsNotNone(shapes_elem)
        self.assertEqual(len(shapes_elem.findall("Shape")), 1)

    def test_to_xml_part_with_groups(self):
        """Test converting Part with groups to XML"""
        group1 = Group(id=0, x=10.0, y=20.0)
        group2 = Group(id=1, x=30.0, y=40.0)
        part = Part(id=0, groups=[group1, group2])
        element = part.to_xml(units=Units.MM)
        
        groups_elem = element.find("Groups")
        self.assertIsNotNone(groups_elem)
        self.assertEqual(len(groups_elem.findall("Group")), 2)

    def test_round_trip_simple_part(self):
        """Test round-trip: Part -> XML -> Part"""
        original = Part(
            id=5,
            part_type=PartType.Normal,
            show_numbers=ShowNumbers.Hide,
            type=ComponentType.Free,
            width=100.0,
            height=200.0,
            name="Test",
            part_name="Part Test"
        )
        element = original.to_xml(units=Units.MM)
        recovered = Part.from_xml(element, units=Units.MM)
        
        self.assertEqual(recovered.id, original.id)
        self.assertEqual(recovered.part_type, original.part_type)
        self.assertEqual(recovered.show_numbers, original.show_numbers)
        self.assertEqual(recovered.type, original.type)
        self.assertAlmostEqual(recovered.width, original.width, places=4)
        self.assertAlmostEqual(recovered.height, original.height, places=4)
        self.assertEqual(recovered.name, original.name)
        self.assertEqual(recovered.part_name, original.part_name)

    def test_all_part_types(self):
        """Test all part types can be created"""
        for part_type in PartType:
            part = Part(part_type=part_type)
            element = part.to_xml()
            recovered = Part.from_xml(element)
            self.assertEqual(recovered.part_type, part_type)

    def test_all_show_numbers_options(self):
        """Test all show numbers options can be created"""
        for show_opt in ShowNumbers:
            part = Part(show_numbers=show_opt)
            element = part.to_xml()
            recovered = Part.from_xml(element)
            self.assertEqual(recovered.show_numbers, show_opt)

    def test_all_component_types(self):
        """Test all component types can be created"""
        for comp_type in ComponentType:
            part = Part(type=comp_type)
            element = part.to_xml()
            recovered = Part.from_xml(element)
            self.assertEqual(recovered.type, comp_type)

    def test_unit_conversion_width_height(self):
        """Test unit conversion for width and height"""
        part = Part(width=25.4, height=50.8)  # in mm
        element = part.to_xml(units=Units.INCH)
        
        width_val = float(element.get("Width"))
        height_val = float(element.get("Height"))
        
        # 25.4 mm = 1 inch, 50.8 mm = 2 inch
        self.assertAlmostEqual(width_val, 1.0, places=4)
        self.assertAlmostEqual(height_val, 2.0, places=4)

    def test_exact_formatting_mm(self):
        """Test MM units use exactly 4 decimal places"""
        part = Part(width=10.0, height=20.0)
        element = part.to_xml(units=Units.MM)
        
        width_str = element.get("Width")
        height_str = element.get("Height")
        
        self.assertEqual(len(width_str.split('.')[1]), 4)
        self.assertEqual(len(height_str.split('.')[1]), 4)

    def test_exact_formatting_inch(self):
        """Test INCH units use exactly 6 decimal places"""
        part = Part(width=25.4, height=50.8)
        element = part.to_xml(units=Units.INCH)
        
        width_str = element.get("Width")
        height_str = element.get("Height")
        
        self.assertEqual(len(width_str.split('.')[1]), 6)
        self.assertEqual(len(height_str.split('.')[1]), 6)

    def test_parse_shapes_elixml_sample(self):
        """Test parsing the actual shapes.elixml sample"""
        xml_str = '''<Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="2755.9056" Height="3740.1574" LockTypeChange="N" SubFolderIndex="-1">
            <Name>Untitled</Name>
            <PartName>Part 1</PartName>
            <Origin X="-590.5512" Y="-492.126"/>
            <SpiceModel Type="SubCkt"/>
            <Pins/>
            <Shapes>
                <Shape Id="0" Type="Line" LineWidth="9.8425" Locked="N" Group="0">
                    <Points>
                        <Point X="-787.4016" Y="-98.4252"/>
                        <Point X="-393.7008" Y="-98.4252"/>
                    </Points>
                </Shape>
            </Shapes>
            <Groups>
                <Group Id="0" X="-590.5512" Y="-295.2756"/>
            </Groups>
        </Part>'''
        element = xml(xml_str)
        part = Part.from_xml(element, units=Units.MIL)
        
        self.assertEqual(part.id, 0)
        self.assertEqual(part.name, "Untitled")
        self.assertEqual(len(part.shapes), 1)
        self.assertEqual(len(part.groups), 1)
        self.assertAlmostEqual(part.origin.x, -15.0, places=1)


if __name__ == "__main__":
    main()
