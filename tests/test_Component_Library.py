#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Library.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Library tests/test_Component_Library.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from tempfile import NamedTemporaryFile
from pathlib import Path
from lxml import etree
from lxml.builder import E
from DipTraceGenerator.Component import Library as ComponentLibrary, Category, Type, SubType, Component
from DipTraceGenerator import Units


class TestSubType(TestCase):
    """Test the SubType class."""
    
    def test_create_subtype(self):
        """Test creating a SubType."""
        st = SubType(index=0, name="Test SubType")
        self.assertEqual(st.index, 0)
        self.assertEqual(st.name, "Test SubType")
    
    def test_subtype_from_xml(self):
        """Test parsing SubType from XML."""
        xml_element = etree.fromstring('<SubType Index="5"><Name>Female</Name></SubType>')
        st = SubType.from_xml(xml_element)
        self.assertEqual(st.index, 5)
        self.assertEqual(st.name, "Female")
    
    def test_subtype_to_xml(self):
        """Test converting SubType to XML."""
        st = SubType(index=3, name="Male")
        xml_element = st.to_xml()
        self.assertEqual(xml_element.get('Index'), '3')
        self.assertEqual(xml_element.find('Name').text, "Male")
    
    def test_subtype_roundtrip(self):
        """Test SubType XML round-trip conversion."""
        original = SubType(index=10, name="Horizontal")
        xml_element = original.to_xml()
        parsed = SubType.from_xml(xml_element)
        self.assertEqual(parsed.index, original.index)
        self.assertEqual(parsed.name, original.name)


class TestType(TestCase):
    """Test the Type class."""
    
    def test_create_type(self):
        """Test creating a Type."""
        t = Type(index=0, name="Test Type")
        self.assertEqual(t.index, 0)
        self.assertEqual(t.name, "Test Type")
        self.assertEqual(t.subtypes, [])
    
    def test_type_with_subtypes(self):
        """Test creating a Type with subtypes."""
        st1 = SubType(index=0, name="Sub1")
        st2 = SubType(index=1, name="Sub2")
        t = Type(index=5, name="Headers", subtypes=[st1, st2])
        self.assertEqual(len(t.subtypes), 2)
        self.assertEqual(t.subtypes[0].name, "Sub1")
        self.assertEqual(t.subtypes[1].name, "Sub2")
    
    def test_type_from_xml_no_subtypes(self):
        """Test parsing Type from XML without subtypes."""
        xml_element = etree.fromstring(
            '<Type Index="0"><Name>Buzzers</Name><SubTypes/></Type>'
        )
        t = Type.from_xml(xml_element)
        self.assertEqual(t.index, 0)
        self.assertEqual(t.name, "Buzzers")
        self.assertEqual(t.subtypes, [])
    
    def test_type_from_xml_with_subtypes(self):
        """Test parsing Type from XML with subtypes."""
        xml_element = etree.fromstring('''
            <Type Index="12">
                <Name>D-Sub &amp; D-Shaped</Name>
                <SubTypes>
                    <SubType Index="0"><Name>D-Shaped</Name></SubType>
                    <SubType Index="1"><Name>D-Sub</Name></SubType>
                </SubTypes>
            </Type>
        ''')
        t = Type.from_xml(xml_element)
        self.assertEqual(t.index, 12)
        self.assertEqual(t.name, "D-Sub & D-Shaped")
        self.assertEqual(len(t.subtypes), 2)
        self.assertEqual(t.subtypes[0].name, "D-Shaped")
        self.assertEqual(t.subtypes[1].name, "D-Sub")
    
    def test_type_to_xml_no_subtypes(self):
        """Test converting Type to XML without subtypes."""
        t = Type(index=1, name="Microphones")
        xml_element = t.to_xml()
        self.assertEqual(xml_element.get('Index'), '1')
        self.assertEqual(xml_element.find('Name').text, "Microphones")
        self.assertIsNotNone(xml_element.find('SubTypes'))
        self.assertEqual(len(xml_element.find('SubTypes')), 0)
    
    def test_type_to_xml_with_subtypes(self):
        """Test converting Type to XML with subtypes."""
        st1 = SubType(index=0, name="Female")
        st2 = SubType(index=1, name="Male")
        t = Type(index=22, name="Rectangular - Headers", subtypes=[st1, st2])
        xml_element = t.to_xml()
        self.assertEqual(xml_element.get('Index'), '22')
        self.assertEqual(xml_element.find('Name').text, "Rectangular - Headers")
        subtypes_elem = xml_element.find('SubTypes')
        self.assertEqual(len(subtypes_elem), 2)
        self.assertEqual(subtypes_elem[0].find('Name').text, "Female")
        self.assertEqual(subtypes_elem[1].find('Name').text, "Male")
    
    def test_type_roundtrip(self):
        """Test Type XML round-trip conversion."""
        st1 = SubType(index=0, name="Test1")
        st2 = SubType(index=1, name="Test2")
        original = Type(index=7, name="Test Type", subtypes=[st1, st2])
        xml_element = original.to_xml()
        parsed = Type.from_xml(xml_element)
        self.assertEqual(parsed.index, original.index)
        self.assertEqual(parsed.name, original.name)
        self.assertEqual(len(parsed.subtypes), len(original.subtypes))
        self.assertEqual(parsed.subtypes[0].name, original.subtypes[0].name)


