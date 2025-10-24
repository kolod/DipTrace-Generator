#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_Component_Pin.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.Component.Pin tests/test_Component_Pin.py -v --cov-report=term --cov-report=term-missing


from typing import Optional
from ..xmltools import etree, E, dataclass, field, Enum
from ..Units import Units, convert_units
from ..Enums import Boolean, PinType, ElectricType
from ..NameFont import NameFont


@dataclass
class Pin:
    """Component Pin class for DipTrace component library pins."""
    
    id: int = field(default=0)
    x: float = field(default=0.0)  # Internal representation in mm
    y: float = field(default=0.0)  # Internal representation in mm
    locked: Boolean = field(default=Boolean.No)
    type: PinType = field(default=PinType.Default)
    electric_type: ElectricType = field(default=ElectricType.Undefined)
    orientation: int = field(default=0)  # 0, 90, 180, 270 degrees
    pad_id: int = field(default=0)
    length: float = field(default=150.0)  # Internal representation in mm
    show_name: Boolean = field(default=Boolean.Yes)
    num_x_shift: float = field(default=0.0)  # Internal representation in mm
    num_y_shift: float = field(default=0.0)  # Internal representation in mm
    name_x_shift: float = field(default=0.0)  # Internal representation in mm
    name_y_shift: float = field(default=0.0)  # Internal representation in mm
    signal_delay: float = field(default=0.0)
    num_orientation: int = field(default=0)
    name_orientation: int = field(default=0)
    name: str = field(default="")
    pad_number: str = field(default="")
    name_font: NameFont = field(default_factory=NameFont)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Pin":
        """
        Create Pin instance from XML element.

        Args:
            element (etree._Element): XML element representing the Pin.
            units (Units): Units used in the XML element. Defaults to Units.MM.

        Returns:
            Pin: Pin instance created from the XML element.
        """
        # Basic attributes
        pin_id = int(element.get("Id", "0"))
        
        # Convert coordinates to mm for internal representation
        x = convert_units(float(element.get("X", "0.0")), units, Units.MM)
        y = convert_units(float(element.get("Y", "0.0")), units, Units.MM)
        
        locked = Boolean(element.get("Locked", "N"))
        pin_type = PinType(element.get("Type", "Default"))
        electric_type = ElectricType(element.get("ElectricType", "Undefined"))
        orientation = int(element.get("Orientation", "0"))
        pad_id = int(element.get("PadId", "0"))
        
        # Convert length to mm
        length = convert_units(float(element.get("Length", "150.0")), units, Units.MM)
        
        show_name = Boolean(element.get("ShowName", "Y"))
        
        # Convert shifts to mm
        num_x_shift = convert_units(float(element.get("NumXShift", "0.0")), units, Units.MM)
        num_y_shift = convert_units(float(element.get("NumYShift", "0.0")), units, Units.MM)
        name_x_shift = convert_units(float(element.get("NameXShift", "0.0")), units, Units.MM)
        name_y_shift = convert_units(float(element.get("NameYShift", "0.0")), units, Units.MM)
        
        signal_delay = float(element.get("SignalDelay", "0.0"))
        num_orientation = int(element.get("NumOrientation", "0"))
        name_orientation = int(element.get("NameOrientation", "0"))
        
        # Parse name
        name_elem = element.find("Name")
        name = name_elem.text if name_elem is not None and name_elem.text else ""
        
        # Parse pad number
        pad_number_elem = element.find("PadNumber")
        pad_number = pad_number_elem.text if pad_number_elem is not None and pad_number_elem.text else ""
        
        # Parse name font
        name_font_elem = element.find("NameFont")
        name_font = NameFont.from_xml(name_font_elem) if name_font_elem is not None else NameFont()
        
        return cls(
            id=pin_id,
            x=x,
            y=y,
            locked=locked,
            type=pin_type,
            electric_type=electric_type,
            orientation=orientation,
            pad_id=pad_id,
            length=length,
            show_name=show_name,
            num_x_shift=num_x_shift,
            num_y_shift=num_y_shift,
            name_x_shift=name_x_shift,
            name_y_shift=name_y_shift,
            signal_delay=signal_delay,
            num_orientation=num_orientation,
            name_orientation=name_orientation,
            name=name,
            pad_number=pad_number,
            name_font=name_font
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Pin instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Pin.
        """
        # Determine decimal places based on units
        digits = 6 if units == Units.INCH else 4
        
        # Convert coordinates from mm to desired units
        x = convert_units(self.x, Units.MM, units)
        y = convert_units(self.y, Units.MM, units)
        length = convert_units(self.length, Units.MM, units)
        num_x_shift = convert_units(self.num_x_shift, Units.MM, units)
        num_y_shift = convert_units(self.num_y_shift, Units.MM, units)
        name_x_shift = convert_units(self.name_x_shift, Units.MM, units)
        name_y_shift = convert_units(self.name_y_shift, Units.MM, units)
        
        # Build attributes dictionary
        attribs = {
            "Id": str(self.id),
            "X": f"{x:.{digits}f}",
            "Y": f"{y:.{digits}f}",
            "Locked": self.locked.value,
            "Type": self.type.value,
            "ElectricType": self.electric_type.value,
            "Orientation": str(self.orientation),
            "PadId": str(self.pad_id),
            "Length": f"{length:.{digits}f}",
            "ShowName": self.show_name.value,
            "NumXShift": f"{num_x_shift:.{digits}f}",
            "NumYShift": f"{num_y_shift:.{digits}f}",
            "NameXShift": f"{name_x_shift:.{digits}f}",
            "NameYShift": f"{name_y_shift:.{digits}f}",
            "SignalDelay": str(self.signal_delay),
            "NumOrientation": str(self.num_orientation),
            "NameOrientation": str(self.name_orientation)
        }
        
        # Create pin element
        pin_elem = etree.Element("Pin", attribs)
        
        # Add name
        if self.name:
            name_elem = etree.SubElement(pin_elem, "Name")
            name_elem.text = self.name
        
        # Add pad number
        if self.pad_number:
            pad_number_elem = etree.SubElement(pin_elem, "PadNumber")
            pad_number_elem.text = self.pad_number
        
        # Add name font
        pin_elem.append(self.name_font.to_xml())
        
        return pin_elem


if __name__ == "__main__":
    pass
