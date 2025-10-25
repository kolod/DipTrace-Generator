#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Represents a 3D model reference for a pattern."""


from typing import Optional
from ..xmltools import etree, E, dataclass, field
from ..Units import Units, convert_units
from ..Enums import Boolean
from .Enums import Model3DUnits, Model3DType


@dataclass
class Filename:
    """Represents a 3D model filename with path and variable substitution."""
    path: str = field(default="")
    var: str = field(default="")

    @classmethod
    def from_xml(cls, element: etree._Element) -> "Filename":
        """
        Create Filename instance from XML element.

        Args:
            element (etree._Element): XML element representing the Filename.

        Returns:
            Filename: The created Filename instance.
        """
        path_elem = element.find("Path")
        var_elem = element.find("Var")
        
        path = path_elem.text if path_elem is not None and path_elem.text else ""
        var = var_elem.text if var_elem is not None and var_elem.text else ""
        
        return cls(path=path, var=var)

    def to_xml(self) -> etree._Element:
        """
        Convert Filename instance to XML element.

        Returns:
            etree._Element: XML element representing the Filename.
        """
        element = E("Filename")
        
        path_elem = E("Path")
        path_elem.text = self.path
        element.append(path_elem)
        
        var_elem = E("Var")
        var_elem.text = self.var
        element.append(var_elem)
        
        return element


@dataclass
class Rotate:
    """Represents 3D model rotation angles."""
    x: float = field(default=0.0)
    y: float = field(default=0.0)
    z: float = field(default=0.0)

    @classmethod
    def from_xml(cls, element: etree._Element) -> "Rotate":
        """
        Create Rotate instance from XML element.

        Args:
            element (etree._Element): XML element representing the Rotate.

        Returns:
            Rotate: The created Rotate instance.
        """
        x = float(element.get("X", "0.0"))
        y = float(element.get("Y", "0.0"))
        z = float(element.get("Z", "0.0"))
        
        return cls(x=x, y=y, z=z)

    def to_xml(self) -> etree._Element:
        """
        Convert Rotate instance to XML element.

        Returns:
            etree._Element: XML element representing the Rotate.
        """
        attrs = {
            "X": str(int(self.x)) if self.x == int(self.x) else str(self.x),
            "Y": str(int(self.y)) if self.y == int(self.y) else str(self.y),
            "Z": str(int(self.z)) if self.z == int(self.z) else str(self.z)
        }
        
        return E("Rotate", attrs)