class TestCategory(TestCase):
    """Test the Category class."""
    
    def test_create_category(self):
        """Test creating a Category."""
        cat = Category(index=0, name="Test Category")
        self.assertEqual(cat.index, 0)
        self.assertEqual(cat.name, "Test Category")
        self.assertEqual(cat.types, [])
    
    def test_category_with_types(self):
        """Test creating a Category with types."""
        t1 = Type(index=0, name="Type1")
        t2 = Type(index=1, name="Type2")
        cat = Category(index=5, name="Capacitors", types=[t1, t2])
        self.assertEqual(len(cat.types), 2)
        self.assertEqual(cat.types[0].name, "Type1")
        self.assertEqual(cat.types[1].name, "Type2")
    
    def test_category_from_xml_no_types(self):
        """Test parsing Category from XML without types."""
        xml_element = etree.fromstring(
            '<Category Index="8"><Name>Others</Name><Types/></Category>'
        )
        cat = Category.from_xml(xml_element)
        self.assertEqual(cat.index, 8)
        self.assertEqual(cat.name, "Others")
        self.assertEqual(cat.types, [])
    
    def test_category_from_xml_with_types(self):
        """Test parsing Category from XML with types."""
        xml_element = etree.fromstring('''
            <Category Index="0">
                <Name>Audio</Name>
                <Types>
                    <Type Index="0"><Name>Buzzers</Name><SubTypes/></Type>
                    <Type Index="1"><Name>Microphones</Name><SubTypes/></Type>
                </Types>
            </Category>
        ''')
        cat = Category.from_xml(xml_element)
        self.assertEqual(cat.index, 0)
        self.assertEqual(cat.name, "Audio")
        self.assertEqual(len(cat.types), 2)
        self.assertEqual(cat.types[0].name, "Buzzers")
        self.assertEqual(cat.types[1].name, "Microphones")
    
    def test_category_to_xml_no_types(self):
        """Test converting Category to XML without types."""
        cat = Category(index=8, name="Others")
        xml_element = cat.to_xml()
        self.assertEqual(xml_element.get('Index'), '8')
        self.assertEqual(xml_element.find('Name').text, "Others")
        self.assertIsNotNone(xml_element.find('Types'))
        self.assertEqual(len(xml_element.find('Types')), 0)
    
    def test_category_to_xml_with_types(self):
        """Test converting Category to XML with types."""
        t1 = Type(index=0, name="Aluminum")
        t2 = Type(index=1, name="Ceramic")
        cat = Category(index=1, name="Capacitors", types=[t1, t2])
        xml_element = cat.to_xml()
        self.assertEqual(xml_element.get('Index'), '1')
        self.assertEqual(xml_element.find('Name').text, "Capacitors")
        types_elem = xml_element.find('Types')
        self.assertEqual(len(types_elem), 2)
        self.assertEqual(types_elem[0].find('Name').text, "Aluminum")
        self.assertEqual(types_elem[1].find('Name').text, "Ceramic")
    
    def test_category_roundtrip(self):
        """Test Category XML round-trip conversion."""
        t1 = Type(index=0, name="Test1")
        t2 = Type(index=1, name="Test2")
        original = Category(index=3, name="Test Category", types=[t1, t2])
        xml_element = original.to_xml()
        parsed = Category.from_xml(xml_element)
        self.assertEqual(parsed.index, original.index)
        self.assertEqual(parsed.name, original.name)
        self.assertEqual(len(parsed.types), len(original.types))
        self.assertEqual(parsed.types[0].name, original.types[0].name)


