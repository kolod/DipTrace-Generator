#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_SpiceModel.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.SpiceModel tests/test_Component_SpiceModel.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator.Component import SpiceModel
from DipTraceGenerator import SpiceModelType


class TestSpiceModel(TestCase):
    """Test cases for SpiceModel class"""

    def test_spice_model_default_initialization(self):
        """Test SpiceModel initializes with default values"""
        model = SpiceModel()
        self.assertEqual(model.type, SpiceModelType.SubCkt)

    def test_spice_model_initialization_with_subckt(self):
        """Test SpiceModel initialization with SubCkt type"""
        model = SpiceModel(type=SpiceModelType.SubCkt)
        self.assertEqual(model.type, SpiceModelType.SubCkt)

    def test_spice_model_initialization_with_model(self):
        """Test SpiceModel initialization with Model type"""
        model = SpiceModel(type=SpiceModelType.Model)
        self.assertEqual(model.type, SpiceModelType.Model)

    def test_from_xml_subckt(self):
        """Test creating SpiceModel with SubCkt type from XML"""
        xml_str = '<SpiceModel Type="SubCkt"/>'
        element = xml(xml_str)
        model = SpiceModel.from_xml(element)
        
        self.assertEqual(model.type, SpiceModelType.SubCkt)

    def test_from_xml_model(self):
        """Test creating SpiceModel with Model type from XML"""
        xml_str = '<SpiceModel Type="Model"/>'
        element = xml(xml_str)
        model = SpiceModel.from_xml(element)
        
        self.assertEqual(model.type, SpiceModelType.Model)

    def test_from_xml_default_when_no_type(self):
        """Test SpiceModel defaults to SubCkt when Type attribute is missing"""
        xml_str = '<SpiceModel/>'
        element = xml(xml_str)
        model = SpiceModel.from_xml(element)
        
        self.assertEqual(model.type, SpiceModelType.SubCkt)

    def test_to_xml_subckt(self):
        """Test converting SpiceModel with SubCkt type to XML"""
        model = SpiceModel(type=SpiceModelType.SubCkt)
        element = model.to_xml()
        
        self.assertEqual(element.tag, "SpiceModel")
        self.assertEqual(element.get("Type"), "SubCkt")

    def test_to_xml_model(self):
        """Test converting SpiceModel with Model type to XML"""
        model = SpiceModel(type=SpiceModelType.Model)
        element = model.to_xml()
        
        self.assertEqual(element.tag, "SpiceModel")
        self.assertEqual(element.get("Type"), "Model")

    def test_round_trip_subckt(self):
        """Test round-trip: SpiceModel -> XML -> SpiceModel with SubCkt"""
        original = SpiceModel(type=SpiceModelType.SubCkt)
        element = original.to_xml()
        recovered = SpiceModel.from_xml(element)
        
        self.assertEqual(recovered.type, original.type)

    def test_round_trip_model(self):
        """Test round-trip: SpiceModel -> XML -> SpiceModel with Model"""
        original = SpiceModel(type=SpiceModelType.Model)
        element = original.to_xml()
        recovered = SpiceModel.from_xml(element)
        
        self.assertEqual(recovered.type, original.type)

    def test_all_spice_model_types(self):
        """Test all SPICE model types can be created and serialized"""
        for model_type in SpiceModelType:
            model = SpiceModel(type=model_type)
            element = model.to_xml()
            recovered = SpiceModel.from_xml(element)
            self.assertEqual(recovered.type, model_type)

    def test_xml_element_has_no_children(self):
        """Test that SpiceModel XML element has no child elements"""
        model = SpiceModel()
        element = model.to_xml()
        
        self.assertEqual(len(element), 0)
        self.assertIsNone(element.text)

    def test_xml_element_has_only_type_attribute(self):
        """Test that SpiceModel XML element has only Type attribute"""
        model = SpiceModel()
        element = model.to_xml()
        
        self.assertEqual(len(element.attrib), 1)
        self.assertIn("Type", element.attrib)


if __name__ == "__main__":
    main()