@dataclass
class Offset:
    """Represents 3D model position offset."""
    x: float = field(default=0.0)
    y: float = field(default=0.0)
    z: float = field(default=0.0)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Offset":
        """
        Create Offset instance from XML element.

        Args:
            element (etree._Element): XML element representing the Offset.
            units (Units): Units of the coordinates in the XML element. Defaults to Units.MM.

        Returns:
            Offset: The created Offset instance.
        """
        x = convert_units(float(element.get("X", "0.0")), units, Units.MM)
        y = convert_units(float(element.get("Y", "0.0")), units, Units.MM)
        z = convert_units(float(element.get("Z", "0.0")), units, Units.MM)
        
        return cls(x=x, y=y, z=z)

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Offset instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Offset.
        """
        digits = 6 if units == Units.INCH else 4
        
        attrs = {
            "X": f"{convert_units(self.x, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "Y": f"{convert_units(self.y, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "Z": f"{convert_units(self.z, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        }
        
        return E("Offset", attrs)


@dataclass
class Zoom:
    """Represents 3D model scale factors."""
    x: float = field(default=1.0)
    y: float = field(default=1.0)
    z: float = field(default=1.0)

    @classmethod
    def from_xml(cls, element: etree._Element) -> "Zoom":
        """
        Create Zoom instance from XML element.

        Args:
            element (etree._Element): XML element representing the Zoom.

        Returns:
            Zoom: The created Zoom instance.
        """
        x = float(element.get("X", "1.0"))
        y = float(element.get("Y", "1.0"))
        z = float(element.get("Z", "1.0"))
        
        return cls(x=x, y=y, z=z)

    def to_xml(self) -> etree._Element:
        """
        Convert Zoom instance to XML element.

        Returns:
            etree._Element: XML element representing the Zoom.
        """
        attrs = {
            "X": str(int(self.x)) if self.x == int(self.x) else str(self.x),
            "Y": str(int(self.y)) if self.y == int(self.y) else str(self.y),
            "Z": str(int(self.z)) if self.z == int(self.z) else str(self.z)
        }
        
        return E("Zoom", attrs)


@dataclass
class Model3D:
    """
    Represents a 3D model reference for a pattern.
    
    Model3D defines how a 3D model is associated with a footprint, including:
    - Model file reference
    - Model transformation (rotation, offset, scale)
    - Model settings (mirror, search, units)
    - IPC-7351 model positioning
    """
    
    mirror: Boolean = field(default=Boolean.No)
    no_search: Boolean = field(default=Boolean.No)
    units: Model3DUnits = field(default=Model3DUnits.MM)
    ipc_xoff: float = field(default=0.0)
    ipc_yoff: float = field(default=0.0)
    auto_height: float = field(default=0.0)
    auto_color: int = field(default=4934475)
    model_type: Model3DType = field(default=Model3DType.File)
    keep_pins: Boolean = field(default=Boolean.No)
    filename: Optional[Filename] = field(default=None)
    rotate: Optional[Rotate] = field(default=None)
    offset: Optional[Offset] = field(default=None)
    zoom: Optional[Zoom] = field(default=None)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "Model3D":
        """
        Create Model3D instance from XML element.

        Args:
            element (etree._Element): XML element representing the Model3D.
            units (Units): Units of the dimensions in the XML element. Defaults to Units.MM.

        Returns:
            Model3D: The created Model3D instance.
        """
        mirror = Boolean(element.get("Mirror", "N"))
        no_search = Boolean(element.get("NoSearch", "N"))
        model_units = Model3DUnits(element.get("Units", "mm"))
        ipc_xoff = convert_units(float(element.get("IPC_XOff", "0.0")), units, Units.MM)
        ipc_yoff = convert_units(float(element.get("IPC_YOff", "0.0")), units, Units.MM)
        auto_height = convert_units(float(element.get("AutoHeight", "0.0")), units, Units.MM)
        auto_color = int(element.get("AutoColor", "4934475"))
        model_type = Model3DType(element.get("Type", "File"))
        keep_pins = Boolean(element.get("KeepPins", "N"))
        
        # Parse child elements
        filename = None
        filename_elem = element.find("Filename")
        if filename_elem is not None:
            filename = Filename.from_xml(filename_elem)
        
        rotate = None
        rotate_elem = element.find("Rotate")
        if rotate_elem is not None:
            rotate = Rotate.from_xml(rotate_elem)
        
        offset = None
        offset_elem = element.find("Offset")
        if offset_elem is not None:
            offset = Offset.from_xml(offset_elem, units)
        
        zoom = None
        zoom_elem = element.find("Zoom")
        if zoom_elem is not None:
            zoom = Zoom.from_xml(zoom_elem)
        
        return cls(
            mirror=mirror,
            no_search=no_search,
            units=model_units,
            ipc_xoff=ipc_xoff,
            ipc_yoff=ipc_yoff,
            auto_height=auto_height,
            auto_color=auto_color,
            model_type=model_type,
            keep_pins=keep_pins,
            filename=filename,
            rotate=rotate,
            offset=offset,
            zoom=zoom
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Model3D instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Model3D.
        """
        digits = 6 if units == Units.INCH else 4
        
        attrs = {
            "Mirror": self.mirror.value,
            "NoSearch": self.no_search.value,
            "Units": self.units.value,
            "IPC_XOff": f"{convert_units(self.ipc_xoff, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "IPC_YOff": f"{convert_units(self.ipc_yoff, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "AutoHeight": f"{convert_units(self.auto_height, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "AutoColor": str(self.auto_color),
            "Type": self.model_type.value,
            "KeepPins": self.keep_pins.value
        }
        
        element = E("Model3D", attrs)
        
        # Add child elements
        if self.filename is not None:
            element.append(self.filename.to_xml())
        
        if self.rotate is not None:
            element.append(self.rotate.to_xml())
        
        if self.offset is not None:
            element.append(self.offset.to_xml(units))
        
        if self.zoom is not None:
            element.append(self.zoom.to_xml())
        
        return element
