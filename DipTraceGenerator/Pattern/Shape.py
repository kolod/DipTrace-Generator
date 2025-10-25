#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Pattern Shape classes for DipTrace pattern library shapes."""

from typing import List, Optional
from ..xmltools import etree, E, dataclass, field
from ..Units import Units, convert_units
from ..Point import Point
from ..Enums import Boolean, HorizontalAlign, VerticalAlign, TextAlign
from .Enums import ShapeType, Layer, TextShow


@dataclass
class Shape:
    """
    Represents a graphical shape in a DipTrace pattern (footprint).
    
    Pattern shapes define the visual appearance of a footprint on various layers
    (silk screen, assembly, etc.). They can be lines, arcs, polygons, text, etc.
    
    Attributes:
        id (int): Unique identifier for the shape within the pattern.
        type (ShapeType): Shape type (Line, Arc, Rectangle, Polygon, Text, etc. - no Arrow).
        locked (Boolean): Whether the shape is locked from editing.
        layer (Layer): The layer on which the shape appears (e.g., Layer.TopSilk, Layer.TopAssy).
        all_layers (Boolean): Whether the shape appears on all layers.
        points (List[Point]): List of points defining the shape geometry (in mm).
        width (float): Line width for outline shapes (in mm). Optional.
        
        Text-specific attributes (only for Type="Text"):
        font_vector (Boolean): True for vector font, False for TrueType font.
        font_name (str): Name of the TrueType font.
        font_size (int): Font size.
        font_scale (float): Horizontal scale for vector text.
        font_width (float): Line width for vector text (-3=thin, -2=normal, -1=bold, >0=custom).
        text_show (TextShow): What text to display (Any Text, Name, RefDes, Value, etc.).
        horz_align (HorizontalAlign): Horizontal text anchor point.
        vert_align (VerticalAlign): Vertical text anchor point.
        text_align (TextAlign): Text alignment.
        line_spacing (float): Line spacing for multiline text.
        angle (float): Angle of text in radians, counterclockwise.
        text_lines (List[str]): Lines of text content.
        group (int): Group number inside pattern.
    """
    
    id: int = 0
    type: ShapeType = ShapeType.Line
    locked: Boolean = Boolean.No
    layer: Layer = Layer.TopSilk
    all_layers: Boolean = Boolean.No
    points: List[Point] = field(default_factory=list)
    width: Optional[float] = None  # Optional, not all shapes have width
    
    # Text-specific attributes
    font_vector: Optional[Boolean] = None
    font_name: Optional[str] = None
    font_size: Optional[int] = None
    font_scale: Optional[float] = None
    font_width: Optional[float] = None
    text_show: Optional[TextShow] = None
    horz_align: Optional[HorizontalAlign] = None
    vert_align: Optional[VerticalAlign] = None
    text_align: Optional[TextAlign] = None
    line_spacing: Optional[float] = None
    angle: Optional[float] = None
    text_lines: List[str] = field(default_factory=list)
    group: Optional[int] = None

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
        layer = Layer(element.get("Layer", "Top Silk"))
        all_layers = Boolean(element.get("AllLayers", "N"))
        
        # Parse optional width attribute
        width_str = element.get("Width")
        width = None
        if width_str is not None:
            width = convert_units(float(width_str), units, Units.MM)
        
        # Parse text-specific attributes
        font_vector = None
        font_name = None
        font_size = None
        font_scale = None
        font_width = None
        text_show = None
        horz_align = None
        vert_align = None
        text_align = None
        line_spacing = None
        angle = None
        group = None
        text_lines = []
        
        if type_val == ShapeType.Text:
            font_vector_str = element.get("FontVector")
            if font_vector_str:
                font_vector = Boolean(font_vector_str)
            
            font_name = element.get("FontName")
            
            font_size_str = element.get("FontSize")
            if font_size_str:
                font_size = int(font_size_str)
            
            font_scale_str = element.get("FontScale")
            if font_scale_str:
                font_scale = float(font_scale_str)
            
            font_width_str = element.get("FontWidth")
            if font_width_str:
                font_width = float(font_width_str)
            
            text_show_str = element.get("TextShow")
            if text_show_str:
                text_show = TextShow(text_show_str)
            
            horz_align_str = element.get("HorzAlign")
            if horz_align_str:
                horz_align = HorizontalAlign(horz_align_str)
            
            vert_align_str = element.get("VertAlign")
            if vert_align_str:
                vert_align = VerticalAlign(vert_align_str)
            
            text_align_str = element.get("TextAlign")
            if text_align_str:
                text_align = TextAlign(text_align_str)
            
            line_spacing_str = element.get("LineSpacing")
            if line_spacing_str:
                line_spacing = float(line_spacing_str)
            
            angle_str = element.get("Angle")
            if angle_str:
                angle = float(angle_str)
            
            group_str = element.get("Group")
            if group_str:
                group = int(group_str)
            
            # Parse text lines
            text_lines_elem = element.find("TextLines")
            if text_lines_elem is not None:
                for line_elem in text_lines_elem.findall("TextLine"):
                    if line_elem.text:
                        text_lines.append(line_elem.text)
        
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
            width=width,
            font_vector=font_vector,
            font_name=font_name,
            font_size=font_size,
            font_scale=font_scale,
            font_width=font_width,
            text_show=text_show,
            horz_align=horz_align,
            vert_align=vert_align,
            text_align=text_align,
            line_spacing=line_spacing,
            angle=angle,
            text_lines=text_lines,
            group=group
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
            "Layer": self.layer.value,
            "AllLayers": self.all_layers.value,
        }
        
        # Add text-specific attributes if this is a text shape
        if self.type == ShapeType.Text:
            if self.font_vector is not None:
                attrs["FontVector"] = self.font_vector.value
            if self.font_name is not None:
                attrs["FontName"] = self.font_name
            if self.font_size is not None:
                attrs["FontSize"] = str(self.font_size)
            if self.font_scale is not None:
                attrs["FontScale"] = str(self.font_scale)
            if self.font_width is not None:
                attrs["FontWidth"] = str(self.font_width)
            if self.text_show is not None:
                attrs["TextShow"] = self.text_show.value
            if self.horz_align is not None:
                attrs["HorzAlign"] = self.horz_align.value
            if self.vert_align is not None:
                attrs["VertAlign"] = self.vert_align.value
            if self.text_align is not None:
                attrs["TextAlign"] = self.text_align.value
            if self.line_spacing is not None:
                attrs["LineSpacing"] = str(self.line_spacing)
            if self.angle is not None:
                attrs["Angle"] = str(self.angle)
            if self.group is not None:
                attrs["Group"] = str(self.group)
        
        # Add optional width if present (for non-text shapes)
        if self.width is not None:
            width_converted = convert_units(self.width, Units.MM, units)
            attrs["Width"] = f"{width_converted:.{digits}f}"
        
        # Create shape element
        shape_elem = E.Shape(**attrs)
        
        # Add text lines if present
        if self.type == ShapeType.Text and self.text_lines:
            text_lines_elem = E.TextLines()
            for line in self.text_lines:
                text_lines_elem.append(E.TextLine(line))
            shape_elem.append(text_lines_elem)
        
        # Add points if present
        if self.points:
            points_elem = E.Points()
            for point in self.points:
                points_elem.append(point.to_xml(units))
            shape_elem.append(points_elem)
        
        return shape_elem


if __name__ == "__main__":
    pass