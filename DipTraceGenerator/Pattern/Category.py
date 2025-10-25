#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


"""
Pattern Category
Represents a hierarchical category structure for organizing patterns.
"""

from dataclasses import dataclass, field
from typing import List
from lxml import etree


@dataclass
class Category:
    """Category for organizing patterns in a library"""
    
    @dataclass
    class SubType:
        """SubType within a Type"""
        number: int = 0
        name: str = ""
    
    @dataclass
    class Type:
        """Type within a Category"""
        number: int = 0
        name: str = ""
        subtypes: List['Category.SubType'] = field(default_factory=list)
    
    number: int = 0
    name: str = ""
    types: List['Category.Type'] = field(default_factory=list)

    @classmethod
    def from_xml(cls, element: etree._Element) -> 'Category':
        """Create Category from XML element"""
        types = []
        types_elem = element.find('Types')
        if types_elem is not None:
            for type_elem in types_elem.findall('Type'):
                # Parse subtypes
                subtypes = []
                subtypes_elem = type_elem.find('SubTypes')
                if subtypes_elem is not None:
                    for subtype_elem in subtypes_elem.findall('SubType'):
                        subtypes.append(cls.SubType(
                            number=int(subtype_elem.get('Number', 0)),
                            name=subtype_elem.findtext('Name', default='')
                        ))
                
                # Create Type with subtypes
                types.append(cls.Type(
                    number=int(type_elem.get('Number', 0)),
                    name=type_elem.findtext('Name', default=''),
                    subtypes=subtypes
                ))
        
        return cls(
            number=int(element.get('Number', 0)),
            name=element.findtext('Name', default=''),
            types=types
        )

    def to_xml(self) -> etree._Element:
        """Convert Category to XML element"""
        category_elem = etree.Element('Category', Number=str(self.number))
        name_elem = etree.SubElement(category_elem, 'Name')
        name_elem.text = self.name
        
        # Always include Types element, even if empty
        types_elem = etree.SubElement(category_elem, 'Types')
        for type_obj in self.types:
            type_elem = etree.SubElement(types_elem, 'Type', Number=str(type_obj.number))
            type_name_elem = etree.SubElement(type_elem, 'Name')
            type_name_elem.text = type_obj.name
            
            # Always include SubTypes element, even if empty
            subtypes_elem = etree.SubElement(type_elem, 'SubTypes')
            for subtype in type_obj.subtypes:
                subtype_elem = etree.SubElement(subtypes_elem, 'SubType', Number=str(subtype.number))
                subtype_name_elem = etree.SubElement(subtype_elem, 'Name')
                subtype_name_elem.text = subtype.name
        
        return category_elem
