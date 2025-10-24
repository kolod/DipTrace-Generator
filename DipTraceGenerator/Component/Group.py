#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Group.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Group tests/test_Component_Group.py -v --cov-report=term --cov-report=term-missing


from ..xmltools import etree, E, dataclass, field
from ..Units import Units, convert_units


@dataclass
class Group:
    """
    Represents a group of shapes in a component part.
    
    Groups allow logical organization of shapes and can have their own origin.
    The group origin acts as a reference point for all shapes assigned to the group.
    
    Attributes:
        id (int): Unique identifier for the group. Defaults to 0.
        x (float): X coordinate of the group origin in millimeters. Defaults to 0.0.
        y (float): Y coordinate of the group origin in millimeters. Defaults to 0.0.
    """
    id: int = field(default=0)
    x: float = field(default=0.0)
    y: float = field(default=0.0)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Group":
        """
        Create Group instance from XML element.

        Args:
            element (etree._Element): XML element representing the Group.
            units (Units): Units of the coordinates in the XML element. Defaults to Units.MM.

        Returns:
            Group: The created Group instance with coordinates in millimeters.
            
        Example:
            >>> from lxml.etree import fromstring
            >>> xml = fromstring('<Group Id="0" X="-590.5512" Y="-295.2756"/>')
            >>> group = Group.from_xml(xml, units=Units.MIL)
            >>> group.id
            0
        """
        group_id = int(element.get("Id", "0"))
        x = convert_units(float(element.get("X", "0.0")), units, Units.MM)
        y = convert_units(float(element.get("Y", "0.0")), units, Units.MM)
        return cls(id=group_id, x=x, y=y)

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Group instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Group.
            
        Example:
            >>> group = Group(id=1, x=-15.0, y=-7.5)
            >>> element = group.to_xml(units=Units.MIL)
            >>> element.get("Id")
            '1'
        """
        digits = 6 if units == Units.INCH else 4
        
        x_converted = convert_units(self.x, Units.MM, units)
        y_converted = convert_units(self.y, Units.MM, units)
        
        return E.Group(
            Id=str(self.id),
            X=f"{x_converted:.{digits}f}",
            Y=f"{y_converted:.{digits}f}"
        )


if __name__ == "__main__":
    pass
