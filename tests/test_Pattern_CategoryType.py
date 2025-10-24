#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Pattern_CategoryType.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Pattern.CategoryType tests/test_Pattern_CategoryType.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml import etree
from DipTraceGenerator.Pattern import CategoryType


class TestCategoryType(TestCase):
    """Test the Pattern.CategoryType class."""
    
    def test_create_category_type_defaults(self):
        """Test creating a CategoryType with default values."""
        ct = CategoryType()
        self.assertEqual(ct.type_index, 0)
        self.assertEqual(ct.type_name, "")
        self.assertIsNone(ct.subtype_index)
        self.assertIsNone(ct.subtype_name)
    
    def test_create_category_type_with_type_only(self):
        """Test creating a CategoryType with only Type values."""
        ct = CategoryType(
            type_index=2,
            type_name="SOIC"
        )
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertIsNone(ct.subtype_index)
        self.assertIsNone(ct.subtype_name)
    
    def test_create_category_type_with_type_and_subtype(self):
        """Test creating a CategoryType with both Type and SubType values."""
        ct = CategoryType(
            type_index=2,
            type_name="SOIC",
            subtype_index=7,
            subtype_name="Pitch 1.27mm"
        )
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertEqual(ct.subtype_index, 7)
        self.assertEqual(ct.subtype_name, "Pitch 1.27mm")
    
    def test_from_xml_type_only(self):
        """Test parsing a CategoryType with only Type from XML."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type Index="2">SOIC</Type>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertIsNone(ct.subtype_index)
        self.assertIsNone(ct.subtype_name)
    
    def test_from_xml_type_and_subtype(self):
        """Test parsing a CategoryType with Type and SubType from XML."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type Index="2">SOIC</Type>
                <SubType Index="7">Pitch 1.27mm</SubType>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertEqual(ct.subtype_index, 7)
        self.assertEqual(ct.subtype_name, "Pitch 1.27mm")
    
    def test_from_xml_exposed_pad_subtype(self):
        """Test parsing a CategoryType with Exposed Pad SubType."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type Index="2">SOIC</Type>
                <SubType Index="0">Exposed Pad</SubType>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertEqual(ct.subtype_index, 0)
        self.assertEqual(ct.subtype_name, "Exposed Pad")
    
    def test_from_xml_overall_width_subtype(self):
        """Test parsing a CategoryType with Overall Width SubType."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type Index="2">SOIC</Type>
                <SubType Index="2">Overall Width by Leads 6mm</SubType>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertEqual(ct.subtype_index, 2)
        self.assertEqual(ct.subtype_name, "Overall Width by Leads 6mm")
    
    def test_from_xml_package_width_subtype(self):
        """Test parsing a CategoryType with Package Width SubType."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type Index="2">SOIC</Type>
                <SubType Index="4">Package Width 150mil</SubType>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertEqual(ct.subtype_index, 4)
        self.assertEqual(ct.subtype_name, "Package Width 150mil")
    
    def test_from_xml_empty_type_element(self):
        """Test parsing a CategoryType with empty Type element."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type Index="0"></Type>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 0)
        self.assertEqual(ct.type_name, "")
        self.assertIsNone(ct.subtype_index)
        self.assertIsNone(ct.subtype_name)
    
    def test_from_xml_missing_type_element(self):
        """Test parsing a CategoryType with missing Type element."""
        xml_element = etree.fromstring('''
            <CategoryType>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 0)
        self.assertEqual(ct.type_name, "")
        self.assertIsNone(ct.subtype_index)
        self.assertIsNone(ct.subtype_name)
    
    def test_from_xml_missing_type_index(self):
        """Test parsing a CategoryType with missing Type Index attribute."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type>SOIC</Type>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 0)
        self.assertEqual(ct.type_name, "SOIC")
    
    def test_from_xml_missing_subtype_index(self):
        """Test parsing a CategoryType with missing SubType Index attribute."""
        xml_element = etree.fromstring('''
            <CategoryType>
                <Type Index="2">SOIC</Type>
                <SubType>Pitch 1.27mm</SubType>
            </CategoryType>
        ''')
        ct = CategoryType.from_xml(xml_element)
        self.assertEqual(ct.type_index, 2)
        self.assertEqual(ct.type_name, "SOIC")
        self.assertEqual(ct.subtype_index, 0)
        self.assertEqual(ct.subtype_name, "Pitch 1.27mm")
    
    def test_to_xml_type_only(self):
        """Test converting a CategoryType with only Type to XML."""
        ct = CategoryType(
            type_index=2,
            type_name="SOIC"
        )
        xml_element = ct.to_xml()
        self.assertEqual(xml_element.tag, "CategoryType")
        
        type_elem = xml_element.find("Type")
        self.assertIsNotNone(type_elem)
        self.assertEqual(type_elem.get("Index"), "2")
        self.assertEqual(type_elem.text, "SOIC")
        
        subtype_elem = xml_element.find("SubType")
        self.assertIsNone(subtype_elem)
    
    def test_to_xml_type_and_subtype(self):
        """Test converting a CategoryType with Type and SubType to XML."""
        ct = CategoryType(
            type_index=2,
            type_name="SOIC",
            subtype_index=7,
            subtype_name="Pitch 1.27mm"
        )
        xml_element = ct.to_xml()
        self.assertEqual(xml_element.tag, "CategoryType")
        
        type_elem = xml_element.find("Type")
        self.assertIsNotNone(type_elem)
        self.assertEqual(type_elem.get("Index"), "2")
        self.assertEqual(type_elem.text, "SOIC")
        
        subtype_elem = xml_element.find("SubType")
        self.assertIsNotNone(subtype_elem)
        self.assertEqual(subtype_elem.get("Index"), "7")
        self.assertEqual(subtype_elem.text, "Pitch 1.27mm")
    
    def test_to_xml_empty_type(self):
        """Test converting a CategoryType with empty Type to XML."""
        ct = CategoryType(
            type_index=0,
            type_name=""
        )
        xml_element = ct.to_xml()
        
        type_elem = xml_element.find("Type")
        self.assertIsNotNone(type_elem)
        self.assertEqual(type_elem.get("Index"), "0")
        self.assertEqual(type_elem.text, "")
    
    def test_to_xml_partial_subtype_index_only(self):
        """Test that SubType is not added if only subtype_index is set."""
        ct = CategoryType(
            type_index=2,
            type_name="SOIC",
            subtype_index=7,
            subtype_name=None
        )
        xml_element = ct.to_xml()
        
        subtype_elem = xml_element.find("SubType")
        self.assertIsNone(subtype_elem)
    
    def test_to_xml_partial_subtype_name_only(self):
        """Test that SubType is not added if only subtype_name is set."""
        ct = CategoryType(
            type_index=2,
            type_name="SOIC",
            subtype_index=None,
            subtype_name="Pitch 1.27mm"
        )
        xml_element = ct.to_xml()
        
        subtype_elem = xml_element.find("SubType")
        self.assertIsNone(subtype_elem)
    
    def test_roundtrip_type_only(self):
        """Test roundtrip conversion for CategoryType with Type only."""
        original_xml = '''
            <CategoryType>
                <Type Index="5">QFP</Type>
            </CategoryType>
        '''
        original_element = etree.fromstring(original_xml)
        ct = CategoryType.from_xml(original_element)
        new_element = ct.to_xml()
        
        self.assertEqual(new_element.tag, "CategoryType")
        type_elem = new_element.find("Type")
        self.assertEqual(type_elem.get("Index"), "5")
        self.assertEqual(type_elem.text, "QFP")
        self.assertIsNone(new_element.find("SubType"))
    
    def test_roundtrip_type_and_subtype(self):
        """Test roundtrip conversion for CategoryType with Type and SubType."""
        original_xml = '''
            <CategoryType>
                <Type Index="2">SOIC</Type>
                <SubType Index="3">Overall Width by Leads 7.8mm</SubType>
            </CategoryType>
        '''
        original_element = etree.fromstring(original_xml)
        ct = CategoryType.from_xml(original_element)
        new_element = ct.to_xml()
        
        type_elem = new_element.find("Type")
        self.assertEqual(type_elem.get("Index"), "2")
        self.assertEqual(type_elem.text, "SOIC")
        
        subtype_elem = new_element.find("SubType")
        self.assertEqual(subtype_elem.get("Index"), "3")
        self.assertEqual(subtype_elem.text, "Overall Width by Leads 7.8mm")
    
    def test_different_type_names(self):
        """Test CategoryType with various Type names."""
        type_names = ["SOIC", "QFP", "BGA", "DIP", "SOP"]
        for name in type_names:
            ct = CategoryType(type_index=1, type_name=name)
            self.assertEqual(ct.type_name, name)
    
    def test_different_subtype_names(self):
        """Test CategoryType with various SubType names."""
        subtypes = [
            "Exposed Pad",
            "Overall Width by Leads 6mm",
            "Package Width 150mil",
            "Pitch 1.27mm",
            "Body Size 5x5mm"
        ]
        for idx, subtype_name in enumerate(subtypes):
            ct = CategoryType(
                type_index=2,
                type_name="SOIC",
                subtype_index=idx,
                subtype_name=subtype_name
            )
            self.assertEqual(ct.subtype_name, subtype_name)
            self.assertEqual(ct.subtype_index, idx)
    
    def test_large_index_values(self):
        """Test CategoryType with large index values."""
        ct = CategoryType(
            type_index=999,
            type_name="CustomType",
            subtype_index=888,
            subtype_name="CustomSubType"
        )
        self.assertEqual(ct.type_index, 999)
        self.assertEqual(ct.subtype_index, 888)
        
        xml_element = ct.to_xml()
        type_elem = xml_element.find("Type")
        self.assertEqual(type_elem.get("Index"), "999")
        
        subtype_elem = xml_element.find("SubType")
        self.assertEqual(subtype_elem.get("Index"), "888")
    
    def test_xml_structure_type_only(self):
        """Test that XML structure matches expected format for Type only."""
        ct = CategoryType(type_index=1, type_name="Test")
        xml_element = ct.to_xml()
        
        # Verify element order
        children = list(xml_element)
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].tag, "Type")
    
    def test_xml_structure_type_and_subtype(self):
        """Test that XML structure matches expected format for Type and SubType."""
        ct = CategoryType(
            type_index=1,
            type_name="Test",
            subtype_index=2,
            subtype_name="SubTest"
        )
        xml_element = ct.to_xml()
        
        # Verify element order
        children = list(xml_element)
        self.assertEqual(len(children), 2)
        self.assertEqual(children[0].tag, "Type")
        self.assertEqual(children[1].tag, "SubType")


if __name__ == '__main__':
    main()
