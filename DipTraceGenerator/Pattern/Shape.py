#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Pattern Shape classes for DipTrace pattern library shapes."""

from typing import List
from ..xmltools import etree, E, dataclass, field
from ..Units import Units, convert_units
from ..Point import Point
from ..Enums import Boolean
from .Enums import ShapeType


@dataclass
class Shape:
    """
    Represents a graphical shape in a DipTrace pattern (footprint).
    
    Pattern shapes define the visual appearance of a footprint on various layers
    (silk screen, assembly, etc.). They can be lines, arcs, polygons, text, etc.
    
    Attributes:
        id (int): Unique identifier for the shape within the pattern.
        type (ShapeType): Shape type (Line, Arc, Rectangle, Polygon, etc. - no Arrow).
        locked (Boolean): Whether the shape is locked from editing.
        layer (str): The layer on which the shape appears (e.g., "Top Silk", "Top Assy").
        all_layers (Boolean): Whether the shape appears on all layers.
        points (List[Point]): List of points defining the shape geometry (in mm).
        width (float): Line width for outline shapes (in mm). Optional.
    """
    
    id: int = 0
    type: ShapeType = ShapeType.Line
    locked: Boolean = Boolean.No
    layer: str = "Top Silk"
    all_layers: Boolean = Boolean.No
    points: List[Point] = field(default_factory=list)
    width: float = field(default=None)  # Optional, not all shapes have width

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Shape":
        """
        Create Shape instance from XML element.

        Args:
            element (etree._Element): XML element representing the Shape.
            units (Units): Units of coordinates in the XML element. Defaults to Units.MM.
            
        Returns:
            Shape: Shape instance created from the XML element.
        """
        id_val = int(element.get("Id", "0"))
        type_val = ShapeType(element.get("Type", "Line"))
        locked = Boolean(element.get("Locked", "N"))
        layer = element.get("Layer", "Top Silk")
        all_layers = Boolean(element.get("AllLayers", "N"))
        
        # Parse optional width attribute
        width_str = element.get("Width")
        width = None
        if width_str is not None:
            width = convert_units(float(width_str), units, Units.MM)
        
        # Parse points
        points = []
        points_elem = element.find("Points")
        if points_elem is not None:
            for point_elem in points_elem.findall("Point"):
                points.append(Point.from_xml(point_elem, units))
        
        return cls(
            id=id_val,
            type=type_val,
            locked=locked,
            layer=layer,
            all_layers=all_layers,
            points=points,
            width=width
        )
    
    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Shape instance to XML element.

        Args:
            units (Units): Units for coordinates in the output XML. Defaults to Units.MM.
            
        Returns:
            etree._Element: XML element representing the Shape.
        """
        # Determine number of digits based on units
        if units == Units.INCH:
            digits = 6
        else:  # MM or MIL
            digits = 4
        
        # Build attributes dictionary
        attrs = {
            "Id": str(self.id),
            "Type": self.type.value,
            "Locked": self.locked.value,
            "Layer": self.layer,
            "AllLayers": self.all_layers.value,
        }
        
        # Add optional width if present
        if self.width is not None:
            width_converted = convert_units(self.width, Units.MM, units)
            attrs["Width"] = f"{width_converted:.{digits}f}"
        
        # Create shape element
        shape_elem = E.Shape(**attrs)
        
        # Add points if present
        if self.points:
            points_elem = E.Points()
            for point in self.points:
                points_elem.append(point.to_xml(units))
            shape_elem.append(points_elem)
        
        return shape_elem


if __name__ == "__main__":
    pass