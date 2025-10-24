#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Pattern CategoryType class for DipTrace pattern library category types."""

from typing import Optional
from ..xmltools import etree, E, dataclass


@dataclass
class CategoryType:
    """
    Represents a category type in a DipTrace pattern library.
    
    Pattern category types define classifications for footprints. Each CategoryType
    contains a Type (required) and optionally a SubType. Unlike component libraries
    where Type and SubType are separate hierarchical classes, in pattern libraries
    they are attributes within a single CategoryType element.
    
    Attributes:
        type_index (int): Index number of the Type.
        type_name (str): Name of the Type (e.g., "SOIC", "QFP").
        subtype_index (Optional[int]): Index number of the SubType (if present).
        subtype_name (Optional[str]): Name of the SubType (if present).
    
    Example XML:
        <CategoryType>
            <Type Index="2">SOIC</Type>
        </CategoryType>
        
        or with SubType:
        
        <CategoryType>
            <Type Index="2">SOIC</Type>
            <SubType Index="7">Pitch 1.27mm</SubType>
        </CategoryType>
    """
    
    type_index: int = 0
    type_name: str = ""
    subtype_index: Optional[int] = None
    subtype_name: Optional[str] = None

    @classmethod
    def from_xml(cls, element: etree._Element) -> "CategoryType":
        """
        Create CategoryType instance from XML element.

        Args:
            element (etree._Element): XML element representing the CategoryType.
            
        Returns:
            CategoryType: CategoryType instance created from the XML element.
        """
        # Parse Type element (required)
        type_elem = element.find("Type")
        type_index = 0
        type_name = ""
        if type_elem is not None:
            type_index = int(type_elem.get("Index", "0"))
            type_name = type_elem.text if type_elem.text else ""
        
        # Parse SubType element (optional)
        subtype_elem = element.find("SubType")
        subtype_index = None
        subtype_name = None
        if subtype_elem is not None:
            subtype_index = int(subtype_elem.get("Index", "0"))
            subtype_name = subtype_elem.text if subtype_elem.text else ""
        
        return cls(
            type_index=type_index,
            type_name=type_name,
            subtype_index=subtype_index,
            subtype_name=subtype_name
        )
    
    def to_xml(self) -> etree._Element:
        """
        Convert CategoryType instance to XML element.
            
        Returns:
            etree._Element: XML element representing the CategoryType.
        """
        # Create CategoryType element
        category_type_elem = E("CategoryType")
        
        # Add Type element (required)
        type_elem = E("Type", {"Index": str(self.type_index)}, self.type_name)
        category_type_elem.append(type_elem)
        
        # Add SubType element (if present)
        if self.subtype_index is not None and self.subtype_name is not None:
            subtype_elem = E("SubType", {"Index": str(self.subtype_index)}, self.subtype_name)
            category_type_elem.append(subtype_elem)
        
        return category_type_elem
