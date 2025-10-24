#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import List
from ..xmltools import etree, E, dataclass, field
from ..Units import Units
from .Part import Part


@dataclass
class Component:
    """
    Represents a component in a DipTrace component library.
    
    A component is a logical grouping of one or more parts (representations)
    of the same physical component. Each part can have different pin arrangements
    or package variations.
    
    Attributes:
        id (int): Unique identifier for the component. Defaults to 0.
        parts (List[Part]): List of parts that make up this component. Defaults to empty list.
    """
    id: int = field(default=0)
    parts: List[Part] = field(default_factory=list)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Component":
        """
        Create Component instance from XML element.

        Args:
            element (etree._Element): XML element representing the Component.
            units (Units): Units used in the XML element. Defaults to Units.MM.

        Returns:
            Component: The created Component instance.
            
        Example:
            >>> from lxml.etree import fromstring
            >>> xml_str = '''<Component Id="0">
            ...     <Part Id="0" PartType="Normal" ShowNumbers="Hide" Type="Free" 
            ...           Int1="0" Int2="0" Width="100" Height="200" 
            ...           LockTypeChange="N" SubFolderIndex="-1">
            ...         <Name>Test Component</Name>
            ...         <PartName>Part 1</PartName>
            ...         <Origin X="0" Y="0"/>
            ...         <SpiceModel Type="SubCkt"/>
            ...         <Pins/>
            ...         <Shapes/>
            ...         <Groups/>
            ...     </Part>
            ... </Component>'''
            >>> element = fromstring(xml_str)
            >>> component = Component.from_xml(element, units=Units.MIL)
            >>> component.id
            0
            >>> len(component.parts)
            1
        """
        # Parse attributes
        comp_id = int(element.get("Id", "0"))

        # Parse Parts
        parts = []
        for part_elem in element.findall("Part"):
            parts.append(Part.from_xml(part_elem, units))

        return cls(
            id=comp_id,
            parts=parts
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Component instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Component.
            
        Example:
            >>> component = Component(id=0)
            >>> part = Part(id=0, name="Test", part_name="Part 1")
            >>> component.parts.append(part)
            >>> element = component.to_xml(units=Units.MM)
            >>> element.get("Id")
            '0'
            >>> len(element.findall("Part"))
            1
        """
        # Create Component element with attributes
        comp_elem = E.Component(Id=str(self.id))

        # Add Parts
        for part in self.parts:
            comp_elem.append(part.to_xml(units))

        return comp_elem


if __name__ == "__main__":
    pass
