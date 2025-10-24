#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Part.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Part tests/test_Component_Part.py -v --cov-report=term --cov-report=term-missing


from typing import List
from ..Enums import PartType, ShowNumbers, ComponentType, Boolean
from ..xmltools import etree, E, dataclass, field
from ..Units import Units, convert_units
from .Origin import Origin
from .Pin import Pin
from .Shape import Shape
from .SpiceModel import SpiceModel
from .Group import Group


@dataclass
class Part:
    """
    Represents a component part in a DipTrace component library.
    
    A part is the schematic representation of a component, including its pins,
    shapes, and other graphical elements.
    
    Attributes:
        id (int): Unique identifier for the part. Defaults to 0.
        part_type (PartType): Type of the part. Defaults to Normal.
        show_numbers (ShowNumbers): How to show pin numbers. Defaults to Hide.
        type (ComponentType): Component type (Free/Fixed). Defaults to Free.
        int1 (int): Internal parameter 1. Defaults to 0.
        int2 (int): Internal parameter 2. Defaults to 0.
        width (float): Width of the part in millimeters. Defaults to 0.0.
        height (float): Height of the part in millimeters. Defaults to 0.0.
        lock_type_change (Boolean): Whether type changes are locked. Defaults to No.
        sub_folder_index (int): Index of the subfolder. Defaults to -1.
        name (str): Component name. Defaults to "Untitled".
        part_name (str): Part name. Defaults to "Part 1".
        origin (Origin): Origin point of the part. Defaults to Origin().
        spice_model (SpiceModel): SPICE model for simulation. Defaults to SpiceModel().
        pins (List[Pin]): List of pins. Defaults to empty list.
        shapes (List[Shape]): List of shapes. Defaults to empty list.
        groups (List[Group]): List of groups. Defaults to empty list.
    """
    id: int = field(default=0)
    part_type: PartType = field(default=PartType.Normal)
    show_numbers: ShowNumbers = field(default=ShowNumbers.Hide)
    type: ComponentType = field(default=ComponentType.Free)
    int1: int = field(default=0)
    int2: int = field(default=0)
    width: float = field(default=0.0)
    height: float = field(default=0.0)
    lock_type_change: Boolean = field(default=Boolean.No)
    sub_folder_index: int = field(default=-1)
    name: str = field(default="Untitled")
    part_name: str = field(default="Part 1")
    origin: Origin = field(default_factory=Origin)
    spice_model: SpiceModel = field(default_factory=SpiceModel)
    pins: List[Pin] = field(default_factory=list)
    shapes: List[Shape] = field(default_factory=list)
    groups: List[Group] = field(default_factory=list)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Part":
        """
        Create Part instance from XML element.

        Args:
            element (etree._Element): XML element representing the Part.
            units (Units): Units used in the XML element. Defaults to Units.MM.

        Returns:
            Part: The created Part instance.
        """
        # Parse attributes
        part_id = int(element.get("Id", "0"))
        part_type = PartType(element.get("PartType", "Normal"))
        show_numbers = ShowNumbers(element.get("ShowNumbers", "Hide"))
        comp_type = ComponentType(element.get("Type", "Free"))
        int1 = int(element.get("Int1", "0"))
        int2 = int(element.get("Int2", "0"))
        width = convert_units(float(element.get("Width", "0.0")), units, Units.MM)
        height = convert_units(float(element.get("Height", "0.0")), units, Units.MM)
        lock_type_change = Boolean(element.get("LockTypeChange", "N"))
        sub_folder_index = int(element.get("SubFolderIndex", "-1"))

        # Parse child elements
        name = element.findtext("Name", "Untitled")
        part_name = element.findtext("PartName", "Part 1")

        # Parse Origin
        origin_elem = element.find("Origin")
        origin = Origin.from_xml(origin_elem, units) if origin_elem is not None else Origin()

        # Parse SpiceModel
        spice_elem = element.find("SpiceModel")
        spice_model = SpiceModel.from_xml(spice_elem) if spice_elem is not None else SpiceModel()

        # Parse Pins
        pins = []
        pins_elem = element.find("Pins")
        if pins_elem is not None:
            for pin_elem in pins_elem.findall("Pin"):
                pins.append(Pin.from_xml(pin_elem, units))

        # Parse Shapes
        shapes = []
        shapes_elem = element.find("Shapes")
        if shapes_elem is not None:
            for shape_elem in shapes_elem.findall("Shape"):
                shapes.append(Shape.from_xml(shape_elem, units))

        # Parse Groups
        groups = []
        groups_elem = element.find("Groups")
        if groups_elem is not None:
            for group_elem in groups_elem.findall("Group"):
                groups.append(Group.from_xml(group_elem, units))

        return cls(
            id=part_id,
            part_type=part_type,
            show_numbers=show_numbers,
            type=comp_type,
            int1=int1,
            int2=int2,
            width=width,
            height=height,
            lock_type_change=lock_type_change,
            sub_folder_index=sub_folder_index,
            name=name,
            part_name=part_name,
            origin=origin,
            spice_model=spice_model,
            pins=pins,
            shapes=shapes,
            groups=groups
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Part instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Part.
        """
        digits = 6 if units == Units.INCH else 4

        # Convert dimensions
        width_converted = convert_units(self.width, Units.MM, units)
        height_converted = convert_units(self.height, Units.MM, units)

        # Create Part element with attributes
        part_elem = E.Part(
            Id=str(self.id),
            PartType=self.part_type.value,
            ShowNumbers=self.show_numbers.value,
            Type=self.type.value,
            Int1=str(self.int1),
            Int2=str(self.int2),
            Width=f"{width_converted:.{digits}f}",
            Height=f"{height_converted:.{digits}f}",
            LockTypeChange=self.lock_type_change.value,
            SubFolderIndex=str(self.sub_folder_index)
        )

        # Add child elements
        part_elem.append(E.Name(self.name))
        part_elem.append(E.PartName(self.part_name))
        part_elem.append(self.origin.to_xml(units))
        part_elem.append(self.spice_model.to_xml())

        # Add Pins
        pins_elem = E.Pins()
        for pin in self.pins:
            pins_elem.append(pin.to_xml(units))
        part_elem.append(pins_elem)

        # Add Shapes
        shapes_elem = E.Shapes()
        for shape in self.shapes:
            shapes_elem.append(shape.to_xml(units))
        part_elem.append(shapes_elem)

        # Add Groups
        groups_elem = E.Groups()
        for group in self.groups:
            groups_elem.append(group.to_xml(units))
        part_elem.append(groups_elem)

        return part_elem


if __name__ == "__main__":
    pass
