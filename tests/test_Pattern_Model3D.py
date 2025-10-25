#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from unittest import TestCase, main
from DipTraceGenerator.Pattern import Model3D, Filename, Rotate, Offset, Zoom, Model3DUnits, Model3DType
from DipTraceGenerator import Units, Boolean
from lxml import etree


class TestFilename(TestCase):
    """Test cases for Filename class."""

    def test_default_constructor(self):
        """Test creating Filename with default values."""
        filename = Filename()
        self.assertEqual(filename.path, "")
        self.assertEqual(filename.var, "")

    def test_constructor_with_values(self):
        """Test creating Filename with specific values."""
        filename = Filename(path="soic-8_150mil.step", var="soic-8_150mil.step")
        self.assertEqual(filename.path, "soic-8_150mil.step")
        self.assertEqual(filename.var, "soic-8_150mil.step")

    def test_from_xml(self):
        """Test parsing Filename from XML."""
        xml = '''<Filename>
            <Path>soic-8_150mil.step</Path>
            <Var>soic-8_150mil.step</Var>
        </Filename>'''
        element = etree.fromstring(xml)
        filename = Filename.from_xml(element)
        
        self.assertEqual(filename.path, "soic-8_150mil.step")
        self.assertEqual(filename.var, "soic-8_150mil.step")

    def test_from_xml_with_full_path(self):
        """Test parsing Filename with full Windows path."""
        xml = '''<Filename>
            <Path>C:\\Program Files (x86)\\DipTrace\\models3d\\DIP Peg Leads\\dip-10(16)s.step</Path>
            <Var>C:\\Program Files (x86)\\DipTrace\\models3d\\DIP Peg Leads\\dip-10(16)s.step</Var>
        </Filename>'''
        element = etree.fromstring(xml)
        filename = Filename.from_xml(element)
        
        self.assertIn("DipTrace", filename.path)
        self.assertIn("dip-10(16)s.step", filename.path)

    def test_to_xml(self):
        """Test converting Filename to XML."""
        filename = Filename(path="test.step", var="test.step")
        element = filename.to_xml()
        
        self.assertEqual(element.tag, "Filename")
        path_elem = element.find("Path")
        var_elem = element.find("Var")
        self.assertIsNotNone(path_elem)
        self.assertIsNotNone(var_elem)
        self.assertEqual(path_elem.text, "test.step")
        self.assertEqual(var_elem.text, "test.step")

    def test_roundtrip(self):
        """Test Filename roundtrip conversion."""
        xml = '''<Filename>
            <Path>model.step</Path>
            <Var>model.step</Var>
        </Filename>'''
        element1 = etree.fromstring(xml)
        filename = Filename.from_xml(element1)
        element2 = filename.to_xml()
        
        self.assertEqual(element2.find("Path").text, element1.find("Path").text)
        self.assertEqual(element2.find("Var").text, element1.find("Var").text)


class TestRotate(TestCase):
    """Test cases for Rotate class."""

    def test_default_constructor(self):
        """Test creating Rotate with default values."""
        rotate = Rotate()
        self.assertEqual(rotate.x, 0.0)
        self.assertEqual(rotate.y, 0.0)
        self.assertEqual(rotate.z, 0.0)

    def test_constructor_with_values(self):
        """Test creating Rotate with specific values."""
        rotate = Rotate(x=90.0, y=45.0, z=180.0)
        self.assertEqual(rotate.x, 90.0)
        self.assertEqual(rotate.y, 45.0)
        self.assertEqual(rotate.z, 180.0)

    def test_from_xml(self):
        """Test parsing Rotate from XML."""
        xml = '<Rotate X="90" Y="45" Z="180"/>'
        element = etree.fromstring(xml)
        rotate = Rotate.from_xml(element)
        
        self.assertEqual(rotate.x, 90.0)
        self.assertEqual(rotate.y, 45.0)
        self.assertEqual(rotate.z, 180.0)

    def test_from_xml_zeros(self):
        """Test parsing Rotate with zero values."""
        xml = '<Rotate X="0" Y="0" Z="0"/>'
        element = etree.fromstring(xml)
        rotate = Rotate.from_xml(element)
        
        self.assertEqual(rotate.x, 0.0)
        self.assertEqual(rotate.y, 0.0)
        self.assertEqual(rotate.z, 0.0)

    def test_to_xml(self):
        """Test converting Rotate to XML."""
        rotate = Rotate(x=90.0, y=45.0, z=180.0)
        element = rotate.to_xml()
        
        self.assertEqual(element.tag, "Rotate")
        self.assertEqual(element.get("X"), "90")
        self.assertEqual(element.get("Y"), "45")
        self.assertEqual(element.get("Z"), "180")

    def test_to_xml_zeros(self):
        """Test converting Rotate with zeros to XML."""
        rotate = Rotate(x=0.0, y=0.0, z=0.0)
        element = rotate.to_xml()
        
        self.assertEqual(element.get("X"), "0")
        self.assertEqual(element.get("Y"), "0")
        self.assertEqual(element.get("Z"), "0")

    def test_negative_angles(self):
        """Test Rotate with negative angles."""
        rotate = Rotate(x=-90.0, y=-45.0, z=-180.0)
        element = rotate.to_xml()
        
        self.assertEqual(element.get("X"), "-90")
        self.assertEqual(element.get("Y"), "-45")
        self.assertEqual(element.get("Z"), "-180")


