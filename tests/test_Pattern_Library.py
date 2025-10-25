#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Pattern_Library.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Pattern.Library tests/test_Pattern_Library.py -v --cov-report=term --cov-report=term-missing


from lxml import etree
from pathlib import Path
from unittest import TestCase, main
from tempfile import NamedTemporaryFile
from DipTraceGenerator.Pattern import Library, PadStyle, Pattern, Category, PadType, PadSide
from DipTraceGenerator import Units


class TestLibrary(TestCase):
    """Test the Pattern.Library class."""
    
    def test_create_library_defaults(self):
        """Test creating a Library with default values."""
        library = Library()
        self.assertEqual(library.type, "DipTrace-PatternLibrary")
        self.assertEqual(library.name, "")
        self.assertEqual(library.hint, "")
        self.assertEqual(library.version, "5.2.0.1")
        self.assertEqual(library.units, Units.MM)
        self.assertEqual(library.pad_styles, [])
        self.assertEqual(library.categories, [])
        self.assertEqual(library.patterns, [])
    
    def test_create_library_with_values(self):
        """Test creating a Library with specific values."""
        pad_styles = [
            PadStyle(name="PadT0", pad_type=PadType.Surface, side=PadSide.Top),
        ]
        categories = [
            Category(number=0, name="Resistors"),
        ]
        patterns = [
            Pattern(id=0, name="0603", ref_des="R"),
        ]
        
        library = Library(
            type="DipTrace-PatternLibrary",
            name="Test Library",
            hint="Test library for unit tests",
            version="5.2.0.1",
            units=Units.MM,
            pad_styles=pad_styles,
            categories=categories,
            patterns=patterns,
        )
        
        self.assertEqual(library.type, "DipTrace-PatternLibrary")
        self.assertEqual(library.name, "Test Library")
        self.assertEqual(library.hint, "Test library for unit tests")
        self.assertEqual(library.version, "5.2.0.1")
        self.assertEqual(library.units, Units.MM)
        self.assertEqual(len(library.pad_styles), 1)
        self.assertEqual(len(library.categories), 1)
        self.assertEqual(len(library.patterns), 1)
    
    def test_library_from_xml_basic(self):
        """Test parsing a basic library from XML."""
        xml_str = '''<Library Type="DipTrace-PatternLibrary" Name="Test Library" Hint="Test Hint" Version="5.2.0.1" Units="mm">
                <PadStyles>
                    <PadStyle Name="PadT0" Type="Surface" Side="Top">
                        <MainStack Shape="Rectangle" Width="0.6" Height="2" Corner="25"/>
                    </PadStyle>
                </PadStyles>
                <Categories>
                    <Category Number="0">
                        <Name>Resistors</Name>
                        <Types/>
                    </Category>
                </Categories>
                <Patterns>
                    <Pattern Id="0" RefDes="R" Mounting="SMD" Width="3.2" Height="1.6" Orientation="0" LockTypeChange="N" Type="Free" Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">
                        <Name>0603</Name>
                        <Origin X="0" Y="0" Cross="Y" Circle="N" Common="Hide" Courtyard="Show"/>
                    </Pattern>
                </Patterns>
            </Library>
        '''
        root = etree.fromstring(xml_str)
        library = Library.from_xml(root)
        
        self.assertEqual(library.type, "DipTrace-PatternLibrary")
        self.assertEqual(library.name, "Test Library")
        self.assertEqual(library.hint, "Test Hint")
        self.assertEqual(library.version, "5.2.0.1")
        self.assertEqual(library.units, Units.MM)
        self.assertEqual(len(library.pad_styles), 1)
        self.assertEqual(len(library.categories), 1)
        self.assertEqual(len(library.patterns), 1)
        self.assertEqual(library.pad_styles[0].name, "PadT0")
        self.assertEqual(library.categories[0].name, "Resistors")
        self.assertEqual(library.patterns[0].name, "0603")
    
    def test_library_from_xml_minimal(self):
        """Test parsing a minimal library with no pad styles, categories, or patterns."""
        xml_str = '''<Library Type="DipTrace-PatternLibrary" Name="Empty Library" Hint="" Version="5.2.0.1" Units="mm">
            </Library>
        '''
        root = etree.fromstring(xml_str)
        library = Library.from_xml(root)
        
        self.assertEqual(library.name, "Empty Library")
        self.assertEqual(library.pad_styles, [])
        self.assertEqual(library.categories, [])
        self.assertEqual(library.patterns, [])
    
    def test_library_from_xml_different_units(self):
        """Test parsing libraries with different units."""
        for unit_str, unit_enum in [("mm", Units.MM), ("inch", Units.INCH), ("mil", Units.MIL)]:
            xml_str = f'''<Library Type="DipTrace-PatternLibrary" Name="Test" Hint="" Version="5.2.0.1" Units="{unit_str}">
                </Library>
            '''
            root = etree.fromstring(xml_str)
            library = Library.from_xml(root)
            self.assertEqual(library.units, unit_enum)
    
    def test_library_to_xml_basic(self):
        """Test converting a Library to XML."""
        pad_styles = [
            PadStyle(name="PadT0", pad_type=PadType.Surface, side=PadSide.Top),
        ]
        categories = [
            Category(number=0, name="Resistors"),
        ]
        patterns = [
            Pattern(id=0, name="0603", ref_des="R", mounting="SMD", width=3.2, height=1.6),
        ]
        
        library = Library(
            name="Test Library",
            hint="Test Hint",
            version="5.2.0.1",
            units=Units.MM,
            pad_styles=pad_styles,
            categories=categories,
            patterns=patterns,
        )
        
        xml_element = library.to_xml()
        
        self.assertEqual(xml_element.get("Type"), "DipTrace-PatternLibrary")
        self.assertEqual(xml_element.get("Name"), "Test Library")
        self.assertEqual(xml_element.get("Hint"), "Test Hint")
        self.assertEqual(xml_element.get("Version"), "5.2.0.1")
        self.assertEqual(xml_element.get("Units"), "mm")
        
        pad_styles_elem = xml_element.find("PadStyles")
        self.assertIsNotNone(pad_styles_elem)
        self.assertEqual(len(pad_styles_elem.findall("PadStyle")), 1)
        
        categories_elem = xml_element.find("Categories")
        self.assertIsNotNone(categories_elem)
        self.assertEqual(len(categories_elem.findall("Category")), 1)
        
        patterns_elem = xml_element.find("Patterns")
        self.assertIsNotNone(patterns_elem)
        self.assertEqual(len(patterns_elem.findall("Pattern")), 1)
    
    def test_library_to_xml_empty(self):
        """Test converting an empty Library to XML."""
        library = Library(
            name="Empty Library",
            hint="",
            version="5.2.0.1",
            units=Units.MM,
        )
        
        xml_element = library.to_xml()
        
        self.assertEqual(xml_element.get("Name"), "Empty Library")
        
        # Empty lists should not create elements
        self.assertIsNone(xml_element.find("PadStyles"))
        self.assertIsNone(xml_element.find("Categories"))
        self.assertIsNone(xml_element.find("Patterns"))
    
    def test_library_roundtrip_mm(self):
        """Test roundtrip conversion from XML to Library and back to XML (MM units)."""
        original_xml = '''<Library Type="DipTrace-PatternLibrary" Name="Test Library" Hint="Test Hint" Version="5.2.0.1" Units="mm">
                <PadStyles>
                    <PadStyle Name="PadT0" Type="Surface" Side="Top">
                        <MainStack Shape="Rectangle" Width="0.6" Height="2" Corner="25"/>
                    </PadStyle>
                </PadStyles>
                <Categories>
                    <Category Number="0">
                        <Name>Resistors</Name>
                        <Types/>
                    </Category>
                </Categories>
                <Patterns>
                    <Pattern Id="0" RefDes="R" Mounting="SMD" Width="3.2" Height="1.6" Orientation="0" LockTypeChange="N" Type="Free" Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">
                        <Name>0603</Name>
                        <Origin X="0" Y="0" Cross="Y" Circle="N" Common="Hide" Courtyard="Show"/>
                    </Pattern>
                </Patterns>
            </Library>
        '''
        original_element = etree.fromstring(original_xml)
        library = Library.from_xml(original_element)
        new_element = library.to_xml()
        
        self.assertEqual(new_element.get("Type"), "DipTrace-PatternLibrary")
        self.assertEqual(new_element.get("Name"), "Test Library")
        self.assertEqual(new_element.get("Hint"), "Test Hint")
        self.assertEqual(new_element.get("Version"), "5.2.0.1")
        self.assertEqual(new_element.get("Units"), "mm")
        self.assertEqual(len(new_element.find("PadStyles").findall("PadStyle")), 1)
        self.assertEqual(len(new_element.find("Categories").findall("Category")), 1)
        self.assertEqual(len(new_element.find("Patterns").findall("Pattern")), 1)
    
    def test_library_to_file_and_from_file(self):
        """Test saving Library to file and loading it back."""
        # Create a library
        pad_styles = [
            PadStyle(name="PadT0", pad_type=PadType.Surface, side=PadSide.Top),
        ]
        patterns = [
            Pattern(id=0, name="0603", ref_des="R", mounting="SMD", width=3.2, height=1.6),
        ]
        
        library = Library(
            name="File Test Library",
            hint="Testing file I/O",
            version="5.2.0.1",
            units=Units.MM,
            pad_styles=pad_styles,
            patterns=patterns,
        )
        
        # Save to temporary file
        with NamedTemporaryFile(mode='w', suffix='.libxml', delete=False, encoding='utf-8') as f:
            temp_filename = f.name
        
        try:
            library.to_file(temp_filename)
            
            # Load from file
            loaded_library = Library.from_file(temp_filename)
            
            self.assertEqual(loaded_library.name, "File Test Library")
            self.assertEqual(loaded_library.hint, "Testing file I/O")
            self.assertEqual(loaded_library.version, "5.2.0.1")
            self.assertEqual(loaded_library.units, Units.MM)
            self.assertEqual(len(loaded_library.pad_styles), 1)
            self.assertEqual(len(loaded_library.patterns), 1)
            self.assertEqual(loaded_library.pad_styles[0].name, "PadT0")
            self.assertEqual(loaded_library.patterns[0].name, "0603")
        finally:
            # Clean up
            Path(temp_filename).unlink(missing_ok=True)
    
    def test_library_multiple_pad_styles(self):
        """Test library with multiple pad styles."""
        pad_styles = [
            PadStyle(name="PadT0", pad_type=PadType.Surface, side=PadSide.Top),
            PadStyle(name="PadT1", pad_type=PadType.Surface, side=PadSide.Top),
            PadStyle(name="PadB0", pad_type=PadType.Surface, side=PadSide.Bottom),
        ]
        
        library = Library(
            name="Multi PadStyle Library",
            pad_styles=pad_styles,
        )
        
        self.assertEqual(len(library.pad_styles), 3)
        
        xml_element = library.to_xml()
        pad_styles_elem = xml_element.find("PadStyles")
        self.assertEqual(len(pad_styles_elem.findall("PadStyle")), 3)
    
    def test_library_multiple_patterns(self):
        """Test library with multiple patterns."""
        patterns = [
            Pattern(id=0, name="0603", ref_des="R"),
            Pattern(id=1, name="0805", ref_des="R"),
            Pattern(id=2, name="1206", ref_des="R"),
        ]
        
        library = Library(
            name="Multi Pattern Library",
            patterns=patterns,
        )
        
        self.assertEqual(len(library.patterns), 3)
        
        xml_element = library.to_xml()
        patterns_elem = xml_element.find("Patterns")
        self.assertEqual(len(patterns_elem.findall("Pattern")), 3)
    
    def test_library_multiple_categories(self):
        """Test library with multiple categories."""
        categories = [
            Category(number=0, name="Resistors"),
            Category(number=1, name="Capacitors"),
            Category(number=2, name="ICs"),
        ]
        
        library = Library(
            name="Multi Category Library",
            categories=categories,
        )
        
        self.assertEqual(len(library.categories), 3)
        
        xml_element = library.to_xml()
        categories_elem = xml_element.find("Categories")
        self.assertEqual(len(categories_elem.findall("Category")), 3)
    
    def test_library_from_real_sample_file_mm(self):
        """Test parsing a real sample library file in MM units."""
        # Get path relative to this test file
        test_dir = Path(__file__).parent
        sample_file = test_dir / "samples" / "general-nonipc-mm.libxml"
        
        # Check if file exists
        if not sample_file.exists():
            self.skipTest(f"Sample file {sample_file} not found")
        
        # Load the library
        library = Library.from_file(sample_file)
        
        # Verify basic properties
        self.assertEqual(library.type, "DipTrace-PatternLibrary")
        self.assertEqual(library.version, "5.2.0.1")
        self.assertEqual(library.units, Units.MM)  # Original file units
        
        # Verify it has content
        self.assertGreater(len(library.pad_styles), 0, "Library should have pad styles")
        self.assertGreater(len(library.patterns), 0, "Library should have patterns")
        
        print(f"\nSuccessfully loaded real sample library (MM):")
        print(f"  Name: {library.name}")
        print(f"  Pad Styles: {len(library.pad_styles)}")
        print(f"  Categories: {len(library.categories)}")
        print(f"  Patterns: {len(library.patterns)}")
    
    def test_library_from_real_sample_file_inch(self):
        """Test parsing a real sample library file in INCH units."""
        # Get path relative to this test file
        test_dir = Path(__file__).parent
        sample_file = test_dir / "samples" / "general-nonipc-inch.libxml"
        
        # Check if file exists
        if not sample_file.exists():
            self.skipTest(f"Sample file {sample_file} not found")
        
        # Load the library
        library = Library.from_file(sample_file)
        
        # Verify basic properties
        self.assertEqual(library.type, "DipTrace-PatternLibrary")
        self.assertEqual(library.version, "5.2.0.1")
        self.assertEqual(library.units, Units.INCH)  # Original file units
        
        # Verify it has content
        self.assertGreater(len(library.pad_styles), 0, "Library should have pad styles")
        self.assertGreater(len(library.patterns), 0, "Library should have patterns")
        
        print(f"\nSuccessfully loaded real sample library (INCH):")
        print(f"  Name: {library.name}")
        print(f"  Pad Styles: {len(library.pad_styles)}")
        print(f"  Categories: {len(library.categories)}")
        print(f"  Patterns: {len(library.patterns)}")
    
    def test_library_from_real_sample_file_mil(self):
        """Test parsing a real sample library file in MIL units."""
        # Get path relative to this test file
        test_dir = Path(__file__).parent
        sample_file = test_dir / "samples" / "general-nonipc-mil.libxml"
        
        # Check if file exists
        if not sample_file.exists():
            self.skipTest(f"Sample file {sample_file} not found")
        
        # Load the library
        library = Library.from_file(sample_file)
        
        # Verify basic properties
        self.assertEqual(library.type, "DipTrace-PatternLibrary")
        self.assertEqual(library.version, "5.2.0.1")
        self.assertEqual(library.units, Units.MIL)  # Original file units
        
        # Verify it has content
        self.assertGreater(len(library.pad_styles), 0, "Library should have pad styles")
        self.assertGreater(len(library.patterns), 0, "Library should have patterns")
        
        print(f"\nSuccessfully loaded real sample library (MIL):")
        print(f"  Name: {library.name}")
        print(f"  Pad Styles: {len(library.pad_styles)}")
        print(f"  Categories: {len(library.categories)}")
        print(f"  Patterns: {len(library.patterns)}")
    
    def test_library_unit_conversion_roundtrip(self):
        """Test that libraries can be loaded in one unit and saved in another."""
        # Get path relative to this test file
        test_dir = Path(__file__).parent
        sample_file_mm = test_dir / "samples" / "general-nonipc-mm.libxml"
        
        # Check if file exists
        if not sample_file_mm.exists():
            self.skipTest(f"Sample file {sample_file_mm} not found")
        
        # Load MM library (internally stored in MM)
        library_mm = Library.from_file(sample_file_mm)
        
        # Save as INCH
        with NamedTemporaryFile(mode='w', suffix='.libxml', delete=False) as f:
            temp_inch_file = f.name
        
        try:
            library_mm.to_file(temp_inch_file, units=Units.INCH)
            
            # Load the INCH file (should convert INCH to MM internally)
            library_inch = Library.from_file(temp_inch_file)
            
            # Verify units are preserved from file
            self.assertEqual(library_inch.units, Units.INCH)
            
            # Verify same number of elements
            self.assertEqual(len(library_inch.pad_styles), len(library_mm.pad_styles))
            self.assertEqual(len(library_inch.patterns), len(library_mm.patterns))
            self.assertEqual(len(library_inch.categories), len(library_mm.categories))
            
            # Now save the INCH-loaded library as MIL
            with NamedTemporaryFile(mode='w', suffix='.libxml', delete=False) as f:
                temp_mil_file = f.name
            
            try:
                library_inch.to_file(temp_mil_file, units=Units.MIL)
                
                # Load the MIL file
                library_mil = Library.from_file(temp_mil_file)
                
                # Verify units
                self.assertEqual(library_mil.units, Units.MIL)
                
                # Verify same number of elements (data should be consistent across conversions)
                self.assertEqual(len(library_mil.pad_styles), len(library_mm.pad_styles))
                self.assertEqual(len(library_mil.patterns), len(library_mm.patterns))
                
                print(f"\nUnit conversion roundtrip successful:")
                print(f"  MM → INCH → MIL")
                print(f"  Patterns preserved: {len(library_mil.patterns)}")
                
            finally:
                if Path(temp_mil_file).exists():
                    Path(temp_mil_file).unlink()
        finally:
            if Path(temp_inch_file).exists():
                Path(temp_inch_file).unlink()
    
    def test_library_from_file_empty_path(self):
        """Test that from_file raises TypeError for empty path."""
        with self.assertRaises(TypeError) as context:
            Library.from_file("")
        self.assertIn("Filename must be a non-empty string", str(context.exception))
    
    def test_library_to_file_empty_path(self):
        """Test that to_file raises TypeError for empty path."""
        library = Library(name="Test")
        with self.assertRaises(TypeError) as context:
            library.to_file("")
        self.assertIn("Filename must be a non-empty string", str(context.exception))
    
    def test_library_to_file_with_path_object(self):
        """Test that to_file works with Path objects."""
        library = Library(
            name="Path Test",
            patterns=[Pattern(id=0, name="Test", ref_des="U")],
        )
        
        with NamedTemporaryFile(mode='w', suffix='.libxml', delete=False) as f:
            temp_filename = Path(f.name)
        
        try:
            # Test saving with Path object
            library.to_file(temp_filename, units=Units.MM)
            
            # Verify file was created and can be loaded
            self.assertTrue(temp_filename.exists())
            loaded_library = Library.from_file(temp_filename)
            self.assertEqual(loaded_library.name, "Path Test")
            self.assertEqual(len(loaded_library.patterns), 1)
        finally:
            if temp_filename.exists():
                temp_filename.unlink()


if __name__ == '__main__':
    main()

