"""Tests for Pattern Shape class."""

import pytest
from lxml import etree

from DipTraceGenerator.Pattern.Shape import Shape
from DipTraceGenerator.Point import Point
from DipTraceGenerator.Units import Units
from DipTraceGenerator.Enums import Boolean


class TestShape:
    """Test the Pattern.Shape class."""
    
    def test_create_shape_defaults(self):
        """Test creating a Shape with default values."""
        shape = Shape()
        assert shape.id == 0
        assert shape.type == "Line"
        assert shape.locked == Boolean.No
        assert shape.layer == "Top Silk"
        assert shape.all_layers == Boolean.No
        assert shape.points == []
        assert shape.width is None
    
    def test_create_shape_with_values(self):
        """Test creating a Shape with specific values."""
        points = [Point(0.0, 0.0), Point(10.0, 5.0)]
        shape = Shape(
            id=5,
            type="Arc",
            locked=Boolean.Yes,
            layer="Top Assy",
            all_layers=Boolean.Yes,
            points=points,
            width=0.25
        )
        assert shape.id == 5
        assert shape.type == "Arc"
        assert shape.locked == Boolean.Yes
        assert shape.layer == "Top Assy"
        assert shape.all_layers == Boolean.Yes
        assert len(shape.points) == 2
        assert shape.width == 0.25
    
    def test_shape_from_xml_line(self):
        """Test parsing a Line shape from XML."""
        xml = etree.fromstring('''
            <Shape Id="1" Type="Line" Locked="N" Layer="Top Silk" AllLayers="N">
                <Points>
                    <Point X="-1.3002" Y="2.5001"/>
                    <Point X="-1.3002" Y="-2.5001"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml, Units.MM)
        assert shape.id == 1
        assert shape.type == "Line"
        assert shape.locked == Boolean.No
        assert shape.layer == "Top Silk"
        assert shape.all_layers == Boolean.No
        assert len(shape.points) == 2
        assert shape.points[0].x == pytest.approx(-1.3002, abs=0.0001)
        assert shape.points[0].y == pytest.approx(2.5001, abs=0.0001)
        assert shape.points[1].x == pytest.approx(-1.3002, abs=0.0001)
        assert shape.points[1].y == pytest.approx(-2.5001, abs=0.0001)
        assert shape.width is None
    
    def test_shape_from_xml_arc(self):
        """Test parsing an Arc shape from XML."""
        xml = etree.fromstring('''
            <Shape Id="6" Type="Arc" Locked="N" Layer="Top Silk" AllLayers="N">
                <Points>
                    <Point X="-0.5002" Y="2.5001"/>
                    <Point X="0" Y="2"/>
                    <Point X="0.5002" Y="2.5001"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml, Units.MM)
        assert shape.id == 6
        assert shape.type == "Arc"
        assert len(shape.points) == 3
        assert shape.points[0].x == pytest.approx(-0.5002, abs=0.0001)
        assert shape.points[1].x == pytest.approx(0, abs=0.0001)
        assert shape.points[1].y == pytest.approx(2, abs=0.0001)
        assert shape.points[2].x == pytest.approx(0.5002, abs=0.0001)
    
    def test_shape_from_xml_with_width(self):
        """Test parsing a shape with width attribute."""
        xml = etree.fromstring('''
            <Shape Id="10" Type="Rectangle" Locked="Y" Layer="Top Assy" AllLayers="Y" Width="0.15">
                <Points>
                    <Point X="0" Y="0"/>
                    <Point X="5" Y="3"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml, Units.MM)
        assert shape.id == 10
        assert shape.type == "Rectangle"
        assert shape.locked == Boolean.Yes
        assert shape.layer == "Top Assy"
        assert shape.all_layers == Boolean.Yes
        assert shape.width == pytest.approx(0.15, abs=0.0001)
        assert len(shape.points) == 2
    
    def test_shape_from_xml_no_points(self):
        """Test parsing a shape without points."""
        xml = etree.fromstring('''
            <Shape Id="7" Type="Text" Locked="N" Layer="Top Silk" AllLayers="N"/>
        ''')
        shape = Shape.from_xml(xml, Units.MM)
        assert shape.id == 7
        assert shape.type == "Text"
        assert shape.points == []
    
    def test_shape_from_xml_units_conversion(self):
        """Test parsing with unit conversion (MIL to MM)."""
        xml = etree.fromstring('''
            <Shape Id="1" Type="Line" Locked="N" Layer="Top Silk" AllLayers="N" Width="10">
                <Points>
                    <Point X="0" Y="0"/>
                    <Point X="100" Y="100"/>
                </Points>
            </Shape>
        ''')
        shape = Shape.from_xml(xml, Units.MIL)
        # 100 mils = 2.54 mm
        assert shape.points[1].x == pytest.approx(2.54, abs=0.01)
        assert shape.points[1].y == pytest.approx(2.54, abs=0.01)
        # 10 mils = 0.254 mm
        assert shape.width == pytest.approx(0.254, abs=0.001)
    
    def test_shape_to_xml_line(self):
        """Test converting a Line shape to XML."""
        shape = Shape(
            id=1,
            type="Line",
            locked=Boolean.No,
            layer="Top Silk",
            all_layers=Boolean.No,
            points=[Point(-1.3, 2.5), Point(-1.3, -2.5)]
        )
        xml = shape.to_xml(Units.MM)
        assert xml.get("Id") == "1"
        assert xml.get("Type") == "Line"
        assert xml.get("Locked") == "N"
        assert xml.get("Layer") == "Top Silk"
        assert xml.get("AllLayers") == "N"
        assert xml.get("Width") is None  # No width specified
        
        points_elem = xml.find("Points")
        assert points_elem is not None
        point_elems = points_elem.findall("Point")
        assert len(point_elems) == 2
        assert point_elems[0].get("X") == "-1.3000"
        assert point_elems[0].get("Y") == "2.5000"
    
    def test_shape_to_xml_with_width(self):
        """Test converting a shape with width to XML."""
        shape = Shape(
            id=10,
            type="Rectangle",
            locked=Boolean.Yes,
            layer="Top Assy",
            all_layers=Boolean.Yes,
            points=[Point(0, 0), Point(5, 3)],
            width=0.15
        )
        xml = shape.to_xml(Units.MM)
        assert xml.get("Id") == "10"
        assert xml.get("Type") == "Rectangle"
        assert xml.get("Locked") == "Y"
        assert xml.get("Width") == "0.1500"
    
    def test_shape_to_xml_no_points(self):
        """Test converting a shape without points."""
        shape = Shape(
            id=7,
            type="Text",
            layer="Top Silk"
        )
        xml = shape.to_xml(Units.MM)
        assert xml.get("Id") == "7"
        assert xml.get("Type") == "Text"
        # Should not have Points element if points list is empty
        assert xml.find("Points") is None
    
    def test_shape_to_xml_units_mil(self):
        """Test converting shape to XML with MIL units."""
        shape = Shape(
            id=1,
            type="Line",
            points=[Point(2.54, 5.08)],  # 100 mils, 200 mils
            width=0.254  # 10 mils
        )
        xml = shape.to_xml(Units.MIL)
        points_elem = xml.find("Points")
        point_elem = points_elem.find("Point")
        # Should be converted to mils
        assert point_elem.get("X") == "100.0000"
        assert point_elem.get("Y") == "200.0000"
        assert xml.get("Width") == "10.0000"
    
    def test_shape_to_xml_units_inch(self):
        """Test converting shape to XML with INCH units."""
        shape = Shape(
            id=1,
            type="Line",
            points=[Point(25.4, 50.8)],  # 1 inch, 2 inches
            width=2.54  # 0.1 inch
        )
        xml = shape.to_xml(Units.INCH)
        points_elem = xml.find("Points")
        point_elem = points_elem.find("Point")
        # Should be converted to inches with 6 decimal places
        assert point_elem.get("X") == "1.000000"
        assert point_elem.get("Y") == "2.000000"
        assert xml.get("Width") == "0.100000"
    
    def test_shape_roundtrip_mm(self):
        """Test Shape XML round-trip conversion (MM units)."""
        original = Shape(
            id=5,
            type="Arc",
            locked=Boolean.Yes,
            layer="Bottom Silk",
            all_layers=Boolean.No,
            points=[
                Point(-0.5, 2.5),
                Point(0, 2.0),
                Point(0.5, 2.5)
            ],
            width=0.2
        )
        xml = original.to_xml(Units.MM)
        parsed = Shape.from_xml(xml, Units.MM)
        
        assert parsed.id == original.id
        assert parsed.type == original.type
        assert parsed.locked == original.locked
        assert parsed.layer == original.layer
        assert parsed.all_layers == original.all_layers
        assert len(parsed.points) == len(original.points)
        assert parsed.points[0].x == pytest.approx(original.points[0].x, abs=0.0001)
        assert parsed.points[1].y == pytest.approx(original.points[1].y, abs=0.0001)
        assert parsed.width == pytest.approx(original.width, abs=0.0001)
    
    def test_shape_roundtrip_mil(self):
        """Test Shape XML round-trip conversion (MIL units)."""
        original = Shape(
            id=3,
            type="Line",
            layer="Top Silk",
            points=[Point(1.27, 2.54), Point(5.08, 7.62)]
        )
        xml = original.to_xml(Units.MIL)
        parsed = Shape.from_xml(xml, Units.MIL)
        
        assert parsed.id == original.id
        assert parsed.type == original.type
        assert len(parsed.points) == 2
        # Allow small tolerance due to unit conversion
        assert parsed.points[0].x == pytest.approx(original.points[0].x, abs=0.01)
        assert parsed.points[1].y == pytest.approx(original.points[1].y, abs=0.01)
    
    def test_shape_locked_values(self):
        """Test different locked values."""
        shape_yes = Shape(locked=Boolean.Yes)
        xml_yes = shape_yes.to_xml()
        assert xml_yes.get("Locked") == "Y"
        
        shape_no = Shape(locked=Boolean.No)
        xml_no = shape_no.to_xml()
        assert xml_no.get("Locked") == "N"
    
    def test_shape_all_layers_values(self):
        """Test different all_layers values."""
        shape_yes = Shape(all_layers=Boolean.Yes)
        xml_yes = shape_yes.to_xml()
        assert xml_yes.get("AllLayers") == "Y"
        
        shape_no = Shape(all_layers=Boolean.No)
        xml_no = shape_no.to_xml()
        assert xml_no.get("AllLayers") == "N"
    
    def test_shape_different_layers(self):
        """Test shapes on different layers."""
        layers = ["Top Silk", "Top Assy", "Bottom Silk", "Bottom Assy", "Top Component Center"]
        for layer in layers:
            shape = Shape(layer=layer)
            xml = shape.to_xml()
            assert xml.get("Layer") == layer
            parsed = Shape.from_xml(xml)
            assert parsed.layer == layer
    
    def test_shape_different_types(self):
        """Test different shape types."""
        types = ["Line", "Arc", "Rectangle", "FillRect", "Polygon", "Text", "Polyline"]
        for shape_type in types:
            shape = Shape(type=shape_type)
            xml = shape.to_xml()
            assert xml.get("Type") == shape_type
            parsed = Shape.from_xml(xml)
            assert parsed.type == shape_type
    
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
            type="Polygon",
            layer="Top Silk",
            points=points,
            width=0.15
        )
        xml = shape.to_xml(Units.MM)
        parsed = Shape.from_xml(xml, Units.MM)
        
        assert parsed.id == 100
        assert parsed.type == "Polygon"
        assert len(parsed.points) == 5
        for i, point in enumerate(parsed.points):
            assert point.x == pytest.approx(points[i].x, abs=0.0001)
            assert point.y == pytest.approx(points[i].y, abs=0.0001)
