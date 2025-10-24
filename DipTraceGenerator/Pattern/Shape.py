#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from ..xmltools import etree, E, dataclass, field, Enum

class ShapeType(Enum):
    Line         = "Line"
    Arrow        = "Arrow"
    Arc          = "Arc"
    Rectangle    = "Rectangle"
    FillRect     = "FillRect"
    Obround      = "Obround"
    FillObround  = "FillObround"
    Polyline     = "Polyline"
    Polygon      = "Polygon"
    Text         = "Text"


@dataclass
class Shape:
    id: int = field(default=0)
    type: ShapeType = field(default=ShapeType.Line)
    width: float = field(default=0.25)
    locked: bool = field(default=False)

    @classmethod
    def from_xml(cls, element: etree._Element) -> "Shape":
        """
        Create Shape instance from XML element.

        Args:
            element (etree._Element): XML element representing the Shape.
        Returns:
            Shape: Shape instance created from the XML element.
        """
        id = int(element.get("id", 0))
        type = ShapeType[element.get("type", "Line")]
        width = float(element.get("width", 0.25))
        locked = element.get("locked", "false").lower() == "true"

        return cls(id=id, type=type, width=width, locked=locked)
    
    def to_xml(self) -> etree._Element:
        """
        Convert Shape instance to XML element.

        Returns:
            etree._Element: XML element representing the Shape.
        """
        return E.Shape(
            id=str(self.id),
            type=self.type.name,
            width=str(self.width),
            locked=str(self.locked).lower()
        )

if __name__ == "__main__":
    pass