#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Pattern_Shape.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Pattern.Shape tests/test_Pattern_Shape.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml import etree
from DipTraceGenerator.Pattern import Shape, ShapeType, Layer, TextShow
from DipTraceGenerator import Point, Units, Boolean, HorizontalAlign, VerticalAlign, TextAlign


class TestShape(TestCase):
    """Test the Pattern.Shape class."""
    
    def test_create_shape_defaults(self):
        """Test creating a Shape with default values."""
        shape = Shape()
        self.assertEqual(shape.id, 0)
        self.assertEqual(shape.type, ShapeType.Line)
        self.assertEqual(shape.locked, Boolean.No)
        self.assertEqual(shape.layer, Layer.TopSilk)
        self.assertEqual(shape.all_layers, Boolean.No)
        self.assertEqual(shape.points, [])
        self.assertIsNone(shape.width)
    
    def test_create_shape_with_values(self):
        """Test creating a Shape with specific values."""
        points = [Point(0.0, 0.0), Point(10.0, 5.0)]
        shape = Shape(
            id=5,
            type=ShapeType.Arc,
            locked=Boolean.Yes,
            layer=Layer.TopAssy,
            all_layers=Boolean.Yes,
            points=points,
            width=0.25
        )
        self.assertEqual(shape.id, 5)
        self.assertEqual(shape.type, ShapeType.Arc)
        self.assertEqual(shape.locked, Boolean.Yes)
        self.assertEqual(shape.layer, Layer.TopAssy)
        self.assertEqual(shape.all_layers, Boolean.Yes)
        self.assertEqual(len(shape.points), 2)
        self.assertEqual(shape.width, 0.25)
    
    def test_shape_from_xml_line(self):
        """Test parsing a Line shape from XML."""
        xml_element = etree.fromstring('''
            <Shape Id="1" Type="Line" Locked="N" Layer="Top Silk" AllLayers="N">
                <Points>
                    <Point X="-1.3002" Y="2.5001"/>
                    <Point X="-1.3002" Y="-2.5001"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml_element, Units.MM)
        self.assertEqual(shape.id, 1)
        self.assertEqual(shape.type, "Line")
        self.assertEqual(shape.locked, Boolean.No)
        self.assertEqual(shape.layer, "Top Silk")
        self.assertEqual(shape.all_layers, Boolean.No)
        self.assertEqual(len(shape.points), 2)
        self.assertAlmostEqual(shape.points[0].x, -1.3002, places=4)
        self.assertAlmostEqual(shape.points[0].y, 2.5001, places=4)
        self.assertAlmostEqual(shape.points[1].x, -1.3002, places=4)
        self.assertAlmostEqual(shape.points[1].y, -2.5001, places=4)
        self.assertIsNone(shape.width)
    
    def test_shape_from_xml_arc(self):
        """Test parsing an Arc shape from XML."""
        xml_element = etree.fromstring('''
            <Shape Id="6" Type="Arc" Locked="N" Layer="Top Silk" AllLayers="N">
                <Points>
                    <Point X="-0.5002" Y="2.5001"/>
                    <Point X="0" Y="2"/>
                    <Point X="0.5002" Y="2.5001"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml_element, Units.MM)
        self.assertEqual(shape.id, 6)
        self.assertEqual(shape.type, "Arc")
        self.assertEqual(len(shape.points), 3)
        self.assertAlmostEqual(shape.points[0].x, -0.5002, places=4)
        self.assertAlmostEqual(shape.points[1].x, 0, places=4)
        self.assertAlmostEqual(shape.points[1].y, 2, places=4)
        self.assertAlmostEqual(shape.points[2].x, 0.5002, places=4)
    
    def test_shape_from_xml_with_width(self):
        """Test parsing a shape with width attribute."""
        xml_element = etree.fromstring('''
            <Shape Id="10" Type="Rectangle" Locked="Y" Layer="Top Assy" AllLayers="Y" Width="0.15">
                <Points>
                    <Point X="0" Y="0"/>
                    <Point X="5" Y="3"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml_element, Units.MM)
        self.assertEqual(shape.id, 10)
        self.assertEqual(shape.type, "Rectangle")
        self.assertEqual(shape.locked, Boolean.Yes)
        self.assertEqual(shape.layer, "Top Assy")
        self.assertEqual(shape.all_layers, Boolean.Yes)
        self.assertAlmostEqual(shape.width, 0.15, places=4)
        self.assertEqual(len(shape.points), 2)
    
    def test_shape_from_xml_no_points(self):
        """Test parsing a shape without points."""
        xml_element = etree.fromstring('''
            <Shape Id="7" Type="Text" Locked="N" Layer="Top Silk" AllLayers="N"/>
        ''')
        shape = Shape.from_xml(xml_element, Units.MM)
        self.assertEqual(shape.id, 7)
        self.assertEqual(shape.type, "Text")
        self.assertEqual(shape.points, [])
    
    def test_shape_from_xml_units_conversion(self):
        """Test parsing with unit conversion (MIL to MM)."""
        xml_element = etree.fromstring('''
            <Shape Id="1" Type="Line" Locked="N" Layer="Top Silk" AllLayers="N" Width="10">
                <Points>
                    <Point X="0" Y="0"/>
                    <Point X="100" Y="100"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml_element, Units.MIL)
        # 100 mils = 2.54 mm
        self.assertAlmostEqual(shape.points[1].x, 2.54, places=2)
        self.assertAlmostEqual(shape.points[1].y, 2.54, places=2)
        # 10 mils = 0.254 mm
        self.assertAlmostEqual(shape.width, 0.254, places=3)
    
    def test_shape_to_xml_line(self):
        """Test converting a Line shape to XML."""
        shape = Shape(
            id=1,
            type=ShapeType.Line,
            locked=Boolean.No,
            layer=Layer.TopSilk,
            all_layers=Boolean.No,
            points=[Point(-1.3, 2.5), Point(-1.3, -2.5)]
        )
        xml_element = shape.to_xml(Units.MM)
        self.assertEqual(xml_element.get("Id"), "1")
        self.assertEqual(xml_element.get("Type"), "Line")
        self.assertEqual(xml_element.get("Locked"), "N")
        self.assertEqual(xml_element.get("Layer"), "Top Silk")
        self.assertEqual(xml_element.get("AllLayers"), "N")
        self.assertIsNone(xml_element.get("Width"))  # No width specified
        
        points_elem = xml_element.find("Points")
        self.assertIsNotNone(points_elem)
        point_elems = points_elem.findall("Point")
        self.assertEqual(len(point_elems), 2)
        self.assertEqual(point_elems[0].get("X"), "-1.3000")
        self.assertEqual(point_elems[0].get("Y"), "2.5000")
    
    def test_shape_to_xml_with_width(self):
        """Test converting a shape with width to XML."""
        shape = Shape(
            id=10,
            type=ShapeType.Rectangle,
            locked=Boolean.Yes,
            layer=Layer.TopAssy,
            all_layers=Boolean.Yes,
            points=[Point(0, 0), Point(5, 3)],
            width=0.15
        )
        xml_element = shape.to_xml(Units.MM)
        self.assertEqual(xml_element.get("Id"), "10")
        self.assertEqual(xml_element.get("Type"), "Rectangle")
        self.assertEqual(xml_element.get("Locked"), "Y")
        self.assertEqual(xml_element.get("Width"), "0.1500")
    
    def test_shape_to_xml_no_points(self):
        """Test converting a shape without points."""
        shape = Shape(
            id=7,
            type=ShapeType.Text,
            layer=Layer.TopSilk
        )
        xml_element = shape.to_xml(Units.MM)
        self.assertEqual(xml_element.get("Id"), "7")
        self.assertEqual(xml_element.get("Type"), "Text")
        # Should not have Points element if points list is empty
        self.assertIsNone(xml_element.find("Points"))
    
    def test_shape_to_xml_units_mil(self):
        """Test converting shape to XML with MIL units."""
        shape = Shape(
            id=1,
            type=ShapeType.Line,
            points=[Point(2.54, 5.08)],  # 100 mils, 200 mils
            width=0.254  # 10 mils
        )
        xml_element = shape.to_xml(Units.MIL)
        points_elem = xml_element.find("Points")
        point_elem = points_elem.find("Point")
        # Should be converted to mils
        self.assertEqual(point_elem.get("X"), "100.0000")
        self.assertEqual(point_elem.get("Y"), "200.0000")
        self.assertEqual(xml_element.get("Width"), "10.0000")
    
    def test_shape_to_xml_units_inch(self):
        """Test converting shape to XML with INCH units."""
        shape = Shape(
            id=1,
            type=ShapeType.Line,
            points=[Point(25.4, 50.8)],  # 1 inch, 2 inches
            width=2.54  # 0.1 inch
        )
        xml_element = shape.to_xml(Units.INCH)
        points_elem = xml_element.find("Points")
        point_elem = points_elem.find("Point")
        # Should be converted to inches with 6 decimal places
        self.assertEqual(point_elem.get("X"), "1.000000")
        self.assertEqual(point_elem.get("Y"), "2.000000")
        self.assertEqual(xml_element.get("Width"), "0.100000")
    
    def test_shape_roundtrip_mm(self):
        """Test Shape XML round-trip conversion (MM units)."""
        original = Shape(
            id=5,
            type=ShapeType.Arc,
            locked=Boolean.Yes,
            layer=Layer.BottomSilk,
            all_layers=Boolean.No,
            points=[
                Point(-0.5, 2.5),
                Point(0, 2.0),
                Point(0.5, 2.5)
            ],
            width=0.2
        )
        xml_element = original.to_xml(Units.MM)
        parsed = Shape.from_xml(xml_element, Units.MM)
        
        self.assertEqual(parsed.id, original.id)
        self.assertEqual(parsed.type, original.type)
        self.assertEqual(parsed.locked, original.locked)
        self.assertEqual(parsed.layer, original.layer)
        self.assertEqual(parsed.all_layers, original.all_layers)
        self.assertEqual(len(parsed.points), len(original.points))
        self.assertAlmostEqual(parsed.points[0].x, original.points[0].x, places=4)
        self.assertAlmostEqual(parsed.points[1].y, original.points[1].y, places=4)
        self.assertAlmostEqual(parsed.width, original.width, places=4)
    
    def test_shape_roundtrip_mil(self):
        """Test Shape XML round-trip conversion (MIL units)."""
        original = Shape(
            id=3,
            type=ShapeType.Line,
            layer=Layer.TopSilk,
            points=[Point(1.27, 2.54), Point(5.08, 7.62)]
        )
        xml_element = original.to_xml(Units.MIL)
        parsed = Shape.from_xml(xml_element, Units.MIL)
        
        self.assertEqual(parsed.id, original.id)
        self.assertEqual(parsed.type, original.type)
        self.assertEqual(len(parsed.points), 2)
        # Allow small tolerance due to unit conversion
        self.assertAlmostEqual(parsed.points[0].x, original.points[0].x, places=2)
        self.assertAlmostEqual(parsed.points[1].y, original.points[1].y, places=2)
    
    def test_shape_locked_values(self):
        """Test different locked values."""
        shape_yes = Shape(locked=Boolean.Yes)
        xml_yes = shape_yes.to_xml()
        self.assertEqual(xml_yes.get("Locked"), "Y")
        
        shape_no = Shape(locked=Boolean.No)
        xml_no = shape_no.to_xml()
        self.assertEqual(xml_no.get("Locked"), "N")
    
    def test_shape_all_layers_values(self):
        """Test different all_layers values."""
        shape_yes = Shape(all_layers=Boolean.Yes)
        xml_yes = shape_yes.to_xml()
        self.assertEqual(xml_yes.get("AllLayers"), "Y")
        
        shape_no = Shape(all_layers=Boolean.No)
        xml_no = shape_no.to_xml()
        self.assertEqual(xml_no.get("AllLayers"), "N")
    
    def test_shape_different_layers(self):
        """Test shapes on different layers."""
        layers = [Layer.TopSilk, Layer.TopAssy, Layer.BottomSilk, Layer.BottomAssy, 
                  Layer.TopMask, Layer.BottomMask, Layer.TopPaste, Layer.BottomPaste]
        for layer in layers:
            shape = Shape(layer=layer)
            xml_element = shape.to_xml()
            self.assertEqual(xml_element.get("Layer"), layer.value)
            parsed = Shape.from_xml(xml_element)
            self.assertEqual(parsed.layer, layer)
    
    def test_shape_different_types(self):
        """Test different shape types."""
        types = [ShapeType.Line, ShapeType.Arc, ShapeType.Rectangle, ShapeType.FillRect, 
                 ShapeType.Polygon, ShapeType.Text, ShapeType.Polyline]
        for shape_type in types:
            shape = Shape(type=shape_type)
            xml_element = shape.to_xml()
            self.assertEqual(xml_element.get("Type"), shape_type.value)
            parsed = Shape.from_xml(xml_element)
            self.assertEqual(parsed.type, shape_type)
    
    def test_shape_complex_polygon(self):
        """Test a complex polygon shape."""
        points = [
            Point(0, 0),
            Point(5, 0),
            Point(5, 3),
            Point(2.5, 4),
            Point(0, 3)
        ]
        shape = Shape(
            id=100,
            type=ShapeType.Polygon,
            layer=Layer.TopSilk,
            points=points,
            width=0.15
        )
        xml_element = shape.to_xml(Units.MM)
        parsed = Shape.from_xml(xml_element, Units.MM)
        
        self.assertEqual(parsed.id, 100)
        self.assertEqual(parsed.type, ShapeType.Polygon)
        self.assertEqual(len(parsed.points), 5)
        for i, point in enumerate(parsed.points):
            self.assertAlmostEqual(point.x, points[i].x, places=4)
            self.assertAlmostEqual(point.y, points[i].y, places=4)
    
    def test_text_shape_from_xml(self):
        """Test parsing a text shape from XML."""
        xml_str = '''
            <Shape Id="1" Type="Text" Locked="N" Layer="Top Silk" FontVector="Y" FontName="Tahoma" 
                   FontSize="8" FontScale="1" FontWidth="-2" TextShow="Any Text" HorzAlign="Left" 
                   VertAlign="Top" TextAlign="Left" LineSpacing="1.2" Angle="0" AllLayers="N">
                <TextLines>
                    <TextLine>Hello</TextLine>
                    <TextLine>World</TextLine>
                </TextLines>
                <Points>
                    <Point X="-13.97" Y="5.3975"/>
                </Points>
            </Shape>
        '''
        element = etree.fromstring(xml_str)
        shape = Shape.from_xml(element, Units.MM)
        
        self.assertEqual(shape.id, 1)
        self.assertEqual(shape.type, ShapeType.Text)
        self.assertEqual(shape.locked, Boolean.No)
        self.assertEqual(shape.layer, Layer.TopSilk)
        self.assertEqual(shape.font_vector, Boolean.Yes)
        self.assertEqual(shape.font_name, "Tahoma")
        self.assertEqual(shape.font_size, 8)
        self.assertEqual(shape.font_scale, 1.0)
        self.assertEqual(shape.font_width, -2.0)
        self.assertEqual(shape.text_show, TextShow.AnyText)
        self.assertEqual(shape.horz_align, HorizontalAlign.Left)
        self.assertEqual(shape.vert_align, VerticalAlign.Top)
        self.assertEqual(shape.text_align, TextAlign.Left)
        self.assertEqual(shape.line_spacing, 1.2)
        self.assertEqual(shape.angle, 0.0)
        self.assertEqual(len(shape.text_lines), 2)
        self.assertEqual(shape.text_lines[0], "Hello")
        self.assertEqual(shape.text_lines[1], "World")
        self.assertEqual(len(shape.points), 1)
        self.assertAlmostEqual(shape.points[0].x, -13.97, places=4)
        self.assertAlmostEqual(shape.points[0].y, 5.3975, places=4)
    
    def test_text_shape_to_xml(self):
        """Test converting a text shape to XML."""
        shape = Shape(
            id=5,
            type=ShapeType.Text,
            locked=Boolean.No,
            layer=Layer.TopSilk,
            font_vector=Boolean.Yes,
            font_name="Arial",
            font_size=10,
            font_scale=1.5,
            font_width=-1.0,
            text_show=TextShow.RefDes,
            horz_align=HorizontalAlign.Center,
            vert_align=VerticalAlign.Bottom,
            text_align=TextAlign.Right,
            line_spacing=1.5,
            angle=0.5,
            text_lines=["Line1", "Line2", "Line3"],
            points=[Point(1.0, 2.0)],
            group=2
        )
        xml_element = shape.to_xml(Units.MM)
        
        self.assertEqual(xml_element.get("Id"), "5")
        self.assertEqual(xml_element.get("Type"), "Text")
        self.assertEqual(xml_element.get("FontVector"), "Y")
        self.assertEqual(xml_element.get("FontName"), "Arial")
        self.assertEqual(xml_element.get("FontSize"), "10")
        self.assertEqual(xml_element.get("FontScale"), "1.5")
        self.assertEqual(xml_element.get("FontWidth"), "-1.0")
        self.assertEqual(xml_element.get("TextShow"), "RefDes")
        self.assertEqual(xml_element.get("HorzAlign"), "Center")
        self.assertEqual(xml_element.get("VertAlign"), "Bottom")
        self.assertEqual(xml_element.get("TextAlign"), "Right")
        self.assertEqual(xml_element.get("LineSpacing"), "1.5")
        self.assertEqual(xml_element.get("Angle"), "0.5")
        self.assertEqual(xml_element.get("Group"), "2")
        
        # Check text lines
        text_lines_elem = xml_element.find("TextLines")
        self.assertIsNotNone(text_lines_elem)
        lines = text_lines_elem.findall("TextLine")
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0].text, "Line1")
        self.assertEqual(lines[1].text, "Line2")
        self.assertEqual(lines[2].text, "Line3")
        
        # Check points
        points_elem = xml_element.find("Points")
        self.assertIsNotNone(points_elem)
        point_elems = points_elem.findall("Point")
        self.assertEqual(len(point_elems), 1)
    
    def test_text_shape_roundtrip(self):
        """Test text shape XML round-trip conversion."""
        original = Shape(
            id=10,
            type=ShapeType.Text,
            layer=Layer.BottomSilk,
            font_vector=Boolean.No,
            font_name="Courier New",
            font_size=12,
            text_show=TextShow.Value,
            horz_align=HorizontalAlign.Right,
            text_lines=["Test", "Data"],
            points=[Point(5.0, -3.0)]
        )
        
        xml_element = original.to_xml(Units.MM)
        parsed = Shape.from_xml(xml_element, Units.MM)
        
        self.assertEqual(parsed.id, original.id)
        self.assertEqual(parsed.type, original.type)
        self.assertEqual(parsed.layer, original.layer)
        self.assertEqual(parsed.font_vector, original.font_vector)
        self.assertEqual(parsed.font_name, original.font_name)
        self.assertEqual(parsed.font_size, original.font_size)
        self.assertEqual(parsed.text_show, original.text_show)
        self.assertEqual(parsed.horz_align, original.horz_align)
        self.assertEqual(len(parsed.text_lines), len(original.text_lines))
        for i, line in enumerate(parsed.text_lines):
            self.assertEqual(line, original.text_lines[i])
    
    def test_text_shape_with_group(self):
        """Test text shape with Group attribute from XML."""
        xml_str = '''
            <Shape Id="10" Type="Text" Locked="N" Layer="Top Silk" FontVector="Y" 
                   FontName="Arial" FontSize="10" TextShow="RefDes" HorzAlign="Center"
                   VertAlign="Top" TextAlign="Center" Group="5" AllLayers="N">
                <TextLines>
                    <TextLine>U1</TextLine>
                </TextLines>
                <Points>
                    <Point X="0" Y="0"/>
                </Points>
            </Shape>
        '''
        element = etree.fromstring(xml_str)
        shape = Shape.from_xml(element, Units.MM)
        
        # Verify group attribute is parsed correctly
        self.assertEqual(shape.group, 5)
        self.assertEqual(shape.id, 10)
        self.assertEqual(shape.type, ShapeType.Text)
        
        # Test round-trip with group
        xml_element = shape.to_xml(Units.MM)
        self.assertEqual(xml_element.get("Group"), "5")
        
        # Parse back and verify
        parsed = Shape.from_xml(xml_element, Units.MM)
        self.assertEqual(parsed.group, 5)


if __name__ == "__main__":
    main()
