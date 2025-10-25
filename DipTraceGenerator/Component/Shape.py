#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Component Shape class for DipTrace component library shapes."""


from typing import Optional, List
from ..xmltools import etree, E, dataclass, field
from ..Point import Point
from ..Units import Units
from ..Enums import Boolean, HorizontalAlign, VerticalAlign, TextAlign, TextShow
from .Enums import ShapeType


@dataclass
class Shape:
    """
    Component Shape class for DipTrace component library shapes.
    
    Attributes:
        id (int): Unique identifier for the shape. Defaults to 0.
        type (ShapeType): Type of the shape. Defaults to ShapeType.Line.
        line_width (float): Width of the shape's outline in millimeters. Defaults to 0.25.
        locked (Boolean): Whether the shape is locked. Defaults to Boolean.No.
        group (Optional[int]): Group ID the shape belongs to. Defaults to None.
        points (List[Point]): List of points defining the shape. Defaults to an empty list.
        font_vector (Optional[Boolean]): Whether the font is vector. Defaults to None.
        font_size (Optional[int]): Size of the font. Defaults to None.
        font_color (Optional[int]): Color of the font. Defaults to None.
        text_show (Optional[TextShow]): How the text is shown. Defaults to None.
        font_name (Optional[str]): Name of the font. Defaults to None.
        font_width (Optional[int]): Width of the font. Defaults to None.
        font_scale (Optional[float]): Scale of the font. Defaults to None.
        angle (Optional[float]): Angle of the text. Defaults to None.
        horz_align (Optional[HorizontalAlign]): Horizontal alignment of the text. Defaults to None.
        vert_align (Optional[VerticalAlign]): Vertical alignment of the text. Defaults to None.
        text_align (Optional[TextAlign]): Text alignment. Defaults to None.
        line_spacing (Optional[float]): Spacing between lines of text. Defaults to None.
        text_lines (List[str]): List of text lines for the shape. Defaults to an empty list.
    """
    
    id: int = field(default=0)
    type: ShapeType = field(default=ShapeType.Line)
    line_width: float = field(default=0.25)
    locked: Boolean = field(default=Boolean.No)
    group: Optional[int] = field(default=None)
    points: List[Point] = field(default_factory=list)
    
    # Text-specific attributes
    font_vector: Optional[Boolean] = field(default=None)
    font_size: Optional[int] = field(default=None)
    font_color: Optional[int] = field(default=None)
    text_show: Optional[TextShow] = field(default=None)
    font_name: Optional[str] = field(default=None)
    font_width: Optional[int] = field(default=None)
    font_scale: Optional[float] = field(default=None)
    angle: Optional[float] = field(default=None)
    horz_align: Optional[HorizontalAlign] = field(default=None)
    vert_align: Optional[VerticalAlign] = field(default=None)
    text_align: Optional[TextAlign] = field(default=None)
    line_spacing: Optional[float] = field(default=None)
    text_lines: List[str] = field(default_factory=list)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Shape":
        """
        Create Shape instance from XML element.

        Args:
            element (etree._Element): XML element representing the Shape.
            units (Units): Units used in the XML element. Defaults to Units.MM.

        Returns:
            Shape: Shape instance created from the XML element.
        """
        # Basic attributes
        shape_id = int(element.get("Id", "0"))
        shape_type = ShapeType(element.get("Type", "Line"))
        line_width = float(element.get("LineWidth", "9.8425"))
        locked = Boolean(element.get("Locked", "N"))
        
        # Optional group
        group = None
        if element.get("Group") is not None:
            group = int(element.get("Group"))
        
        # Parse points
        points = []
        points_elem = element.find("Points")
        if points_elem is not None:
            for point_elem in points_elem.findall("Point"):
                points.append(Point.from_xml(point_elem, units))
        
        # Text-specific attributes
        font_vector = None
        if element.get("FontVector") is not None:
            font_vector = Boolean(element.get("FontVector"))
        
        font_size = None
        if element.get("FontSize") is not None:
            font_size = int(element.get("FontSize"))
        
        font_color = None
        if element.get("FontColor") is not None:
            font_color = int(element.get("FontColor"))
        
        text_show = None
        if element.get("TextShow") is not None:
            text_show = TextShow(element.get("TextShow"))
        
        font_name = element.get("FontName")
        
        font_width = None
        if element.get("FontWidth") is not None:
            font_width = int(element.get("FontWidth"))
        
        font_scale = None
        if element.get("FontScale") is not None:
            font_scale = float(element.get("FontScale"))
        
        angle = None
        if element.get("Angle") is not None:
            angle = float(element.get("Angle"))
        
        horz_align = None
        if element.get("HorzAlign") is not None:
            horz_align = HorizontalAlign(element.get("HorzAlign"))
        
        vert_align = None
        if element.get("VertAlign") is not None:
            vert_align = VerticalAlign(element.get("VertAlign"))
        
        text_align = None
        if element.get("TextAlign") is not None:
            text_align = TextAlign(element.get("TextAlign"))
        
        line_spacing = None
        if element.get("LineSpacing") is not None:
            line_spacing = float(element.get("LineSpacing"))
        
        # Parse text lines
        text_lines = []
        text_lines_elem = element.find("TextLines")
        if text_lines_elem is not None:
            for line_elem in text_lines_elem.findall("TextLine"):
                if line_elem.text:
                    text_lines.append(line_elem.text)
        
        return cls(
            id=shape_id,
            type=shape_type,
            line_width=line_width,
            locked=locked,
            group=group,
            points=points,
            font_vector=font_vector,
            font_size=font_size,
            font_color=font_color,
            text_show=text_show,
            font_name=font_name,
            font_width=font_width,
            font_scale=font_scale,
            angle=angle,
            horz_align=horz_align,
            vert_align=vert_align,
            text_align=text_align,
            line_spacing=line_spacing,
            text_lines=text_lines
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Shape instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Shape.
        """
        # Build attributes dictionary
        attribs = {
            "Id": str(self.id),
            "Type": self.type.value,
            "LineWidth": f"{self.line_width:.4f}",
            "Locked": self.locked.value
        }
        
        # Add optional group
        if self.group is not None:
            attribs["Group"] = str(self.group)
        
        # Add text-specific attributes
        if self.font_vector is not None:
            attribs["FontVector"] = self.font_vector.value
        
        if self.font_size is not None:
            attribs["FontSize"] = str(self.font_size)
        
        if self.font_color is not None:
            attribs["FontColor"] = str(self.font_color)
        
        if self.text_show is not None:
            attribs["TextShow"] = self.text_show.value
        
        if self.font_name is not None:
            attribs["FontName"] = self.font_name
        
        if self.font_width is not None:
            attribs["FontWidth"] = str(self.font_width)
        
        if self.font_scale is not None:
            attribs["FontScale"] = str(self.font_scale)
        
        if self.angle is not None:
            attribs["Angle"] = str(self.angle)
        
        if self.horz_align is not None:
            attribs["HorzAlign"] = self.horz_align.value
        
        if self.vert_align is not None:
            attribs["VertAlign"] = self.vert_align.value
        
        if self.text_align is not None:
            attribs["TextAlign"] = self.text_align.value
        
        if self.line_spacing is not None:
            attribs["LineSpacing"] = str(self.line_spacing)
        
        # Create shape element
        shape_elem = etree.Element("Shape", attribs)
        
        # Add text lines if present
        if self.text_lines:
            text_lines_elem = etree.SubElement(shape_elem, "TextLines")
            for line in self.text_lines:
                line_elem = etree.SubElement(text_lines_elem, "TextLine")
                line_elem.text = line
        
        # Add points
        if self.points:
            points_elem = etree.SubElement(shape_elem, "Points")
            for point in self.points:
                points_elem.append(point.to_xml(units))
        
        return shape_elem


if __name__ == "__main__":
    pass
