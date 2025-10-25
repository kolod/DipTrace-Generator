"""Tests for Pattern.Category module"""

import unittest
from lxml import etree
from DipTraceGenerator.Pattern.Category import Category

# Aliases for convenience
SubType = Category.SubType
Type = Category.Type


class TestSubType(unittest.TestCase):
    """Tests for SubType dataclass"""

    def test_subtype_default(self):
        """Test SubType with default values"""
        subtype = SubType()
        self.assertEqual(subtype.number, 0)
        self.assertEqual(subtype.name, "")

    def test_subtype_init(self):
        """Test SubType initialization"""
        subtype = SubType(number=1, name="Inline Leads")
        self.assertEqual(subtype.number, 1)
        self.assertEqual(subtype.name, "Inline Leads")


class TestType(unittest.TestCase):
    """Tests for Type dataclass"""

    def test_type_default(self):
        """Test Type with default values"""
        type_obj = Type()
        self.assertEqual(type_obj.number, 0)
        self.assertEqual(type_obj.name, "")
        self.assertEqual(type_obj.subtypes, [])

    def test_type_init(self):
        """Test Type initialization"""
        subtype1 = SubType(0, "Inline Leads")
        subtype2 = SubType(1, "Staggered Leads")
        type_obj = Type(number=4, name="''TO-92", subtypes=[subtype1, subtype2])
        
        self.assertEqual(type_obj.number, 4)
        self.assertEqual(type_obj.name, "''TO-92")
        self.assertEqual(len(type_obj.subtypes), 2)


