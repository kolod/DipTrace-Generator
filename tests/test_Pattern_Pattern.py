#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Pattern_Pattern.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Pattern.Pattern tests/test_Pattern_Pattern.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml import etree
from DipTraceGenerator import Units, Boolean
from DipTraceGenerator.Pattern import Pattern, Pad, Shape, Origin, Model3D, Category, Side, ShapeType, Layer, \
    Model3DUnits, Model3DType


class TestPattern(TestCase):
    """Test the Pattern.Pattern class."""
    
    def test_create_pattern_defaults(self):
        """Test creating a Pattern with default values."""
        pattern = Pattern()
        self.assertEqual(pattern.id, 0)
        self.assertEqual(pattern.ref_des, "")
        self.assertEqual(pattern.mounting, "None")
        self.assertEqual(pattern.width, 0.0)
        self.assertEqual(pattern.height, 0.0)
        self.assertEqual(pattern.orientation, "0")
        self.assertEqual(pattern.lock_type_change, Boolean.No)
        self.assertEqual(pattern.type, "Free")
        self.assertEqual(pattern.float1, 0.0)
        self.assertEqual(pattern.float2, 0.0)
        self.assertEqual(pattern.float3, 0.0)
        self.assertEqual(pattern.int1, 0)
        self.assertEqual(pattern.int2, 0)
        self.assertEqual(pattern.name, "")
        self.assertEqual(pattern.name_unique, "")
        self.assertEqual(pattern.name_description, "")
        self.assertEqual(pattern.value, "")
        self.assertEqual(pattern.manufacturer, "")
        self.assertEqual(pattern.datasheet, "")
        self.assertIsInstance(pattern.origin, Origin)
        self.assertEqual(pattern.def_pad, "")
        self.assertEqual(pattern.pads, [])
        self.assertEqual(pattern.shapes, [])
        self.assertIsNone(pattern.model_3d)
        self.assertIsNone(pattern.category)
    
    def test_create_pattern_with_values(self):
        """Test creating a Pattern with specific values."""
        origin = Origin(x=1.0, y=2.0, cross=Boolean.Yes, circle=Boolean.Yes)
        pads = [
            Pad(id=1, style="PadT0", x=1.0, y=2.0, side=Side.Top, number="1"),
            Pad(id=2, style="PadT0", x=3.0, y=4.0, side=Side.Top, number="2"),
        ]
        shapes = [
            Shape(id=1, type=ShapeType.Line, layer=Layer.TopSilk),
            Shape(id=2, type=ShapeType.Arc, layer=Layer.TopSilk),
        ]
        
        pattern = Pattern(
            id=5,
            ref_des="U",
            mounting="SMD",
            width=10.0,
            height=8.0,
            orientation="90",
            lock_type_change=Boolean.Yes,
            type="Lines",
            float1=1.27,
            float2=5.4,
            float3=0.0,
            int1=2,
            int2=8,
            name="SOIC-8",
            name_unique="SOIC-8/150mil",
            name_description="Small Outline IC, 8 pin",
            value="IC1",
            manufacturer="Test Corp",
            datasheet="http://example.com/datasheet.pdf",
            origin=origin,
            def_pad="PadT0",
            pads=pads,
            shapes=shapes,
        )
        
        self.assertEqual(pattern.id, 5)
        self.assertEqual(pattern.ref_des, "U")
        self.assertEqual(pattern.mounting, "SMD")
        self.assertAlmostEqual(pattern.width, 10.0, places=4)
        self.assertAlmostEqual(pattern.height, 8.0, places=4)
        self.assertEqual(pattern.orientation, "90")
        self.assertEqual(pattern.lock_type_change, Boolean.Yes)
        self.assertEqual(pattern.type, "Lines")
        self.assertAlmostEqual(pattern.float1, 1.27, places=4)
        self.assertAlmostEqual(pattern.float2, 5.4, places=4)
        self.assertEqual(pattern.int1, 2)
        self.assertEqual(pattern.int2, 8)
        self.assertEqual(pattern.name, "SOIC-8")
        self.assertEqual(pattern.name_unique, "SOIC-8/150mil")
        self.assertEqual(pattern.def_pad, "PadT0")
        self.assertEqual(len(pattern.pads), 2)
        self.assertEqual(len(pattern.shapes), 2)
    
    def test_pattern_from_xml_basic(self):
        """Test parsing a basic pattern from XML."""
        xml_element = etree.fromstring('''
            <Pattern Id="0" RefDes="U" Mounting="SMD" Width="7.4" Height="5.0001" Orientation="90" LockTypeChange="Y" Type="Lines" Float1="1.27" Float2="5.4" Float3="0" Int1="2" Int2="8">
                <Name>SOIC-8/150mil</Name>
                <Name_Unique>SOIC-8/150mil</Name_Unique>
                <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
                <DefPad Style="PadT0"/>
                <Pads>
                    <Pad Id="1" Style="PadT0" X="-2.7" Y="1.905" Angle="1.5708" Locked="N" Side="Top">
                        <Number>1</Number>
                    </Pad>
                    <Pad Id="2" Style="PadT0" X="-2.7" Y="0.635" Angle="1.5708" Locked="N" Side="Top">
                        <Number>2</Number>
                    </Pad>
                </Pads>
                <Shapes>
                    <Shape Id="1" Type="Line" Locked="N" Layer="Top Silk" AllLayers="N">
                        <Points>
                            <Point X="-1.3002" Y="2.5001"/>
                            <Point X="-1.3002" Y="-2.5001"/>
                        </Points>
                    </Shape>
                </Shapes>
            </Pattern>
        ''')
        pattern = Pattern.from_xml(xml_element, Units.MM)
        
        self.assertEqual(pattern.id, 0)
        self.assertEqual(pattern.ref_des, "U")
        self.assertEqual(pattern.mounting, "SMD")
        self.assertAlmostEqual(pattern.width, 7.4, places=4)
        self.assertAlmostEqual(pattern.height, 5.0001, places=4)
        self.assertEqual(pattern.orientation, "90")
        self.assertEqual(pattern.lock_type_change, Boolean.Yes)
        self.assertEqual(pattern.type, "Lines")
        self.assertAlmostEqual(pattern.float1, 1.27, places=4)
        self.assertAlmostEqual(pattern.float2, 5.4, places=4)
        self.assertAlmostEqual(pattern.float3, 0.0, places=4)
        self.assertEqual(pattern.int1, 2)
        self.assertEqual(pattern.int2, 8)
        self.assertEqual(pattern.name, "SOIC-8/150mil")
        self.assertEqual(pattern.name_unique, "SOIC-8/150mil")
        self.assertEqual(pattern.def_pad, "PadT0")
        self.assertEqual(len(pattern.pads), 2)
        self.assertEqual(len(pattern.shapes), 1)
        self.assertEqual(pattern.pads[0].number, "1")
        self.assertEqual(pattern.pads[1].number, "2")
    
    def test_pattern_from_xml_with_optional_fields(self):
        """Test parsing a pattern with all optional fields."""
        xml_element = etree.fromstring('''
            <Pattern Id="1" RefDes="R" Mounting="SMD" Width="3.2" Height="1.6" Orientation="0" LockTypeChange="N" Type="Free" Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">
                <Name>0603</Name>
                <Name_Unique>RES-0603</Name_Unique>
                <Name_Description>Chip Resistor 0603</Name_Description>
                <Value>10K</Value>
                <Manufacturer>Yageo</Manufacturer>
                <Datasheet>http://example.com/0603.pdf</Datasheet>
                <Category Index="0">
                    <Name>Resistors</Name>
                </Category>
                <Origin X="0" Y="0" Cross="Y" Circle="N" Common="Hide" Courtyard="Show"/>
                <DefPad Style="PadT0"/>
                <Pads/>
                <Shapes/>
                <Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">
                    <Filename>
                        <Path>0603.step</Path>
                        <Var>0603.step</Var>
                    </Filename>
                    <Rotate X="0" Y="0" Z="0"/>
                    <Offset X="0" Y="0" Z="0"/>
                    <Zoom X="1" Y="1" Z="1"/>
                </Model3D>
            </Pattern>
        ''')
        pattern = Pattern.from_xml(xml_element, Units.MM)
        
        self.assertEqual(pattern.name_description, "Chip Resistor 0603")
        self.assertEqual(pattern.value, "10K")
        self.assertEqual(pattern.manufacturer, "Yageo")
        self.assertEqual(pattern.datasheet, "http://example.com/0603.pdf")
        self.assertIsNotNone(pattern.category)
        self.assertIsNotNone(pattern.model_3d)
        self.assertEqual(pattern.category.name, "Resistors")
    
    def test_pattern_to_xml_mm(self):
        """Test converting a Pattern to XML in MM units."""
        origin = Origin(x=0.0, y=0.0, cross=Boolean.Yes, circle=Boolean.Yes)
        pads = [
            Pad(id=1, style="PadT0", x=-2.7, y=1.905, angle=1.5708, side=Side.Top, number="1"),
        ]
        
        pattern = Pattern(
            id=0,
            ref_des="U",
            mounting="SMD",
            width=7.4,
            height=5.0001,
            orientation="90",
            lock_type_change=Boolean.Yes,
            type="Lines",
            float1=1.27,
            float2=5.4,
            float3=0.0,
            int1=2,
            int2=8,
            name="SOIC-8",
            origin=origin,
            def_pad="PadT0",
            pads=pads,
        )
        
        xml_element = pattern.to_xml(Units.MM)
        
        self.assertEqual(xml_element.get("Id"), "0")
        self.assertEqual(xml_element.get("RefDes"), "U")
        self.assertEqual(xml_element.get("Mounting"), "SMD")
        self.assertAlmostEqual(float(xml_element.get("Width")), 7.4, places=3)
        self.assertAlmostEqual(float(xml_element.get("Height")), 5.0001, places=3)
        self.assertEqual(xml_element.get("Orientation"), "90")
        self.assertEqual(xml_element.get("LockTypeChange"), "Y")
        self.assertEqual(xml_element.get("Type"), "Lines")
        
        name_elem = xml_element.find("Name")
        self.assertIsNotNone(name_elem)
        self.assertEqual(name_elem.text, "SOIC-8")
        
        pads_elem = xml_element.find("Pads")
        self.assertIsNotNone(pads_elem)
        self.assertEqual(len(pads_elem.findall("Pad")), 1)
    
    def test_pattern_to_xml_inch(self):
        """Test converting a Pattern to XML in INCH units."""
        # Internal: 25.4 mm = 1 inch
        pattern = Pattern(
            id=1,
            ref_des="C",
            mounting="SMD",
            width=25.4,
            height=50.8,
            orientation="0",
            lock_type_change=Boolean.No,
            type="Free",
            name="CAP-0805",
        )
        
        xml_element = pattern.to_xml(Units.INCH)
        
        self.assertAlmostEqual(float(xml_element.get("Width")), 1.0, places=5)
        self.assertAlmostEqual(float(xml_element.get("Height")), 2.0, places=5)
    
    def test_pattern_roundtrip_mm(self):
        """Test roundtrip conversion from XML to Pattern and back to XML (MM units)."""
        original_xml = '''
            <Pattern Id="0" RefDes="U" Mounting="SMD" Width="7.4" Height="5.0001" Orientation="90" LockTypeChange="Y" Type="Lines" Float1="1.27" Float2="5.4" Float3="0" Int1="2" Int2="8">
                <Name>SOIC-8/150mil</Name>
                <Name_Unique>SOIC-8/150mil</Name_Unique>
                <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
                <DefPad Style="PadT0"/>
                <Pads>
                    <Pad Id="1" Style="PadT0" X="-2.7" Y="1.905" Angle="1.5708" Locked="N" Side="Top">
                        <Number>1</Number>
                    </Pad>
                </Pads>
                <Shapes>
                    <Shape Id="1" Type="Line" Locked="N" Layer="Top Silk" AllLayers="N">
                        <Points>
                            <Point X="-1.3002" Y="2.5001"/>
                            <Point X="-1.3002" Y="-2.5001"/>
                        </Points>
                    </Shape>
                </Shapes>
            </Pattern>
        '''
        original_element = etree.fromstring(original_xml)
        pattern = Pattern.from_xml(original_element, Units.MM)
        new_element = pattern.to_xml(Units.MM)
        
        self.assertEqual(new_element.get("Id"), "0")
        self.assertEqual(new_element.get("RefDes"), "U")
        self.assertEqual(new_element.get("Mounting"), "SMD")
        self.assertAlmostEqual(float(new_element.get("Width")), 7.4, places=4)
        self.assertAlmostEqual(float(new_element.get("Height")), 5.0001, places=4)
        self.assertEqual(new_element.get("Orientation"), "90")
        self.assertEqual(new_element.get("LockTypeChange"), "Y")
        
        name_elem = new_element.find("Name")
        self.assertEqual(name_elem.text, "SOIC-8/150mil")
        
        pads_elem = new_element.find("Pads")
        self.assertEqual(len(pads_elem.findall("Pad")), 1)
        
        shapes_elem = new_element.find("Shapes")
        self.assertEqual(len(shapes_elem.findall("Shape")), 1)
    
    def test_pattern_mounting_types(self):
        """Test various mounting types."""
        for mounting in ["None", "Through", "SMD", "Chassis", "Mixed"]:
            pattern = Pattern(mounting=mounting)
            self.assertEqual(pattern.mounting, mounting)
    
    def test_pattern_orientation_values(self):
        """Test various orientation values."""
        for orientation in ["0", "90", "180", "270"]:
            pattern = Pattern(orientation=orientation)
            self.assertEqual(pattern.orientation, orientation)
    
    def test_pattern_type_values(self):
        """Test various pattern type values."""
        for type_val in ["Free", "Circle", "Lines", "Square", "Matrix", "Rectangle", "Zig-Zag", "IPC-7351"]:
            pattern = Pattern(type=type_val)
            self.assertEqual(pattern.type, type_val)
    
    def test_pattern_empty_pads_and_shapes(self):
        """Test pattern with empty pads and shapes lists."""
        pattern = Pattern(
            id=1,
            name="Empty",
            pads=[],
            shapes=[],
        )
        
        xml_element = pattern.to_xml(Units.MM)
        
        # Empty pads and shapes should not create elements
        pads_elem = xml_element.find("Pads")
        shapes_elem = xml_element.find("Shapes")
        self.assertIsNone(pads_elem)
        self.assertIsNone(shapes_elem)
    
    def test_pattern_with_model_3d(self):
        """Test pattern with 3D model."""
        model = Model3D(
            mirror=Boolean.No,
            no_search=Boolean.No,
            units=Model3DUnits.MM,
            model_type=Model3DType.File,
        )
        
        pattern = Pattern(
            id=1,
            name="With3D",
            model_3d=model,
        )
        
        self.assertIsNotNone(pattern.model_3d)
        
        xml_element = pattern.to_xml(Units.MM)
        model_elem = xml_element.find("Model3D")
        self.assertIsNotNone(model_elem)
    
    def test_pattern_with_category(self):
        """Test pattern with category."""
        category = Category(number=0, name="Test Category")
        
        pattern = Pattern(
            id=1,
            name="WithCategory",
            category=category,
        )
        
        self.assertIsNotNone(pattern.category)
        
        xml_element = pattern.to_xml(Units.MM)
        category_elem = xml_element.find("Category")
        self.assertIsNotNone(category_elem)
    
    def test_pattern_from_xml_missing_optional_elements(self):
        """Test parsing pattern with missing optional elements."""
        xml_element = etree.fromstring('''
            <Pattern Id="0" RefDes="U" Mounting="SMD" Width="7.4" Height="5" Orientation="0" LockTypeChange="N" Type="Free" Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">
                <Name>Test</Name>
                <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
            </Pattern>
        ''')
        pattern = Pattern.from_xml(xml_element, Units.MM)
        
        self.assertEqual(pattern.name_unique, "")
        self.assertEqual(pattern.name_description, "")
        self.assertEqual(pattern.value, "")
        self.assertEqual(pattern.manufacturer, "")
        self.assertEqual(pattern.datasheet, "")
        self.assertEqual(pattern.def_pad, "")
        self.assertEqual(pattern.pads, [])
        self.assertEqual(pattern.shapes, [])
        self.assertIsNone(pattern.model_3d)
        self.assertIsNone(pattern.category)
    
    def test_pattern_unit_conversion_inch_to_mm(self):
        """Test that dimensions are correctly converted from INCH to internal MM."""
        xml_element = etree.fromstring('''
            <Pattern Id="0" RefDes="U" Mounting="SMD" Width="1" Height="2" Orientation="0" LockTypeChange="N" Type="Free" Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">
                <Name>InchTest</Name>
                <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
            </Pattern>
        ''')
        pattern = Pattern.from_xml(xml_element, Units.INCH)
        
        # 1 inch = 25.4 mm, 2 inches = 50.8 mm
        self.assertAlmostEqual(pattern.width, 25.4, places=3)
        self.assertAlmostEqual(pattern.height, 50.8, places=3)
    
    def test_pattern_unit_conversion_mil_to_mm(self):
        """Test that dimensions are correctly converted from MIL to internal MM."""
        xml_element = etree.fromstring('''
            <Pattern Id="0" RefDes="U" Mounting="SMD" Width="100" Height="200" Orientation="0" LockTypeChange="N" Type="Free" Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">
                <Name>MilTest</Name>
                <Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>
            </Pattern>
        ''')
        pattern = Pattern.from_xml(xml_element, Units.MIL)
        
        # 100 mils = 2.54 mm, 200 mils = 5.08 mm
        self.assertAlmostEqual(pattern.width, 2.54, places=3)
        self.assertAlmostEqual(pattern.height, 5.08, places=3)
    
    def test_pattern_to_xml_empty_optional_strings(self):
        """Test that empty optional strings don't create XML elements."""
        pattern = Pattern(
            id=1,
            name="Required",
            name_unique="",
            name_description="",
            value="",
            manufacturer="",
            datasheet="",
            def_pad="",
        )
        
        xml_element = pattern.to_xml(Units.MM)
        
        # Name should be present
        self.assertIsNotNone(xml_element.find("Name"))
        
        # Empty fields should not create elements
        self.assertIsNone(xml_element.find("Name_Unique"))
        self.assertIsNone(xml_element.find("Name_Description"))
        self.assertIsNone(xml_element.find("Value"))
        self.assertIsNone(xml_element.find("Manufacturer"))
        self.assertIsNone(xml_element.find("Datasheet"))
        self.assertIsNone(xml_element.find("DefPad"))
    
    def test_pattern_to_xml_with_all_optional_fields(self):
        """Test that non-empty optional strings create XML elements."""
        pattern = Pattern(
            id=1,
            name="Required",
            name_unique="UNIQUE-001",
            name_description="A detailed description",
            value="TEST-VALUE",
            manufacturer="Test Manufacturer",
            datasheet="http://example.com/datasheet.pdf",
            def_pad="PadT0",
        )
        
        xml_element = pattern.to_xml(Units.MM)
        
        # All fields should be present
        self.assertIsNotNone(xml_element.find("Name"))
        self.assertIsNotNone(xml_element.find("Name_Unique"))
        self.assertIsNotNone(xml_element.find("Name_Description"))
        self.assertIsNotNone(xml_element.find("Value"))
        self.assertIsNotNone(xml_element.find("Manufacturer"))
        self.assertIsNotNone(xml_element.find("Datasheet"))
        self.assertIsNotNone(xml_element.find("DefPad"))
        
        # Check content
        self.assertEqual(xml_element.find("Name_Unique").text, "UNIQUE-001")
        self.assertEqual(xml_element.find("Name_Description").text, "A detailed description")
        self.assertEqual(xml_element.find("Value").text, "TEST-VALUE")
        self.assertEqual(xml_element.find("Manufacturer").text, "Test Manufacturer")
        self.assertEqual(xml_element.find("Datasheet").text, "http://example.com/datasheet.pdf")
        self.assertEqual(xml_element.find("DefPad").get("Style"), "PadT0")


if __name__ == '__main__':
    main()
