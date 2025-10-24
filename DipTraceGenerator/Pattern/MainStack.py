#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from DipTraceGenerator.xmltools import etree, E, dataclass, field
from DipTraceGenerator import Units, convert_units
from DipTraceGenerator.Enums import PadStackShape
from DipTraceGenerator.Point import Point
from typing import Optional


@dataclass
class MainStack:
    """
    Represents a pad stack definition in a pattern library.
    
    MainStack defines the copper pad shape and dimensions.
    For through-hole pads, it can be offset from the hole center.
    """
    
    shape: PadStackShape = field(default=PadStackShape.Ellipse)
    width: float = field(default=0.0)
    height: float = field(default=0.0)
    xoff: Optional[float] = field(default=None)
    yoff: Optional[float] = field(default=None)
    corner: Optional[float] = field(default=None)
    points: list[Point] = field(default_factory=list)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "MainStack":
        """
        Create MainStack instance from XML element.

        Args:
            element (etree._Element): XML element representing the MainStack.
            units (Units): Units of the dimensions in the XML element. Defaults to Units.MM.

        Returns:
            MainStack: The created MainStack instance.
        """
        shape = PadStackShape(element.get("Shape", "Ellipse"))
        width = convert_units(float(element.get("Width", "0.0")), units, Units.MM)
        height = convert_units(float(element.get("Height", "0.0")), units, Units.MM)
        
        # XOff and YOff are optional (only for through-hole pads)
        xoff = None
        yoff = None
        if "XOff" in element.attrib:
            xoff = convert_units(float(element.get("XOff")), units, Units.MM)
        if "YOff" in element.attrib:
            yoff = convert_units(float(element.get("YOff")), units, Units.MM)
        
        # Corner is optional (only for Rectangle shape)
        corner = None
        if "Corner" in element.attrib:
            corner = float(element.get("Corner"))
        
        # Parse polygon points if present
        points = []
        points_element = element.find("Points")
        if points_element is not None:
            for point_element in points_element.findall("Point"):
                points.append(Point.from_xml(point_element, units))
        
        return cls(
            shape=shape,
            width=width,
            height=height,
            xoff=xoff,
            yoff=yoff,
            corner=corner,
            points=points
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert MainStack instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the MainStack.
        """
        # Determine number of decimal places based on units
        digits = 6 if units == Units.INCH else 4
        
        # Create attributes dictionary
        attrs = {
            "Shape": self.shape.value,
            "Width": f"{convert_units(self.width, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "Height": f"{convert_units(self.height, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        }
        
        # Add optional attributes
        if self.xoff is not None:
            attrs["XOff"] = f"{convert_units(self.xoff, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        if self.yoff is not None:
            attrs["YOff"] = f"{convert_units(self.yoff, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        if self.corner is not None:
            attrs["Corner"] = str(int(self.corner))
        
        # Create element
        element = E("MainStack", attrs)
        
        # Add polygon points if present
        if self.points:
            points_element = E("Points")
            for point in self.points:
                points_element.append(point.to_xml(units))
            element.append(points_element)
        
        return element