class TestCategory(unittest.TestCase):
    """Tests for Category class"""

    def test_category_default(self):
        """Test Category with default values"""
        category = Category()
        self.assertEqual(category.number, 0)
        self.assertEqual(category.name, "")
        self.assertEqual(category.types, [])

    def test_category_init(self):
        """Test Category initialization"""
        type1 = Type(0, "Type1")
        type2 = Type(1, "Type2")
        category = Category(number=1, name="'BGA", types=[type1, type2])
        
        self.assertEqual(category.number, 1)
        self.assertEqual(category.name, "'BGA")
        self.assertEqual(len(category.types), 2)

    def test_category_to_xml_with_types(self):
        """Test Category to_xml conversion with types"""
        type1 = Type(0, "''TO-5", subtypes=[])
        type2 = Type(1, "''TO-92", subtypes=[SubType(0, "Inline")])
        category = Category(number=15, name="'Transistor", types=[type1, type2])
        elem = category.to_xml()
        
        self.assertEqual(elem.tag, 'Category')
        self.assertEqual(elem.get('Number'), '15')
        self.assertEqual(elem.findtext('Name'), "'Transistor")
        
        types_elem = elem.find('Types')
        self.assertIsNotNone(types_elem)
        type_elems = types_elem.findall('Type')
        self.assertEqual(len(type_elems), 2)

    def test_category_to_xml_empty_types(self):
        """Test Category to_xml conversion with empty types"""
        category = Category(number=0, name="'BGA", types=[])
        elem = category.to_xml()
        
        self.assertEqual(elem.get('Number'), '0')
        self.assertEqual(elem.findtext('Name'), "'BGA")
        
        types_elem = elem.find('Types')
        self.assertIsNotNone(types_elem)
        type_elems = types_elem.findall('Type')
        self.assertEqual(len(type_elems), 0)

    def test_category_from_xml_with_types(self):
        """Test Category from_xml parsing with types"""
        xml_str = """
        <Category Number="15">
            <Name>'Transistor</Name>
            <Types>
                <Type Number="3">
                    <Name>''TO-5</Name>
                    <SubTypes/>
                </Type>
                <Type Number="4">
                    <Name>''TO-92</Name>
                    <SubTypes>
                        <SubType Number="0">
                            <Name>'Inline Leads</Name>
                        </SubType>
                        <SubType Number="1">
                            <Name>'Staggered Leads</Name>
                        </SubType>
                    </SubTypes>
                </Type>
            </Types>
        </Category>
        """
        elem = etree.fromstring(xml_str)
        category = Category.from_xml(elem)
        
        self.assertEqual(category.number, 15)
        self.assertEqual(category.name, "'Transistor")
        self.assertEqual(len(category.types), 2)
        self.assertEqual(category.types[0].name, "''TO-5")
        self.assertEqual(len(category.types[0].subtypes), 0)
        self.assertEqual(category.types[1].name, "''TO-92")
        self.assertEqual(len(category.types[1].subtypes), 2)

    def test_category_from_xml_empty_types(self):
        """Test Category from_xml parsing with empty types"""
        xml_str = """
        <Category Number="0">
            <Name>'BGA</Name>
            <Types/>
        </Category>
        """
        elem = etree.fromstring(xml_str)
        category = Category.from_xml(elem)
        
        self.assertEqual(category.number, 0)
        self.assertEqual(category.name, "'BGA")
        self.assertEqual(len(category.types), 0)

    def test_category_from_xml_missing_types(self):
        """Test Category from_xml parsing with missing Types element"""
        xml_str = """
        <Category Number="0">
            <Name>'BGA</Name>
        </Category>
        """
        elem = etree.fromstring(xml_str)
        category = Category.from_xml(elem)
        
        self.assertEqual(category.number, 0)
        self.assertEqual(category.name, "'BGA")
        self.assertEqual(len(category.types), 0)

    def test_category_from_xml_defaults(self):
        """Test Category from_xml with missing elements"""
        xml_str = "<Category/>"
        elem = etree.fromstring(xml_str)
        category = Category.from_xml(elem)
        
        self.assertEqual(category.number, 0)
        self.assertEqual(category.name, "")
        self.assertEqual(category.types, [])

    def test_category_roundtrip_with_types(self):
        """Test Category XML roundtrip conversion with types"""
        subtype1 = SubType(0, "'Horizontal")
        subtype2 = SubType(1, "'Vertical")
        type1 = Type(0, "''TO-5", subtypes=[])
        type2 = Type(1, "''TO-220", subtypes=[subtype1, subtype2])
        original = Category(number=15, name="'Transistor", types=[type1, type2])
        elem = original.to_xml()
        restored = Category.from_xml(elem)
        
        self.assertEqual(restored.number, original.number)
        self.assertEqual(restored.name, original.name)
        self.assertEqual(len(restored.types), len(original.types))
        self.assertEqual(restored.types[0].name, original.types[0].name)
        self.assertEqual(len(restored.types[0].subtypes), 0)
        self.assertEqual(restored.types[1].name, original.types[1].name)
        self.assertEqual(len(restored.types[1].subtypes), 2)

    def test_category_roundtrip_empty_types(self):
        """Test Category XML roundtrip conversion with empty types"""
        original = Category(number=0, name="'BGA", types=[])
        elem = original.to_xml()
        restored = Category.from_xml(elem)
        
        self.assertEqual(restored.number, original.number)
        self.assertEqual(restored.name, original.name)
        self.assertEqual(restored.types, [])

    def test_category_special_characters(self):
        """Test Category with special characters in names"""
        category = Category(number=1, name="'Package Length (X) 0.57mm")
        elem = category.to_xml()
        restored = Category.from_xml(elem)
        
        self.assertEqual(restored.name, "'Package Length (X) 0.57mm")

    def test_category_complex_hierarchy(self):
        """Test Category with complex nested hierarchy"""
        # Create a complex structure with multiple types and subtypes
        subtype1 = SubType(0, "SubType1")
        subtype2 = SubType(1, "SubType2")
        subtype3 = SubType(2, "SubType3")
        
        type1 = Type(0, "Type1", subtypes=[])
        type2 = Type(1, "Type2", subtypes=[subtype1, subtype2])
        type3 = Type(2, "Type3", subtypes=[subtype3])
        
        category = Category(number=5, name="Complex", types=[type1, type2, type3])
        elem = category.to_xml()
        restored = Category.from_xml(elem)
        
        self.assertEqual(len(restored.types), 3)
        self.assertEqual(len(restored.types[0].subtypes), 0)
        self.assertEqual(len(restored.types[1].subtypes), 2)
        self.assertEqual(len(restored.types[2].subtypes), 1)


if __name__ == '__main__':
    unittest.main()
