"""Tests for Component Library class."""

import pytest
import tempfile
import os
from lxml import etree
from lxml.builder import E

from DipTraceGenerator.Component.Library import Library, Category, Type, SubType
from DipTraceGenerator.Component.Component import Component
from DipTraceGenerator.Units import Units


class TestSubType:
    """Test the SubType class."""
    
    def test_create_subtype(self):
        """Test creating a SubType."""
        st = SubType(index=0, name="Test SubType")
        assert st.index == 0
        assert st.name == "Test SubType"
    
    def test_subtype_from_xml(self):
        """Test parsing SubType from XML."""
        xml = etree.fromstring('<SubType Index="5"><Name>Female</Name></SubType>')
        st = SubType.from_xml(xml)
        assert st.index == 5
        assert st.name == "Female"
    
    def test_subtype_to_xml(self):
        """Test converting SubType to XML."""
        st = SubType(index=3, name="Male")
        xml = st.to_xml()
        assert xml.get('Index') == '3'
        assert xml.find('Name').text == "Male"
    
    def test_subtype_roundtrip(self):
        """Test SubType XML round-trip conversion."""
        original = SubType(index=10, name="Horizontal")
        xml = original.to_xml()
        parsed = SubType.from_xml(xml)
        assert parsed.index == original.index
        assert parsed.name == original.name


class TestType:
    """Test the Type class."""
    
    def test_create_type(self):
        """Test creating a Type."""
        t = Type(index=0, name="Test Type")
        assert t.index == 0
        assert t.name == "Test Type"
        assert t.subtypes == []
    
    def test_type_with_subtypes(self):
        """Test creating a Type with subtypes."""
        st1 = SubType(index=0, name="Sub1")
        st2 = SubType(index=1, name="Sub2")
        t = Type(index=5, name="Headers", subtypes=[st1, st2])
        assert len(t.subtypes) == 2
        assert t.subtypes[0].name == "Sub1"
        assert t.subtypes[1].name == "Sub2"
    
    def test_type_from_xml_no_subtypes(self):
        """Test parsing Type from XML without subtypes."""
        xml = etree.fromstring(
            '<Type Index="0"><Name>Buzzers</Name><SubTypes/></Type>'
        )
        t = Type.from_xml(xml)
        assert t.index == 0
        assert t.name == "Buzzers"
        assert t.subtypes == []
    
    def test_type_from_xml_with_subtypes(self):
        """Test parsing Type from XML with subtypes."""
        xml = etree.fromstring('''
            <Type Index="12">
                <Name>D-Sub &amp; D-Shaped</Name>
                <SubTypes>
                    <SubType Index="0"><Name>D-Shaped</Name></SubType>
                    <SubType Index="1"><Name>D-Sub</Name></SubType>
                </SubTypes>
            </Type>
        ''')
        t = Type.from_xml(xml)
        assert t.index == 12
        assert t.name == "D-Sub & D-Shaped"
        assert len(t.subtypes) == 2
        assert t.subtypes[0].name == "D-Shaped"
        assert t.subtypes[1].name == "D-Sub"
    
    def test_type_to_xml_no_subtypes(self):
        """Test converting Type to XML without subtypes."""
        t = Type(index=1, name="Microphones")
        xml = t.to_xml()
        assert xml.get('Index') == '1'
        assert xml.find('Name').text == "Microphones"
        assert xml.find('SubTypes') is not None
        assert len(xml.find('SubTypes')) == 0
    
    def test_type_to_xml_with_subtypes(self):
        """Test converting Type to XML with subtypes."""
        st1 = SubType(index=0, name="Female")
        st2 = SubType(index=1, name="Male")
        t = Type(index=22, name="Rectangular - Headers", subtypes=[st1, st2])
        xml = t.to_xml()
        assert xml.get('Index') == '22'
        assert xml.find('Name').text == "Rectangular - Headers"
        subtypes_elem = xml.find('SubTypes')
        assert len(subtypes_elem) == 2
        assert subtypes_elem[0].find('Name').text == "Female"
        assert subtypes_elem[1].find('Name').text == "Male"
    
    def test_type_roundtrip(self):
        """Test Type XML round-trip conversion."""
        st1 = SubType(index=0, name="Test1")
        st2 = SubType(index=1, name="Test2")
        original = Type(index=7, name="Test Type", subtypes=[st1, st2])
        xml = original.to_xml()
        parsed = Type.from_xml(xml)
        assert parsed.index == original.index
        assert parsed.name == original.name
        assert len(parsed.subtypes) == len(original.subtypes)
        assert parsed.subtypes[0].name == original.subtypes[0].name