class TestLibrary(TestCase):
    """Test the Library class."""
    
    def test_create_library(self):
        """Test creating a Library with defaults."""
        lib = ComponentLibrary()
        self.assertIsNone(lib.id)
        self.assertEqual(lib.type, "DipTrace-ComponentLibrary")
        self.assertEqual(lib.name, "")
        self.assertEqual(lib.hint, "")
        self.assertEqual(lib.version, "5.2.0.1")
        self.assertEqual(lib.units, Units.MM)
        self.assertIsNone(lib.pattern_library_xml)
        self.assertEqual(lib.categories, [])
        self.assertEqual(lib.components, [])
    
    def test_create_library_with_values(self):
        """Test creating a Library with specific values."""
        cat = Category(index=0, name="Test")
        comp = Component(id=0)
        lib = ComponentLibrary(
            id=1,
            name="Test Library",
            hint="A test library",
            units=Units.MIL,
            categories=[cat],
            components=[comp]
        )
        self.assertEqual(lib.id, 1)
        self.assertEqual(lib.name, "Test Library")
        self.assertEqual(lib.hint, "A test library")
        self.assertEqual(lib.units, Units.MIL)
        self.assertEqual(len(lib.categories), 1)
        self.assertEqual(len(lib.components), 1)
    
    def test_library_from_xml_minimal(self):
        """Test parsing Library from minimal XML."""
        xml_element = etree.fromstring('''
            <Library Type="DipTrace-ComponentLibrary" Name="Test" Version="5.2.0.1" Units="mm"/>
        ''')
        lib = ComponentLibrary.from_xml(xml_element)
        self.assertEqual(lib.type, "DipTrace-ComponentLibrary")
        self.assertEqual(lib.name, "Test")
        self.assertEqual(lib.version, "5.2.0.1")
        self.assertEqual(lib.units, Units.MM)
    
    def test_library_from_xml_with_hint(self):
        """Test parsing Library from XML with hint."""
        xml_element = etree.fromstring('''
            <Library Type="DipTrace-ComponentLibrary" 
                     Name="IC Interface" 
                     Hint="Integrated Circuit - Interface" 
                     Version="5.2.0.1" 
                     Units="mil"/>
        ''')
        lib = ComponentLibrary.from_xml(xml_element)
        self.assertEqual(lib.name, "IC Interface")
        self.assertEqual(lib.hint, "Integrated Circuit - Interface")
        self.assertEqual(lib.units, Units.MIL)
    
    def test_library_from_xml_validates_type(self):
        """Test that from_xml validates library type."""
        xml_element = etree.fromstring('''
            <Library Type="DipTrace-PatternLibrary" Name="Test" Version="5.2.0.1" Units="mm"/>
        ''')
        with self.assertRaises(ValueError) as context:
            ComponentLibrary.from_xml(xml_element)
        self.assertIn("Invalid library type", str(context.exception))
        self.assertIn("DipTrace-PatternLibrary", str(context.exception))
        self.assertIn("DipTrace-ComponentLibrary", str(context.exception))
    
    def test_library_from_xml_with_categories(self):
        """Test parsing Library with categories."""
        xml_element = etree.fromstring('''
            <Library Type="DipTrace-ComponentLibrary" Name="Test" Version="5.2.0.1" Units="mm">
                <Categories>
                    <Category Index="0">
                        <Name>Audio</Name>
                        <Types>
                            <Type Index="0"><Name>Buzzers</Name><SubTypes/></Type>
                        </Types>
                    </Category>
                    <Category Index="1">
                        <Name>Capacitors</Name>
                        <Types/>
                    </Category>
                </Categories>
            </Library>
        ''')
        lib = ComponentLibrary.from_xml(xml_element)
        self.assertEqual(len(lib.categories), 2)
        self.assertEqual(lib.categories[0].name, "Audio")
        self.assertEqual(lib.categories[1].name, "Capacitors")
        self.assertEqual(len(lib.categories[0].types), 1)
        self.assertEqual(lib.categories[0].types[0].name, "Buzzers")
    
    def test_library_from_xml_with_components(self):
        """Test parsing Library with components."""
        xml_element = etree.fromstring('''
            <Library Type="DipTrace-ComponentLibrary" Name="Test" Version="5.2.0.1" Units="mm">
                <Components>
                    <Component Id="0">
                        <RefDes>U</RefDes>
                    </Component>
                    <Component Id="1">
                        <RefDes>R</RefDes>
                    </Component>
                </Components>
            </Library>
        ''')
        lib = ComponentLibrary.from_xml(xml_element)
        self.assertEqual(len(lib.components), 2)
        self.assertEqual(lib.components[0].id, 0)
        self.assertEqual(lib.components[1].id, 1)
    
    def test_library_from_xml_with_pattern_library_stub(self):
        """Test parsing Library with nested PatternLibrary (stub)."""
        xml_element = etree.fromstring('''
            <Library Type="DipTrace-ComponentLibrary" Name="Test" Version="5.2.0.1" Units="mil">
                <Library Type="DipTrace-PatternLibrary" Version="5.2.0.1" Units="mil">
                    <PadStyles>
                        <PadStyle Name="Test"/>
                    </PadStyles>
                </Library>
                <Categories/>
                <Components/>
            </Library>
        ''')
        lib = ComponentLibrary.from_xml(xml_element)
        self.assertIsNotNone(lib.pattern_library_xml)
        self.assertEqual(lib.pattern_library_xml.get('Type'), 'DipTrace-PatternLibrary')
        # Verify the stub is preserved
        padstyles = lib.pattern_library_xml.find('PadStyles')
        self.assertIsNotNone(padstyles)
        self.assertEqual(len(padstyles), 1)
    
    def test_library_to_xml_minimal(self):
        """Test converting Library to XML (minimal)."""
        lib = ComponentLibrary(name="Test Library")
        xml_element = lib.to_xml()
        self.assertEqual(xml_element.get('Type'), "DipTrace-ComponentLibrary")
        self.assertEqual(xml_element.get('Name'), "Test Library")
        self.assertEqual(xml_element.get('Version'), "5.2.0.1")
        self.assertEqual(xml_element.get('Units'), "mm")
        self.assertIsNone(xml_element.get('Id'))
        self.assertIsNone(xml_element.get('Hint'))
    
    def test_library_to_xml_with_all_attributes(self):
        """Test converting Library to XML with all attributes."""
        lib = ComponentLibrary(
            id=5,
            name="Test Library",
            hint="A test",
            version="5.2.0.1",
            units=Units.MIL
        )
        xml_element = lib.to_xml()
        self.assertEqual(xml_element.get('Id'), '5')
        self.assertEqual(xml_element.get('Type'), "DipTrace-ComponentLibrary")
        self.assertEqual(xml_element.get('Name'), "Test Library")
        self.assertEqual(xml_element.get('Hint'), "A test")
        self.assertEqual(xml_element.get('Version'), "5.2.0.1")
        self.assertEqual(xml_element.get('Units'), "mil")
    
    def test_library_to_xml_with_categories(self):
        """Test converting Library to XML with categories."""
        cat1 = Category(index=0, name="Audio")
        cat2 = Category(index=1, name="Capacitors")
        lib = ComponentLibrary(name="Test", categories=[cat1, cat2])
        xml_element = lib.to_xml()
        categories_elem = xml_element.find('Categories')
        self.assertIsNotNone(categories_elem)
        self.assertEqual(len(categories_elem), 2)
        self.assertEqual(categories_elem[0].find('Name').text, "Audio")
        self.assertEqual(categories_elem[1].find('Name').text, "Capacitors")
    
    def test_library_to_xml_with_components(self):
        """Test converting Library to XML with components."""
        comp1 = Component(id=0)
        comp2 = Component(id=1)
        lib = ComponentLibrary(name="Test", components=[comp1, comp2])
        xml_element = lib.to_xml()
        components_elem = xml_element.find('Components')
        self.assertIsNotNone(components_elem)
        self.assertEqual(len(components_elem), 2)
        self.assertEqual(components_elem[0].get('Id'), '0')
        self.assertEqual(components_elem[1].get('Id'), '1')
    
    def test_library_to_xml_with_pattern_library_stub(self):
        """Test converting Library to XML with PatternLibrary stub."""
        # Create a stub pattern library
        pattern_lib = E.Library(
            Type="DipTrace-PatternLibrary",
            Version="5.2.0.1",
            Units="mil"
        )
        pattern_lib.append(E.PadStyles())
        
        lib = ComponentLibrary(name="Test", pattern_library_xml=pattern_lib)
        xml_element = lib.to_xml()
        
        # Check that the stub is preserved
        nested_lib = xml_element.find("Library[@Type='DipTrace-PatternLibrary']")
        self.assertIsNotNone(nested_lib)
        self.assertEqual(nested_lib.get('Type'), 'DipTrace-PatternLibrary')
        self.assertIsNotNone(nested_lib.find('PadStyles'))
    
    def test_library_roundtrip_minimal(self):
        """Test Library XML round-trip conversion (minimal)."""
        original = ComponentLibrary(name="Test Library", units=Units.MIL)
        xml_element = original.to_xml()
        parsed = ComponentLibrary.from_xml(xml_element)
        self.assertEqual(parsed.type, original.type)
        self.assertEqual(parsed.name, original.name)
        self.assertEqual(parsed.version, original.version)
        self.assertEqual(parsed.units, original.units)
    
    def test_library_roundtrip_full(self):
        """Test Library XML round-trip conversion (full)."""
        cat = Category(
            index=0,
            name="Audio",
            types=[Type(index=0, name="Buzzers")]
        )
        comp = Component(id=0)
        
        original = ComponentLibrary(
            id=1,
            name="Test Library",
            hint="A test library",
            units=Units.INCH,
            categories=[cat],
            components=[comp]
        )
        
        xml_element = original.to_xml()
        parsed = ComponentLibrary.from_xml(xml_element)
        
        self.assertEqual(parsed.id, original.id)
        self.assertEqual(parsed.name, original.name)
        self.assertEqual(parsed.hint, original.hint)
        self.assertEqual(parsed.units, original.units)
        self.assertEqual(len(parsed.categories), 1)
        self.assertEqual(parsed.categories[0].name, "Audio")
        self.assertEqual(len(parsed.components), 1)
        self.assertEqual(parsed.components[0].id, 0)
    
    def test_library_roundtrip_with_pattern_stub(self):
        """Test Library XML round-trip with PatternLibrary stub."""
        # Create a stub with nested content
        pattern_lib = E.Library(
            Type="DipTrace-PatternLibrary",
            Version="5.2.0.1",
            Units="mil"
        )
        padstyles = E.PadStyles()
        padstyles.append(E.PadStyle(Name="TestPad"))
        pattern_lib.append(padstyles)
        
        original = ComponentLibrary(
            name="Test",
            pattern_library_xml=pattern_lib
        )
        
        xml_element = original.to_xml()
        parsed = ComponentLibrary.from_xml(xml_element)
        
        self.assertIsNotNone(parsed.pattern_library_xml)
        self.assertEqual(parsed.pattern_library_xml.get('Type'), 'DipTrace-PatternLibrary')
        padstyles_parsed = parsed.pattern_library_xml.find('PadStyles')
        self.assertIsNotNone(padstyles_parsed)
        self.assertEqual(len(padstyles_parsed), 1)
    
    def test_library_save_and_load(self):
        """Test saving Library to file and loading it back."""
        # Create a library with content
        cat = Category(index=0, name="Test Category")
        comp = Component(id=0)
        original = ComponentLibrary(
            id=1,
            name="Test Library",
            hint="A test library",
            units=Units.MIL,
            categories=[cat],
            components=[comp]
        )
        
        # Save to temporary file
        with NamedTemporaryFile(mode='w', suffix='.elixml', delete=False) as f:
            filepath = f.name
        
        try:
            original.save(filepath)
            
            # Load from file
            loaded = ComponentLibrary.load(filepath)
            
            # Verify
            self.assertEqual(loaded.id, original.id)
            self.assertEqual(loaded.name, original.name)
            self.assertEqual(loaded.hint, original.hint)
            self.assertEqual(loaded.units, original.units)
            self.assertEqual(len(loaded.categories), 1)
            self.assertEqual(loaded.categories[0].name, "Test Category")
            self.assertEqual(len(loaded.components), 1)
            self.assertEqual(loaded.components[0].id, 0)
        finally:
            # Clean up
            Path(filepath).unlink(missing_ok=True)
            

if __name__ == "__main__":
    main()
