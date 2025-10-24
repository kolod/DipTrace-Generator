#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Pattern Origin class for DipTrace pattern library origin point."""

from ..xmltools import etree, E, dataclass
from ..Units import Units, convert_units
from ..Enums import Boolean


@dataclass
class Origin:
    """
    Represents the origin point of a DipTrace pattern (footprint).
    
    The origin defines the reference point for the pattern. Coordinates are
    measured as offset from the pattern center (0,0). The origin can have
    visual indicators (cross, circle) and different visibility settings.
    
    Attributes:
        x (float): X coordinate offset from pattern center (in mm, internal representation).
        y (float): Y coordinate offset from pattern center (in mm, internal representation).
        cross (Boolean): Show cross at origin point.
        circle (Boolean): Show circle at origin point (cross+circle = target).
        common (str): Origin visibility in all layers: "Show", "Hide", "Show if not center".
        courtyard (str): Origin visibility in courtyard layer: "Show", "Hide".
    """
    
    x: float = 0.0
    y: float = 0.0
    cross: Boolean = Boolean.Yes
    circle: Boolean = Boolean.Yes
    common: str = "Hide"
    courtyard: str = "Show"

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Origin":
        """
        Create Origin instance from XML element.

        Args:
            element (etree._Element): XML element representing the Origin.
            units (Units): Units of coordinates in the XML element. Defaults to Units.MM.
            
        Returns:
            Origin: Origin instance created from the XML element.
        """
        # Convert coordinates to mm for internal representation
        x = convert_units(float(element.get("X", "0.0")), units, Units.MM)
        y = convert_units(float(element.get("Y", "0.0")), units, Units.MM)
        
        cross = Boolean(element.get("Cross", "Y"))
        circle = Boolean(element.get("Circle", "Y"))
        common = element.get("Common", "Hide")
        courtyard = element.get("Courtyard", "Show")
        
        return cls(
            x=x,
            y=y,
            cross=cross,
            circle=circle,
            common=common,
            courtyard=courtyard
        )
    
    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Origin instance to XML element.

        Args:
            units (Units): Units for coordinates in the output XML. Defaults to Units.MM.
            
        Returns:
            etree._Element: XML element representing the Origin.
        """
        # Determine number of digits based on units
        if units == Units.INCH:
            digits = 6
        else:  # MM or MIL
            digits = 4
        
        # Convert coordinates from mm to target units
        x_out = convert_units(self.x, Units.MM, units)
        y_out = convert_units(self.y, Units.MM, units)
        
        # Build attributes dictionary
        attribs = {
            "X": f"{x_out:.{digits}f}",
            "Y": f"{y_out:.{digits}f}",
            "Cross": self.cross.value,
            "Circle": self.circle.value,
            "Common": self.common,
            "Courtyard": self.courtyard,
        }
        
        # Create Origin element (self-closing, no children)
        return E("Origin", attribs)
