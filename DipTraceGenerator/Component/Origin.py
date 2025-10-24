#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Origin.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Origin tests/test_Component_Origin.py -v --cov-report=term --cov-report=term-missing


from ..xmltools import etree, E, dataclass, field
from DipTraceGenerator import Units, convert_units


@dataclass
class Origin:
    """
    Represents the origin point of a component.
    
    The origin defines the reference point for positioning the component.
    Coordinates are stored internally in millimeters.
    
    Attributes:
        x (float): X coordinate in millimeters. Defaults to 0.0.
        y (float): Y coordinate in millimeters. Defaults to 0.0.
    """
    x: float = field(default=0.0)
    y: float = field(default=0.0)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Origin":
        """
        Create Origin instance from XML element.

        Args:
            element (etree._Element): XML element representing the Origin.
            units (Units): Units of the coordinates in the XML element. Defaults to Units.MM.

        Returns:
            Origin: The created Origin instance with coordinates in millimeters.
                    
        Example:
            >>> from lxml.etree import fromstring
            >>> xml = fromstring('<Origin X="-590.5512" Y="-492.126"/>')
            >>> origin = Origin.from_xml(xml, units=Units.MIL)
            >>> origin.x  # Converted to mm
            -15.0
            >>> origin.y  # Converted to mm
            -12.5
        """
        # Convert coordinates to millimeters for internal representation if needed
        x = convert_units(float(element.get("X", "0.0")), units, Units.MM)
        y = convert_units(float(element.get("Y", "0.0")), units, Units.MM)
        return cls(x=x, y=y)

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Origin instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Origin.
            
        Example:
            >>> origin = Origin(x=-15.0, y=-12.5)
            >>> element = origin.to_xml(units=Units.MIL)
            >>> element.get("X")
            '-590.5512'
            >>> element.get("Y")
            '-492.1260'
        """

        # Determine number of decimal places based on units
        digits = 6 if units == Units.INCH else 4

        # Convert coordinates from millimeters to desired units for XML representation if needed
        x_converted = convert_units(self.x, Units.MM, units)
        y_converted = convert_units(self.y, Units.MM, units)

        # Create XML element with formatted coordinates
        return E.Origin(
            X=f"{x_converted:.{digits}f}", 
            Y=f"{y_converted:.{digits}f}"
        )


if __name__ == "__main__":
    pass