class TestCategory:
    """Test the Category class."""
    
    def test_create_category(self):
        """Test creating a Category."""
        cat = Category(index=0, name="Test Category")
        assert cat.index == 0
        assert cat.name == "Test Category"
        assert cat.types == []
    
    def test_category_with_types(self):
        """Test creating a Category with types."""
        t1 = Type(index=0, name="Type1")
        t2 = Type(index=1, name="Type2")
        cat = Category(index=5, name="Capacitors", types=[t1, t2])
        assert len(cat.types) == 2
        assert cat.types[0].name == "Type1"
        assert cat.types[1].name == "Type2"
    
    def test_category_from_xml_no_types(self):
        """Test parsing Category from XML without types."""
        xml = etree.fromstring(
            '<Category Index="8"><Name>Others</Name><Types/></Category>'
        )
        cat = Category.from_xml(xml)
        assert cat.index == 8
        assert cat.name == "Others"
        assert cat.types == []
    
    def test_category_from_xml_with_types(self):
        """Test parsing Category from XML with types."""
        xml = etree.fromstring('''
            <Category Index="0">
                <Name>Audio</Name>
                <Types>
                    <Type Index="0"><Name>Buzzers</Name><SubTypes/></Type>
                    <Type Index="1"><Name>Microphones</Name><SubTypes/></Type>
                </Types>
            </Category>
        ''')
        cat = Category.from_xml(xml)
        assert cat.index == 0
        assert cat.name == "Audio"
        assert len(cat.types) == 2
        assert cat.types[0].name == "Buzzers"
        assert cat.types[1].name == "Microphones"
    
    def test_category_to_xml_no_types(self):
        """Test converting Category to XML without types."""
        cat = Category(index=8, name="Others")
        xml = cat.to_xml()
        assert xml.get('Index') == '8'
        assert xml.find('Name').text == "Others"
        assert xml.find('Types') is not None
        assert len(xml.find('Types')) == 0
    
    def test_category_to_xml_with_types(self):
        """Test converting Category to XML with types."""
        t1 = Type(index=0, name="Aluminum")
        t2 = Type(index=1, name="Ceramic")
        cat = Category(index=1, name="Capacitors", types=[t1, t2])
        xml = cat.to_xml()
        assert xml.get('Index') == '1'
        assert xml.find('Name').text == "Capacitors"
        types_elem = xml.find('Types')
        assert len(types_elem) == 2
        assert types_elem[0].find('Name').text == "Aluminum"
        assert types_elem[1].find('Name').text == "Ceramic"
    
    def test_category_roundtrip(self):
        """Test Category XML round-trip conversion."""
        t1 = Type(index=0, name="Test1")
        t2 = Type(index=1, name="Test2")
        original = Category(index=3, name="Test Category", types=[t1, t2])
        xml = original.to_xml()
        parsed = Category.from_xml(xml)
        assert parsed.index == original.index
        assert parsed.name == original.name
        assert len(parsed.types) == len(original.types)
        assert parsed.types[0].name == original.types[0].name