class TestOffset(TestCase):
    """Test cases for Offset class."""

    def test_default_constructor(self):
        """Test creating Offset with default values."""
        offset = Offset()
        self.assertEqual(offset.x, 0.0)
        self.assertEqual(offset.y, 0.0)
        self.assertEqual(offset.z, 0.0)

    def test_constructor_with_values(self):
        """Test creating Offset with specific values."""
        offset = Offset(x=1.5, y=2.5, z=3.5)
        self.assertEqual(offset.x, 1.5)
        self.assertEqual(offset.y, 2.5)
        self.assertEqual(offset.z, 3.5)

    def test_from_xml(self):
        """Test parsing Offset from XML."""
        xml = '<Offset X="1.5" Y="2.5" Z="3.5"/>'
        element = etree.fromstring(xml)
        offset = Offset.from_xml(element)
        
        self.assertAlmostEqual(offset.x, 1.5, places=4)
        self.assertAlmostEqual(offset.y, 2.5, places=4)
        self.assertAlmostEqual(offset.z, 3.5, places=4)

    def test_from_xml_zeros(self):
        """Test parsing Offset with zero values."""
        xml = '<Offset X="0" Y="0" Z="0"/>'
        element = etree.fromstring(xml)
        offset = Offset.from_xml(element)
        
        self.assertEqual(offset.x, 0.0)
        self.assertEqual(offset.y, 0.0)
        self.assertEqual(offset.z, 0.0)

    def test_to_xml(self):
        """Test converting Offset to XML."""
        offset = Offset(x=1.5, y=2.5, z=3.5)
        element = offset.to_xml()
        
        self.assertEqual(element.tag, "Offset")
        self.assertEqual(element.get("X"), "1.5")
        self.assertEqual(element.get("Y"), "2.5")
        self.assertEqual(element.get("Z"), "3.5")

    def test_to_xml_zeros(self):
        """Test converting Offset with zeros to XML."""
        offset = Offset(x=0.0, y=0.0, z=0.0)
        element = offset.to_xml()
        
        self.assertEqual(element.get("X"), "0")
        self.assertEqual(element.get("Y"), "0")
        self.assertEqual(element.get("Z"), "0")

    def test_unit_conversion_mil(self):
        """Test Offset unit conversion to MIL."""
        offset = Offset(x=2.54, y=1.27, z=5.08)  # 100, 50, 200 mils
        element = offset.to_xml(Units.MIL)
        
        self.assertEqual(element.get("X"), "100")
        self.assertEqual(element.get("Y"), "50")
        self.assertEqual(element.get("Z"), "200")

    def test_negative_offset(self):
        """Test Offset with negative values."""
        offset = Offset(x=-1.5, y=-2.5, z=-3.5)
        element = offset.to_xml()
        
        self.assertEqual(element.get("X"), "-1.5")
        self.assertEqual(element.get("Y"), "-2.5")
        self.assertEqual(element.get("Z"), "-3.5")


