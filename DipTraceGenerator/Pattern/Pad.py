#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Pattern Pad classes for DipTrace pattern library pads."""

from typing import Optional
from ..xmltools import etree, E, dataclass
from ..Units import Units, convert_units
from ..Enums import Boolean
from .Enums import Side


@dataclass
class Pad:
    """
    Represents a pad in a DipTrace pattern (footprint).
    
    Pattern pads define the physical landing areas for component leads on a PCB.
    They reference a PadStyle which defines the pad's shape, size, and stack-up.

    X, Y coordinates represent offset from pattern center coordinate (0, 0) to 
    pad center coordinate.
    
    Attributes:
        id (int): Unique identifier for the pad within the pattern.
        style (str): Reference to a PadStyle by name (e.g., "PadT0").
        x (float): X coordinate position (in mm, internal representation).
        y (float): Y coordinate position (in mm, internal representation).
        angle (float): Rotation angle in degrees counter-clockwise.
        locked (Boolean): Whether the pad is locked from editing.
        side (Side): Which side of the board the pad is on (Side.Top or Side.Bottom).
        number (str): Pad number or name (e.g., "1", "2", "GND").
    """
    
    id: int = 0
    style: str = ""
    x: float = 0.0
    y: float = 0.0
    angle: float = 0.0
    locked: Boolean = Boolean.No
    side: Side = Side.Top
    number: str = ""

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Pad":
        """
        Create Pad instance from XML element.

        Args:
            element (etree._Element): XML element representing the Pad.
            units (Units): Units of coordinates in the XML element. Defaults to Units.MM.
            
        Returns:
            Pad: Pad instance created from the XML element.
        """
        id_val = int(element.get("Id", "0"))
        style = element.get("Style", "")
        
        # Convert coordinates to mm for internal representation
        x = convert_units(float(element.get("X", "0.0")), units, Units.MM)
        y = convert_units(float(element.get("Y", "0.0")), units, Units.MM)
        
        # Angle is stored in radians
        angle = float(element.get("Angle", "0.0"))
        
        locked = Boolean(element.get("Locked", "N"))
        side = Side(element.get("Side", "Top"))
        
        # Parse number sub-element
        number_elem = element.find("Number")
        number = number_elem.text if number_elem is not None and number_elem.text else ""
        
        return cls(
            id=id_val,
            style=style,
            x=x,
            y=y,
            angle=angle,
            locked=locked,
            side=side,
            number=number
        )
    
    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Pad instance to XML element.

        Args:
            units (Units): Units for coordinates in the output XML. Defaults to Units.MM.
            
        Returns:
            etree._Element: XML element representing the Pad.
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
            "Id": str(self.id),
            "Style": self.style,
            "X": f"{x_out:.{digits}f}",
            "Y": f"{y_out:.{digits}f}",
            "Angle": f"{self.angle:.{digits}f}",
            "Locked": self.locked.value,
            "Side": self.side.value,
        }
        
        # Create Pad element
        pad_elem = E("Pad", attribs)
        
        # Add Number sub-element
        if self.number:
            pad_elem.append(E("Number", self.number))
        
        return pad_elem