class TestLibrary:
    """Test the Library class."""
    
    def test_create_library(self):
        """Test creating a Library with defaults."""
        lib = Library()
        assert lib.id is None
        assert lib.type == "DipTrace-ComponentLibrary"
        assert lib.name == ""
        assert lib.hint == ""
        assert lib.version == "5.2.0.1"
        assert lib.units == Units.MM
        assert lib.pattern_library_xml is None
        assert lib.categories == []
        assert lib.components == []
    
    def test_create_library_with_values(self):
        """Test creating a Library with specific values."""
        cat = Category(index=0, name="Test")
        comp = Component(id=0)
        lib = Library(
            id=1,
            name="Test Library",
            hint="A test library",
            units=Units.MIL,
            categories=[cat],
            components=[comp]
        )
        assert lib.id == 1
        assert lib.name == "Test Library"
        assert lib.hint == "A test library"
        assert lib.units == Units.MIL
        assert len(lib.categories) == 1
        assert len(lib.components) == 1
    
    def test_library_from_xml_minimal(self):
        """Test parsing Library from minimal XML."""
        xml = etree.fromstring('''
            <Library Type="DipTrace-ComponentLibrary" Name="Test" Version="5.2.0.1" Units="mm"/>
        ''')
        lib = Library.from_xml(xml)
        assert lib.type == "DipTrace-ComponentLibrary"
        assert lib.name == "Test"
        assert lib.version == "5.2.0.1"
        assert lib.units == Units.MM
    
    def test_library_from_xml_with_hint(self):
        """Test parsing Library from XML with hint."""
        xml = etree.fromstring('''
            <Library Type="DipTrace-ComponentLibrary" 
                     Name="IC Interface" 
                     Hint="Integrated Circuit - Interface" 
                     Version="5.2.0.1" 
                     Units="mil"/>
        ''')
        lib = Library.from_xml(xml)
        assert lib.name == "IC Interface"
        assert lib.hint == "Integrated Circuit - Interface"
        assert lib.units == Units.MIL
    
    def test_library_from_xml_validates_type(self):
        """Test that from_xml validates library type."""
        xml = etree.fromstring('''
            <Library Type="DipTrace-PatternLibrary" Name="Test" Version="5.2.0.1" Units="mm"/>
        ''')
        with pytest.raises(ValueError) as excinfo:
            Library.from_xml(xml)
        assert "Invalid library type" in str(excinfo.value)
        assert "DipTrace-PatternLibrary" in str(excinfo.value)
        assert "DipTrace-ComponentLibrary" in str(excinfo.value)
    
    def test_library_from_xml_with_categories(self):
        """Test parsing Library with categories."""
        xml = etree.fromstring('''
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
        lib = Library.from_xml(xml)
        assert len(lib.categories) == 2
        assert lib.categories[0].name == "Audio"
        assert lib.categories[1].name == "Capacitors"
        assert len(lib.categories[0].types) == 1
        assert lib.categories[0].types[0].name == "Buzzers"
    
    def test_library_from_xml_with_components(self):
        """Test parsing Library with components."""
        xml = etree.fromstring('''
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
        lib = Library.from_xml(xml)
        assert len(lib.components) == 2
        assert lib.components[0].id == 0
        assert lib.components[1].id == 1
    
    def test_library_from_xml_with_pattern_library_stub(self):
        """Test parsing Library with nested PatternLibrary (stub)."""
        xml = etree.fromstring('''
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
        lib = Library.from_xml(xml)
        assert lib.pattern_library_xml is not None
        assert lib.pattern_library_xml.get('Type') == 'DipTrace-PatternLibrary'
        # Verify the stub is preserved
        padstyles = lib.pattern_library_xml.find('PadStyles')
        assert padstyles is not None
        assert len(padstyles) == 1
    
    def test_library_to_xml_minimal(self):
        """Test converting Library to XML (minimal)."""
        lib = Library(name="Test Library")
        xml = lib.to_xml()
        assert xml.get('Type') == "DipTrace-ComponentLibrary"
        assert xml.get('Name') == "Test Library"
        assert xml.get('Version') == "5.2.0.1"
        assert xml.get('Units') == "mm"
        assert xml.get('Id') is None
        assert xml.get('Hint') is None
    
    def test_library_to_xml_with_all_attributes(self):
        """Test converting Library to XML with all attributes."""
        lib = Library(
            id=5,
            name="Test Library",
            hint="A test",
            version="5.2.0.1",
            units=Units.MIL
        )
        xml = lib.to_xml()
        assert xml.get('Id') == '5'
        assert xml.get('Type') == "DipTrace-ComponentLibrary"
        assert xml.get('Name') == "Test Library"
        assert xml.get('Hint') == "A test"
        assert xml.get('Version') == "5.2.0.1"
        assert xml.get('Units') == "mil"
    
    def test_library_to_xml_with_categories(self):
        """Test converting Library to XML with categories."""
        cat1 = Category(index=0, name="Audio")
        cat2 = Category(index=1, name="Capacitors")
        lib = Library(name="Test", categories=[cat1, cat2])
        xml = lib.to_xml()
        categories_elem = xml.find('Categories')
        assert categories_elem is not None
        assert len(categories_elem) == 2
        assert categories_elem[0].find('Name').text == "Audio"
        assert categories_elem[1].find('Name').text == "Capacitors"
    
    def test_library_to_xml_with_components(self):
        """Test converting Library to XML with components."""
        comp1 = Component(id=0)
        comp2 = Component(id=1)
        lib = Library(name="Test", components=[comp1, comp2])
        xml = lib.to_xml()
        components_elem = xml.find('Components')
        assert components_elem is not None
        assert len(components_elem) == 2
        assert components_elem[0].get('Id') == '0'
        assert components_elem[1].get('Id') == '1'
    
    def test_library_to_xml_with_pattern_library_stub(self):
        """Test converting Library to XML with PatternLibrary stub."""
        # Create a stub pattern library
        pattern_lib = E.Library(
            Type="DipTrace-PatternLibrary",
            Version="5.2.0.1",
            Units="mil"
        )
        pattern_lib.append(E.PadStyles())
        
        lib = Library(name="Test", pattern_library_xml=pattern_lib)
        xml = lib.to_xml()
        
        # Check that the stub is preserved
        nested_lib = xml.find("Library[@Type='DipTrace-PatternLibrary']")
        assert nested_lib is not None
        assert nested_lib.get('Type') == 'DipTrace-PatternLibrary'
        assert nested_lib.find('PadStyles') is not None
    
    def test_library_roundtrip_minimal(self):
        """Test Library XML round-trip conversion (minimal)."""
        original = Library(name="Test Library", units=Units.MIL)
        xml = original.to_xml()
        parsed = Library.from_xml(xml)
        assert parsed.type == original.type
        assert parsed.name == original.name
        assert parsed.version == original.version
        assert parsed.units == original.units
    
    def test_library_roundtrip_full(self):
        """Test Library XML round-trip conversion (full)."""
        cat = Category(
            index=0,
            name="Audio",
            types=[Type(index=0, name="Buzzers")]
        )
        comp = Component(id=0)
        
        original = Library(
            id=1,
            name="Test Library",
            hint="A test library",
            units=Units.INCH,
            categories=[cat],
            components=[comp]
        )
        
        xml = original.to_xml()
        parsed = Library.from_xml(xml)
        
        assert parsed.id == original.id
        assert parsed.name == original.name
        assert parsed.hint == original.hint
        assert parsed.units == original.units
        assert len(parsed.categories) == 1
        assert parsed.categories[0].name == "Audio"
        assert len(parsed.components) == 1
        assert parsed.components[0].id == 0
    
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
        
        original = Library(
            name="Test",
            pattern_library_xml=pattern_lib
        )
        
        xml = original.to_xml()
        parsed = Library.from_xml(xml)
        
        assert parsed.pattern_library_xml is not None
        assert parsed.pattern_library_xml.get('Type') == 'DipTrace-PatternLibrary'
        padstyles_parsed = parsed.pattern_library_xml.find('PadStyles')
        assert padstyles_parsed is not None
        assert len(padstyles_parsed) == 1
    
    def test_library_save_and_load(self):
        """Test saving Library to file and loading it back."""
        # Create a library with content
        cat = Category(index=0, name="Test Category")
        comp = Component(id=0)
        original = Library(
            id=1,
            name="Test Library",
            hint="A test library",
            units=Units.MIL,
            categories=[cat],
            components=[comp]
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.elixml', delete=False) as f:
            filepath = f.name
        
        try:
            original.save(filepath)
            
            # Load from file
            loaded = Library.load(filepath)
            
            # Verify
            assert loaded.id == original.id
            assert loaded.name == original.name
            assert loaded.hint == original.hint
            assert loaded.units == original.units
            assert len(loaded.categories) == 1
            assert loaded.categories[0].name == "Test Category"
            assert len(loaded.components) == 1
            assert loaded.components[0].id == 0
        finally:
            # Clean up
            if os.path.exists(filepath):
                os.unlink(filepath)
