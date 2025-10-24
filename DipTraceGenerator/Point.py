#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from dataclasses import dataclass, field
from lxml import etree
from lxml.builder import E
from DipTraceGenerator import Units, convert_units


@dataclass
class Point:
    x: float = field(default=0.0)
    y: float = field(default=0.0)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Point":
        """
        Create Point instance from XML element.

        Args:
            element (etree._Element): XML element representing the Point.
            units (Units): Units of the coordinates in the XML element. Defaults to Units.MM.

        Returns:
            Point: The created Point instance.
                    
        """
        # Convert coordinates to millimeters for internal representation if needed
        x = convert_units(float(element.get("X", "0.0")), units, Units.MM)
        y = convert_units(float(element.get("Y", "0.0")), units, Units.MM)
        return cls(x=x, y=y)

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Point instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Point.
        """

        # Determine number of decimal places based on units
        digits = 6 if units == Units.INCH else 4

        # Convert coordinates from millimeters to desired units for XML representation if needed
        x_converted = convert_units(self.x, Units.MM, units)
        y_converted = convert_units(self.y, Units.MM, units)

        # Create XML element with formatted coordinates
        return E.Point(
            X=f"{x_converted:.{digits}f}", 
            Y=f"{y_converted:.{digits}f}"
        )


if __name__ == "__main__":
    pass