#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Component.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Component tests/test_Component_Component.py -v --cov-report=term --cov-report=term-missing

from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator.Component import Component, Part
from DipTraceGenerator import PartType, Units, ShapeType


class TestComponent(TestCase):
    """Test cases for Component class"""

    def test_component_default_initialization(self):
        """Test Component initializes with default values"""
        component = Component()
        self.assertEqual(component.id, 0)
        self.assertEqual(len(component.parts), 0)

    def test_component_initialization_with_id(self):
        """Test Component initialization with explicit ID"""
        component = Component(id=5)
        self.assertEqual(component.id, 5)
        self.assertEqual(len(component.parts), 0)

    def test_component_initialization_with_parts(self):
        """Test Component initialization with parts"""
        part1 = Part(id=0, name="Part 1")
        part2 = Part(id=1, name="Part 2")
        component = Component(id=10, parts=[part1, part2])
        
        self.assertEqual(component.id, 10)
        self.assertEqual(len(component.parts), 2)
        self.assertEqual(component.parts[0].name, "Part 1")
        self.assertEqual(component.parts[1].name, "Part 2")

    def test_from_xml_empty_component(self):
        """Test creating Component with no parts from XML"""
        xml_str = '<Component Id="0"/>'
        element = xml(xml_str)
        component = Component.from_xml(element)
        
        self.assertEqual(component.id, 0)
        self.assertEqual(len(component.parts), 0)

    def test_from_xml_component_with_one_part(self):
        """Test creating Component with one part from XML"""
        xml_str = '''<Component Id="5">
            <Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
                <Name>Test Component</Name>
                <PartName>Part 1</PartName>
                <Origin X="0" Y="0"/>
                <SpiceModel Type="SubCkt"/>
                <Pins/>
                <Shapes/>
                <Groups/>
            </Part>
        </Component>'''
        element = xml(xml_str)
        component = Component.from_xml(element, units=Units.MIL)
        
        self.assertEqual(component.id, 5)
        self.assertEqual(len(component.parts), 1)
        self.assertEqual(component.parts[0].id, 0)
        self.assertEqual(component.parts[0].name, "Test Component")

    def test_from_xml_component_with_multiple_parts(self):
        """Test creating Component with multiple parts from XML"""
        xml_str = '''<Component Id="10">
            <Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
                <Name>Part A</Name>
                <PartName>Part 1</PartName>
                <Origin X="0" Y="0"/>
                <SpiceModel Type="SubCkt"/>
                <Pins/>
                <Shapes/>
                <Groups/>
            </Part>
            <Part Id="1" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="150" Height="250" LockTypeChange="N" SubFolderIndex="-1">
                <Name>Part B</Name>
                <PartName>Part 2</PartName>
                <Origin X="0" Y="0"/>
                <SpiceModel Type="SubCkt"/>
                <Pins/>
                <Shapes/>
                <Groups/>
            </Part>
        </Component>'''
        element = xml(xml_str)
        component = Component.from_xml(element, units=Units.MIL)
        
        self.assertEqual(component.id, 10)
        self.assertEqual(len(component.parts), 2)
        self.assertEqual(component.parts[0].name, "Part A")
        self.assertEqual(component.parts[1].name, "Part B")

    def test_from_xml_component_with_pins(self):
        """Test creating Component with parts containing pins"""
        xml_str = '''<Component Id="0">
            <Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
                <Name>IC</Name>
                <PartName>Part 1</PartName>
                <Origin X="0" Y="0"/>
                <SpiceModel Type="SubCkt"/>
                <Pins>
                    <Pin Id="0" X="0" Y="0" Locked="N" Type="Default" ElectricType="Input" Orientation="0" PadId="1" Length="150" ShowName="Y" NumXShift="0" NumYShift="0" NameXShift="0" NameYShift="0" SignalDelay="0" NumOrientation="0" NameOrientation="0">
                        <Name>IN</Name>
                        <PadNumber>1</PadNumber>
                        <NameFont Size="5" Width="-2" Scale="1"/>
                    </Pin>
                </Pins>
                <Shapes/>
                <Groups/>
            </Part>
        </Component>'''
        element = xml(xml_str)
        component = Component.from_xml(element, units=Units.MIL)
        
        self.assertEqual(len(component.parts), 1)
        self.assertEqual(len(component.parts[0].pins), 1)
        self.assertEqual(component.parts[0].pins[0].name, "IN")

    def test_from_xml_component_with_shapes(self):
        """Test creating Component with parts containing shapes"""
        xml_str = '''<Component Id="0">
            <Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
                <Name>Symbol</Name>
                <PartName>Part 1</PartName>
                <Origin X="0" Y="0"/>
                <SpiceModel Type="SubCkt"/>
                <Pins/>
                <Shapes>
                    <Shape Id="0" Type="Rectangle" LineWidth="10" Locked="N">
                        <Points>
                            <Point X="0" Y="0"/>
                            <Point X="100" Y="100"/>
                        </Points>
                    </Shape>
                </Shapes>
                <Groups/>
            </Part>
        </Component>'''
        element = xml(xml_str)
        component = Component.from_xml(element, units=Units.MIL)
        
        self.assertEqual(len(component.parts), 1)
        self.assertEqual(len(component.parts[0].shapes), 1)
        self.assertEqual(component.parts[0].shapes[0].type, ShapeType.Rectangle)

    def test_to_xml_empty_component(self):
        """Test converting empty Component to XML"""
        component = Component(id=0)
        element = component.to_xml()
        
        self.assertEqual(element.tag, "Component")
        self.assertEqual(element.get("Id"), "0")
        self.assertEqual(len(element.findall("Part")), 0)

    def test_to_xml_component_with_one_part(self):
        """Test converting Component with one part to XML"""
        part = Part(id=0, name="Test", part_name="Part 1")
        component = Component(id=5, parts=[part])
        element = component.to_xml(units=Units.MM)
        
        self.assertEqual(element.get("Id"), "5")
        self.assertEqual(len(element.findall("Part")), 1)
        
        part_elem = element.find("Part")
        self.assertEqual(part_elem.findtext("Name"), "Test")

    def test_to_xml_component_with_multiple_parts(self):
        """Test converting Component with multiple parts to XML"""
        part1 = Part(id=0, name="Part A", part_name="Part 1")
        part2 = Part(id=1, name="Part B", part_name="Part 2")
        component = Component(id=10, parts=[part1, part2])
        element = component.to_xml(units=Units.MM)
        
        self.assertEqual(element.get("Id"), "10")
        parts = element.findall("Part")
        self.assertEqual(len(parts), 2)
        self.assertEqual(parts[0].findtext("Name"), "Part A")
        self.assertEqual(parts[1].findtext("Name"), "Part B")

    def test_round_trip_empty_component(self):
        """Test round-trip: Component -> XML -> Component (empty)"""
        original = Component(id=5)
        element = original.to_xml(units=Units.MM)
        recovered = Component.from_xml(element, units=Units.MM)
        
        self.assertEqual(recovered.id, original.id)
        self.assertEqual(len(recovered.parts), len(original.parts))

    def test_round_trip_component_with_parts(self):
        """Test round-trip: Component -> XML -> Component (with parts)"""
        part1 = Part(id=0, name="Test1", width=100.0, height=200.0)
        part2 = Part(id=1, name="Test2", width=150.0, height=250.0)
        original = Component(id=10, parts=[part1, part2])
        
        element = original.to_xml(units=Units.MM)
        recovered = Component.from_xml(element, units=Units.MM)
        
        self.assertEqual(recovered.id, original.id)
        self.assertEqual(len(recovered.parts), 2)
        self.assertEqual(recovered.parts[0].name, "Test1")
        self.assertEqual(recovered.parts[1].name, "Test2")
        self.assertAlmostEqual(recovered.parts[0].width, 100.0, places=4)
        self.assertAlmostEqual(recovered.parts[1].width, 150.0, places=4)

    def test_component_add_part(self):
        """Test adding parts to component"""
        component = Component(id=0)
        self.assertEqual(len(component.parts), 0)
        
        part = Part(id=0, name="Added Part")
        component.parts.append(part)
        
        self.assertEqual(len(component.parts), 1)
        self.assertEqual(component.parts[0].name, "Added Part")

    def test_component_multiple_parts_different_types(self):
        """Test component with parts of different types"""
        part1 = Part(id=0, part_type=PartType.Normal, name="Normal Part")
        part2 = Part(id=1, part_type=PartType.Power, name="Power Part")
        component = Component(id=0, parts=[part1, part2])
        
        self.assertEqual(component.parts[0].part_type, PartType.Normal)
        self.assertEqual(component.parts[1].part_type, PartType.Power)

    def test_unit_conversion_mm_to_mil(self):
        """Test unit conversion when creating component from XML"""
        xml_str = '''<Component Id="0">
            <Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="0" Int2="0" Width="100" Height="200" LockTypeChange="N" SubFolderIndex="-1">
                <Name>Test</Name>
                <PartName>Part 1</PartName>
                <Origin X="0" Y="0"/>
                <SpiceModel Type="SubCkt"/>
                <Pins/>
                <Shapes/>
                <Groups/>
            </Part>
        </Component>'''
        element = xml(xml_str)
        component = Component.from_xml(element, units=Units.MIL)
        
        # 100 MIL = 2.54 mm
        self.assertAlmostEqual(component.parts[0].width, 2.54, places=2)

    def test_xml_structure(self):
        """Test that Component XML has correct structure"""
        component = Component(id=5)
        element = component.to_xml()
        
        # Should have Id attribute
        self.assertIn("Id", element.attrib)
        self.assertEqual(len(element.attrib), 1)

    def test_large_component_id(self):
        """Test Component with large ID value"""
        component = Component(id=9999)
        element = component.to_xml()
        recovered = Component.from_xml(element)
        
        self.assertEqual(recovered.id, 9999)

    def test_parse_simplified_library_sample(self):
        """Test parsing a simplified structure from library.elixml"""
        xml_str = '''<Component Id="0">
            <Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" Int1="10" Int2="10" Width="700" Height="1700" LockTypeChange="Y" SubFolderIndex="1">
                <Name>AD693AD</Name>
                <PartName>Part 1</PartName>
                <Origin X="0" Y="0"/>
                <SpiceModel Type="SubCkt"/>
                <Pins/>
                <Shapes>
                    <Shape Id="0" Type="Rectangle" LineWidth="9.8425" Locked="N">
                        <Points>
                            <Point X="-350" Y="850"/>
                            <Point X="350" Y="-850"/>
                        </Points>
                    </Shape>
                </Shapes>
                <Groups/>
            </Part>
        </Component>'''
        element = xml(xml_str)
        component = Component.from_xml(element, units=Units.MIL)
        
        self.assertEqual(component.id, 0)
        self.assertEqual(len(component.parts), 1)
        self.assertEqual(component.parts[0].name, "AD693AD")
        self.assertEqual(len(component.parts[0].shapes), 1)


if __name__ == "__main__":
    main()