class TestZoom(TestCase):
    """Test cases for Zoom class."""

    def test_default_constructor(self):
        """Test creating Zoom with default values."""
        zoom = Zoom()
        self.assertEqual(zoom.x, 1.0)
        self.assertEqual(zoom.y, 1.0)
        self.assertEqual(zoom.z, 1.0)

    def test_constructor_with_values(self):
        """Test creating Zoom with specific values."""
        zoom = Zoom(x=2.0, y=1.5, z=0.5)
        self.assertEqual(zoom.x, 2.0)
        self.assertEqual(zoom.y, 1.5)
        self.assertEqual(zoom.z, 0.5)

    def test_from_xml(self):
        """Test parsing Zoom from XML."""
        xml = '<Zoom X="2" Y="1.5" Z="0.5"/>'
        element = etree.fromstring(xml)
        zoom = Zoom.from_xml(element)
        
        self.assertEqual(zoom.x, 2.0)
        self.assertEqual(zoom.y, 1.5)
        self.assertEqual(zoom.z, 0.5)

    def test_from_xml_ones(self):
        """Test parsing Zoom with default values (1.0)."""
        xml = '<Zoom X="1" Y="1" Z="1"/>'
        element = etree.fromstring(xml)
        zoom = Zoom.from_xml(element)
        
        self.assertEqual(zoom.x, 1.0)
        self.assertEqual(zoom.y, 1.0)
        self.assertEqual(zoom.z, 1.0)

    def test_to_xml(self):
        """Test converting Zoom to XML."""
        zoom = Zoom(x=2.0, y=1.5, z=0.5)
        element = zoom.to_xml()
        
        self.assertEqual(element.tag, "Zoom")
        self.assertEqual(element.get("X"), "2")
        self.assertEqual(element.get("Y"), "1.5")
        self.assertEqual(element.get("Z"), "0.5")

    def test_to_xml_ones(self):
        """Test converting Zoom with 1.0 values to XML."""
        zoom = Zoom(x=1.0, y=1.0, z=1.0)
        element = zoom.to_xml()
        
        self.assertEqual(element.get("X"), "1")
        self.assertEqual(element.get("Y"), "1")
        self.assertEqual(element.get("Z"), "1")


