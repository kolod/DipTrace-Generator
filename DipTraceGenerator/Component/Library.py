"""Component Library - Top-level container for DipTrace component library files."""

from dataclasses import dataclass, field
from typing import List, Optional
from lxml import etree
from lxml.builder import E

from ..Units import Units
from .Component import Component


@dataclass
class Category:
    """
    Represents a component category with types and subtypes.
    
    Categories organize components into a hierarchical structure:
    Category > Type > SubType
    """
    
    index: int
    name: str
    types: List['Type'] = field(default_factory=list)
    
    @classmethod
    def from_xml(cls, element: etree._Element) -> 'Category':
        """Parse a Category from an XML element."""
        index = int(element.get('Index', '0'))
        name_elem = element.find('Name')
        name = name_elem.text if name_elem is not None and name_elem.text else ''
        
        types = []
        types_elem = element.find('Types')
        if types_elem is not None:
            for type_elem in types_elem.findall('Type'):
                types.append(Type.from_xml(type_elem))
        
        return cls(index=index, name=name, types=types)
    
    def to_xml(self) -> etree._Element:
        """Convert this Category to an XML element."""
        elem = E.Category(Index=str(self.index))
        elem.append(E.Name(self.name))
        
        if self.types:
            types_elem = E.Types()
            for t in self.types:
                types_elem.append(t.to_xml())
            elem.append(types_elem)
        else:
            elem.append(E.Types())
        
        return elem


@dataclass
class SubType:
    """Represents a component sub-type within a Type."""
    
    index: int
    name: str
    
    @classmethod
    def from_xml(cls, element: etree._Element) -> 'SubType':
        """Parse a SubType from an XML element."""
        index = int(element.get('Index', '0'))
        name_elem = element.find('Name')
        name = name_elem.text if name_elem is not None and name_elem.text else ''
        
        return cls(index=index, name=name)
    
    def to_xml(self) -> etree._Element:
        """Convert this SubType to an XML element."""
        elem = E.SubType(Index=str(self.index))
        elem.append(E.Name(self.name))
        return elem


@dataclass
class Type:
    """Represents a component type within a Category."""
    
    index: int
    name: str
    subtypes: List[SubType] = field(default_factory=list)
    
    @classmethod
    def from_xml(cls, element: etree._Element) -> 'Type':
        """Parse a Type from an XML element."""
        index = int(element.get('Index', '0'))
        name_elem = element.find('Name')
        name = name_elem.text if name_elem is not None and name_elem.text else ''
        
        subtypes = []
        subtypes_elem = element.find('SubTypes')
        if subtypes_elem is not None:
            for subtype_elem in subtypes_elem.findall('SubType'):
                subtypes.append(SubType.from_xml(subtype_elem))
        
        return cls(index=index, name=name, subtypes=subtypes)
    
    def to_xml(self) -> etree._Element:
        """Convert this Type to an XML element."""
        elem = E.Type(Index=str(self.index))
        elem.append(E.Name(self.name))
        
        if self.subtypes:
            subtypes_elem = E.SubTypes()
            for st in self.subtypes:
                subtypes_elem.append(st.to_xml())
            elem.append(subtypes_elem)
        else:
            elem.append(E.SubTypes())
        
        return elem


@dataclass
class Library:
    """
    Represents a DipTrace Component Library.
    
    This is the top-level container for a component library file (.elixml).
    Contains a nested pattern library (stubbed), categories for organization,
    and the actual components.
    """
    
    id: Optional[int] = None
    type: str = "DipTrace-ComponentLibrary"
    name: str = ""
    hint: str = ""
    version: str = "5.2.0.1"
    units: Units = Units.MM
    
    # Nested PatternLibrary stub - not implemented
    pattern_library_xml: Optional[etree._Element] = None
    
    # Categories for organizing components
    categories: List[Category] = field(default_factory=list)
    
    # The actual components
    components: List[Component] = field(default_factory=list)
    
    @classmethod
    def from_xml(cls, element: etree._Element) -> 'Library':
        """
        Parse a Library from an XML element.
        
        Validates that Type="DipTrace-ComponentLibrary".
        Raises ValueError if the type is incorrect.
        """
        # Validate library type
        lib_type = element.get('Type', '')
        if lib_type != 'DipTrace-ComponentLibrary':
            raise ValueError(
                f"Invalid library type: '{lib_type}'. "
                f"Expected 'DipTrace-ComponentLibrary'."
            )
        
        # Parse basic attributes
        id_str = element.get('Id')
        id_val = int(id_str) if id_str is not None else None
        name = element.get('Name', '')
        hint = element.get('Hint', '')
        version = element.get('Version', '5.2.0.1')
        units_str = element.get('Units', 'mm')
        # Units is already a str enum, so we can use it directly
        units = Units(units_str)
        
        # Store nested PatternLibrary as-is (stub)
        pattern_lib = element.find("Library[@Type='DipTrace-PatternLibrary']")
        
        # Parse categories
        categories = []
        categories_elem = element.find('Categories')
        if categories_elem is not None:
            for cat_elem in categories_elem.findall('Category'):
                categories.append(Category.from_xml(cat_elem))
        
        # Parse components
        components = []
        components_elem = element.find('Components')
        if components_elem is not None:
            for comp_elem in components_elem.findall('Component'):
                components.append(Component.from_xml(comp_elem))
        
        return cls(
            id=id_val,
            type=lib_type,
            name=name,
            hint=hint,
            version=version,
            units=units,
            pattern_library_xml=pattern_lib,
            categories=categories,
            components=components
        )
    
    def to_xml(self) -> etree._Element:
        """Convert this Library to an XML element."""
        attrs = {
            'Type': self.type,
            'Name': self.name,
            'Version': self.version,
            'Units': self.units.value  # Use .value to get the string representation
        }
        
        if self.id is not None:
            attrs['Id'] = str(self.id)
        
        if self.hint:
            attrs['Hint'] = self.hint
        
        elem = E.Library(**attrs)
        
        # Add nested PatternLibrary if present (stub)
        if self.pattern_library_xml is not None:
            elem.append(self.pattern_library_xml)
        
        # Add categories
        if self.categories:
            categories_elem = E.Categories()
            for cat in self.categories:
                categories_elem.append(cat.to_xml())
            elem.append(categories_elem)
        
        # Add components
        if self.components:
            components_elem = E.Components()
            for comp in self.components:
                components_elem.append(comp.to_xml())
            elem.append(components_elem)
        
        return elem
    
    @classmethod
    def load(cls, filepath: str) -> 'Library':
        """
        Load a Library from a file.
        
        Args:
            filepath: Path to the .elixml file
            
        Returns:
            The parsed Library
            
        Raises:
            ValueError: If the file is not a DipTrace-ComponentLibrary
        """
        tree = etree.parse(filepath)
        root = tree.getroot()
        return cls.from_xml(root)
    
    def save(self, filepath: str) -> None:
        """
        Save this Library to a file.
        
        Args:
            filepath: Path to save the .elixml file
        """
        xml = self.to_xml()
        tree = etree.ElementTree(xml)
        tree.write(
            filepath,
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True
        )
