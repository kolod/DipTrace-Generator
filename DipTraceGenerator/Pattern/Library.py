#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Library class for DipTrace Pattern Library."""


from typing import Union
from pathlib import Path
from ..xmltools import dataclass, field, etree, E
from ..Units import Units
from .PadStyle import PadStyle
from .Pattern import Pattern
from .Category import Category


@dataclass
class Library:
    """
    Represents a DipTrace Pattern Library file.
    
    A Pattern Library contains:
    - Library metadata (name, hint, version)
    - Pad styles used by patterns
    - Categories for organizing patterns
    - Pattern definitions (PCB footprints)
    
    Note: All dimensions are stored internally in millimeters (MM).
    When loading from XML, values are converted from the file's units to MM.
    When saving to XML, values are converted from MM to the specified output units
    and units are stored in the object.
    
    Attributes:
        type: Library type, always "DipTrace-PatternLibrary".
        name: Library name displayed on the Library panel.
        hint: Library hint text displayed on the Library panel.
        version: Version of the library file format.
        units: Measurement units to use when saving (mm, inch, mil). 
               Note: Internal storage is always in MM regardless of this setting.
        pad_styles: List of pad styles defined in the library.
        categories: List of categories for organizing patterns.
        patterns: List of patterns (PCB footprints) in the library.
    """
    
    type: str = "DipTrace-PatternLibrary"
    name: str = ""
    hint: str = ""
    version: str = "5.2.0.1"
    units: Units = Units.MM
    pad_styles: list[PadStyle] = field(default_factory=list)
    categories: list[Category] = field(default_factory=list)
    patterns: list[Pattern] = field(default_factory=list)
    
    @classmethod
    def from_xml(cls, element: etree._Element) -> 'Library':
        """
        Parse Library from XML element.
        
        Reads values from the file in the file's units and converts them to internal MM representation.
        The units attribute is preserved to remember the original file's units.
        
        Args:
            element: XML element representing the Library (root element).
            
        Returns:
            Library instance with all dimensions in MM.
        """
        # Parse main attributes
        lib_type = element.get("Type", "DipTrace-PatternLibrary")
        name = element.get("Name", "")
        hint = element.get("Hint", "")
        version = element.get("Version", "5.2.0.1")
        units = Units(element.get("Units", "mm"))
        
        # Parse PadStyles (convert from file_units to MM)
        pad_styles = []
        pad_styles_elem = element.find("PadStyles")
        if pad_styles_elem is not None:
            for pad_style_elem in pad_styles_elem.findall("PadStyle"):
                pad_styles.append(PadStyle.from_xml(pad_style_elem, units))
        
        # Parse Categories
        categories = []
        categories_elem = element.find("Categories")
        if categories_elem is not None:
            for category_elem in categories_elem.findall("Category"):
                categories.append(Category.from_xml(category_elem))
        
        # Parse Patterns (convert from file_units to MM)
        patterns = []
        patterns_elem = element.find("Patterns")
        if patterns_elem is not None:
            for pattern_elem in patterns_elem.findall("Pattern"):
                patterns.append(Pattern.from_xml(pattern_elem, units))
        
        return cls(
            type=lib_type,
            name=name,
            hint=hint,
            version=version,
            units=units,  # Remember original file units!
            pad_styles=pad_styles,
            categories=categories,
            patterns=patterns,
        )
    
    @classmethod
    def from_file(cls, filename: Union[Path, str]) -> 'Library':
        """
        Load Library from XML file.
        
        Args:
            filename: Path to the library XML file.
            
        Returns:
            Library instance.
        """

        # Determine path string
        if isinstance(filename, str):
            path = filename
        elif isinstance(filename, Path):
            path = str(filename)
        if not path:
            raise TypeError("Filename must be a non-empty string or Path.")
        
        # Generate XML tree and parse
        tree = etree.parse(path)
        root = tree.getroot()
        return cls.from_xml(root)
    
    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Library instance to XML element.
        
        Converts internal MM values to the specified output units.
        
        Args:
            units: Target units for the output file (MM, INCH, or MIL). Defaults to MM.
        
        Returns:
            etree._Element: XML element representing the Library (root element).
        """

        # Store used units in object
        self.units = units

        # Build attributes dictionary
        attribs = {
            "Type": self.type,
            "Name": self.name,
            "Hint": self.hint,
            "Version": self.version,
            "Units": self.units.value,
        }
        
        # Create Library element
        library_elem = E("Library", attribs)
        
        # Add PadStyles (convert from MM to target units)
        if self.pad_styles:
            pad_styles_elem = E("PadStyles")
            for pad_style in self.pad_styles:
                pad_styles_elem.append(pad_style.to_xml(self.units))
            library_elem.append(pad_styles_elem)
        
        # Add Categories
        if self.categories:
            categories_elem = E("Categories")
            for category in self.categories:
                categories_elem.append(category.to_xml())
            library_elem.append(categories_elem)
        
        # Add Patterns (convert from MM to target units)
        if self.patterns:
            patterns_elem = E("Patterns")
            for pattern in self.patterns:
                patterns_elem.append(pattern.to_xml(self.units))
            library_elem.append(patterns_elem)
        
        return library_elem
    
    def to_file(self, filename: Union[Path, str], units: Units = Units.MM, encoding: str = "utf-8", pretty_print: bool = True) -> None:
        """
        Save Library to XML file.
        
        Args:
            filename: Path to the output XML file.
            units: Target units for the output file (MM, INCH, or MIL). Defaults to MM.
            encoding: XML file encoding. Defaults to "utf-8".
            pretty_print: Whether to format the XML with indentation. Defaults to True.
        """

        # Determine path string
        if isinstance(filename, str):
            path = filename
        elif isinstance(filename, Path):
            path = str(filename)
        if not path:
            raise TypeError("Filename must be a non-empty string or Path.")

        # Generate XML tree and write to file
        root = self.to_xml(units)
        tree = etree.ElementTree(root)
        tree.write(
            path,
            encoding=encoding,
            xml_declaration=True,
            pretty_print=pretty_print,
        )