class TestModel3D(TestCase):
    """Test cases for Pattern.Model3D class."""

    def test_default_constructor(self):
        """Test creating Model3D with default values."""
        model = Model3D()
        self.assertEqual(model.mirror, Boolean.No)
        self.assertEqual(model.no_search, Boolean.No)
        self.assertEqual(model.units, Model3DUnits.MM)
        self.assertEqual(model.ipc_xoff, 0.0)
        self.assertEqual(model.ipc_yoff, 0.0)
        self.assertEqual(model.auto_height, 0.0)
        self.assertEqual(model.auto_color, 4934475)
        self.assertEqual(model.model_type, Model3DType.File)
        self.assertEqual(model.keep_pins, Boolean.No)
        self.assertIsNone(model.filename)
        self.assertIsNone(model.rotate)
        self.assertIsNone(model.offset)
        self.assertIsNone(model.zoom)

    def test_constructor_with_values(self):
        """Test creating Model3D with specific values."""
        filename = Filename(path="test.step", var="test.step")
        model = Model3D(
            mirror=Boolean.Yes,
            units=Model3DUnits.Wings,
            model_type=Model3DType.IPC7351,
            filename=filename
        )
        self.assertEqual(model.mirror, Boolean.Yes)
        self.assertEqual(model.units, Model3DUnits.Wings)
        self.assertEqual(model.model_type, Model3DType.IPC7351)
        self.assertEqual(model.filename, filename)

    def test_from_xml_simple(self):
        """Test parsing simple Model3D from XML."""
        xml = '''<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">
            <Filename>
                <Path>soic-8_150mil.step</Path>
                <Var>soic-8_150mil.step</Var>
            </Filename>
            <Rotate X="0" Y="0" Z="0"/>
            <Offset X="0" Y="0" Z="0"/>
            <Zoom X="1" Y="1" Z="1"/>
        </Model3D>'''
        element = etree.fromstring(xml)
        model = Model3D.from_xml(element)
        
        self.assertEqual(model.mirror, Boolean.No)
        self.assertEqual(model.no_search, Boolean.No)
        self.assertEqual(model.units, Model3DUnits.MM)
        self.assertEqual(model.model_type, Model3DType.File)
        self.assertIsNotNone(model.filename)
        self.assertEqual(model.filename.path, "soic-8_150mil.step")
        self.assertIsNotNone(model.rotate)
        self.assertIsNotNone(model.offset)
        self.assertIsNotNone(model.zoom)

    def test_from_xml_with_mirror(self):
        """Test parsing Model3D with mirror enabled."""
        xml = '''<Model3D Mirror="Y" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">
            <Filename>
                <Path>test.step</Path>
                <Var>test.step</Var>
            </Filename>
            <Rotate X="0" Y="0" Z="0"/>
            <Offset X="0" Y="0" Z="0"/>
            <Zoom X="1" Y="1" Z="1"/>
        </Model3D>'''
        element = etree.fromstring(xml)
        model = Model3D.from_xml(element)
        
        self.assertEqual(model.mirror, Boolean.Yes)

    def test_from_xml_wings_units(self):
        """Test parsing Model3D with Wings units."""
        xml = '''<Model3D Mirror="N" NoSearch="N" Units="Wings" IPC_XOff="-0.483393" IPC_YOff="0.103078" AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">
            <Filename>
                <Path>test.step</Path>
                <Var>test.step</Var>
            </Filename>
            <Rotate X="0" Y="0" Z="0"/>
            <Offset X="0" Y="0" Z="0"/>
            <Zoom X="1" Y="1" Z="1"/>
        </Model3D>'''
        element = etree.fromstring(xml)
        model = Model3D.from_xml(element)
        
        self.assertEqual(model.units, Model3DUnits.Wings)
        self.assertAlmostEqual(model.ipc_xoff, -0.483393, places=4)
        self.assertAlmostEqual(model.ipc_yoff, 0.103078, places=4)

    def test_from_xml_ipc7351_type(self):
        """Test parsing Model3D with IPC-7351 type."""
        xml = '''<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0" AutoColor="4934475" Type="IPC-7351" KeepPins="Y">
            <Rotate X="0" Y="0" Z="0"/>
            <Offset X="0" Y="0" Z="0"/>
            <Zoom X="1" Y="1" Z="1"/>
        </Model3D>'''
        element = etree.fromstring(xml)
        model = Model3D.from_xml(element)
        
        self.assertEqual(model.model_type, Model3DType.IPC7351)
        self.assertEqual(model.keep_pins, Boolean.Yes)

    def test_from_xml_outline_type(self):
        """Test parsing Model3D with Outline type."""
        xml = '''<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="5" AutoColor="4934475" Type="Outline" KeepPins="N">
            <Rotate X="0" Y="0" Z="0"/>
            <Offset X="0" Y="0" Z="0"/>
            <Zoom X="1" Y="1" Z="1"/>
        </Model3D>'''
        element = etree.fromstring(xml)
        model = Model3D.from_xml(element)
        
        self.assertEqual(model.model_type, Model3DType.Outline)
        self.assertAlmostEqual(model.auto_height, 5.0, places=4)

    def test_to_xml_simple(self):
        """Test converting simple Model3D to XML."""
        filename = Filename(path="test.step", var="test.step")
        rotate = Rotate(x=0.0, y=0.0, z=0.0)
        offset = Offset(x=0.0, y=0.0, z=0.0)
        zoom = Zoom(x=1.0, y=1.0, z=1.0)
        
        model = Model3D(
            mirror=Boolean.No,
            no_search=Boolean.No,
            units=Model3DUnits.MM,
            model_type=Model3DType.File,
            filename=filename,
            rotate=rotate,
            offset=offset,
            zoom=zoom
        )
        element = model.to_xml()
        
        self.assertEqual(element.tag, "Model3D")
        self.assertEqual(element.get("Mirror"), "N")
        self.assertEqual(element.get("NoSearch"), "N")
        self.assertEqual(element.get("Units"), "mm")
        self.assertEqual(element.get("Type"), "File")
        self.assertIsNotNone(element.find("Filename"))
        self.assertIsNotNone(element.find("Rotate"))
        self.assertIsNotNone(element.find("Offset"))
        self.assertIsNotNone(element.find("Zoom"))

    def test_to_xml_without_optional_children(self):
        """Test converting Model3D without optional children."""
        model = Model3D(
            mirror=Boolean.No,
            units=Model3DUnits.MM,
            model_type=Model3DType.File
        )
        element = model.to_xml()
        
        self.assertIsNone(element.find("Filename"))
        self.assertIsNone(element.find("Rotate"))
        self.assertIsNone(element.find("Offset"))
        self.assertIsNone(element.find("Zoom"))

    def test_all_model_types(self):
        """Test all model type values."""
        types = [Model3DType.File, Model3DType.IPC7351, Model3DType.Outline]
        
        for model_type in types:
            with self.subTest(model_type=model_type):
                model = Model3D(model_type=model_type)
                element = model.to_xml()
                self.assertEqual(element.get("Type"), model_type.value)

    def test_all_units(self):
        """Test all unit values."""
        units = [Model3DUnits.MM, Model3DUnits.MIL, Model3DUnits.INCH, Model3DUnits.Wings]
        
        for unit in units:
            with self.subTest(unit=unit):
                model = Model3D(units=unit)
                element = model.to_xml()
                self.assertEqual(element.get("Units"), unit.value)

    def test_unit_conversion_offsets(self):
        """Test unit conversion for IPC offsets and auto height."""
        model = Model3D(
            ipc_xoff=2.54,  # 100 mils
            ipc_yoff=1.27,  # 50 mils
            auto_height=5.08  # 200 mils
        )
        element = model.to_xml(Units.MIL)
        
        self.assertEqual(element.get("IPC_XOff"), "100")
        self.assertEqual(element.get("IPC_YOff"), "50")
        self.assertEqual(element.get("AutoHeight"), "200")

    def test_roundtrip_conversion(self):
        """Test Model3D roundtrip conversion."""
        xml = '''<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">
            <Filename>
                <Path>soic-8_150mil.step</Path>
                <Var>soic-8_150mil.step</Var>
            </Filename>
            <Rotate X="0" Y="0" Z="0"/>
            <Offset X="0" Y="0" Z="0"/>
            <Zoom X="1" Y="1" Z="1"/>
        </Model3D>'''
        element1 = etree.fromstring(xml)
        model = Model3D.from_xml(element1)
        element2 = model.to_xml()
        
        self.assertEqual(element2.get("Mirror"), element1.get("Mirror"))
        self.assertEqual(element2.get("Type"), element1.get("Type"))
        self.assertEqual(element2.get("Units"), element1.get("Units"))

    def test_auto_color_value(self):
        """Test Model3D with specific auto color value."""
        model = Model3D(auto_color=16711680)  # Red color
        element = model.to_xml()
        
        self.assertEqual(element.get("AutoColor"), "16711680")

    def test_negative_ipc_offsets(self):
        """Test Model3D with negative IPC offsets."""
        model = Model3D(ipc_xoff=-0.5, ipc_yoff=-1.5)
        element = model.to_xml()
        
        self.assertEqual(element.get("IPC_XOff"), "-0.5")
        self.assertEqual(element.get("IPC_YOff"), "-1.5")

    def test_parse_real_world_sample(self):
        """Test parsing real-world Model3D sample."""
        xml = '''<Model3D Mirror="N" NoSearch="N" Units="mm" IPC_XOff="0" IPC_YOff="0" AutoHeight="0" AutoColor="4934475" Type="File" KeepPins="N">
            <Filename>
                <Path>soic-8_150mil.step</Path>
                <Var>soic-8_150mil.step</Var>
            </Filename>
            <Rotate X="0" Y="0" Z="0"/>
            <Offset X="0" Y="0" Z="0"/>
            <Zoom X="1" Y="1" Z="1"/>
        </Model3D>'''
        element = etree.fromstring(xml)
        model = Model3D.from_xml(element)
        
        self.assertEqual(model.mirror, Boolean.No)
        self.assertEqual(model.model_type, Model3DType.File)
        self.assertIsNotNone(model.filename)
        self.assertEqual(model.filename.path, "soic-8_150mil.step")


if __name__ == "__main__":
    main()
