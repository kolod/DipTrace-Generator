#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Represents a pad style definition in a pattern library."""


from typing import Optional
from ..xmltools import etree, E, dataclass, field
from ..Units import Units, convert_units
from .Enums import PadType, HoleType, PadSide
from .MainStack import MainStack
from .MaskPaste import MaskPaste


@dataclass
class PadStyle:
    """
    Represents a pad style definition in a pattern library.
    
    PadStyle defines the complete pad configuration including:
    - Pad type (surface or through-hole)
    - Hole specifications (for through-hole pads)
    - Main copper stack-up (MainStack)
    - Solder mask and paste mask settings (MaskPaste)
    """
    
    name: str = field(default="")
    pad_type: PadType = field(default=PadType.Surface)
    side: PadSide = field(default=PadSide.Top)
    hole_type: Optional[HoleType] = field(default=None)
    hole: Optional[float] = field(default=None)
    hole_h: Optional[float] = field(default=None)
    main_stack: Optional[MainStack] = field(default=None)
    mask_paste: Optional[MaskPaste] = field(default=None)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "PadStyle":
        """
        Create PadStyle instance from XML element.

        Args:
            element (etree._Element): XML element representing the PadStyle.
            units (Units): Units of the dimensions in the XML element. Defaults to Units.MM.

        Returns:
            PadStyle: The created PadStyle instance.
        """
        name = element.get("Name", "")
        pad_type = PadType(element.get("Type", "Surface"))
        side = PadSide(element.get("Side", "Top"))
        
        # Parse hole attributes (only for through-hole pads)
        hole_type = None
        hole = None
        hole_h = None
        
        if "HoleType" in element.attrib:
            hole_type = HoleType(element.get("HoleType"))
        if "Hole" in element.attrib:
            hole = convert_units(float(element.get("Hole")), units, Units.MM)
        if "HoleH" in element.attrib:
            hole_h = convert_units(float(element.get("HoleH")), units, Units.MM)
        
        # Parse MainStack child element
        main_stack = None
        main_stack_element = element.find("MainStack")
        if main_stack_element is not None:
            main_stack = MainStack.from_xml(main_stack_element, units)
        
        # Parse MaskPaste child element
        mask_paste = None
        mask_paste_element = element.find("MaskPaste")
        if mask_paste_element is not None:
            mask_paste = MaskPaste.from_xml(mask_paste_element, units)
        
        return cls(
            name=name,
            pad_type=pad_type,
            side=side,
            hole_type=hole_type,
            hole=hole,
            hole_h=hole_h,
            main_stack=main_stack,
            mask_paste=mask_paste
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert PadStyle instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the PadStyle.
        """
        # Determine number of decimal places based on units
        digits = 6 if units == Units.INCH else 4
        
        # Create attributes dictionary
        attrs = {
            "Name": self.name,
            "Type": self.pad_type.value,
            "Side": self.side.value
        }
        
        # Add hole attributes for through-hole pads
        if self.hole_type is not None:
            attrs["HoleType"] = self.hole_type.value
        if self.hole is not None:
            attrs["Hole"] = f"{convert_units(self.hole, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        if self.hole_h is not None:
            attrs["HoleH"] = f"{convert_units(self.hole_h, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        
        # Create element
        element = E("PadStyle", attrs)
        
        # Add MainStack child element
        if self.main_stack is not None:
            element.append(self.main_stack.to_xml(units))
        
        # Add MaskPaste child element
        if self.mask_paste is not None:
            element.append(self.mask_paste.to_xml(units))
        
        return element
