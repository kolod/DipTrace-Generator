#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Pattern class for DipTrace Pattern Library."""

from dataclasses import dataclass, field
from typing import Optional
from lxml import etree
from lxml.builder import E

from ..Units import Units, convert_units
from ..Enums import Boolean
from .Origin import Origin
from .Pad import Pad
from .Shape import Shape
from .Model3D import Model3D
from .Category import Category


@dataclass
class Pattern:
    """
    Represents a PCB footprint pattern in DipTrace Pattern Library.
    
    Attributes:
        id: Pattern Id (unique number) in the library.
        ref_des: Pattern RefDes (default reference designator).
        mounting: Pattern mounting type: "None", "Through", "SMD", "Chassis", "Mixed".
        width: Pattern width (X distance between extreme points).
        height: Pattern height (Y distance between extreme points).
        orientation: Pattern rotation: "0", "90", "180", "270".
        lock_type_change: Lock of pattern template change.
        type: Style of pattern creation template: "Free", "Circle", "Lines", "Square", "Matrix", "Rectangle", "Zig-Zag", "IPC-7351".
        float1: Style parameter in pattern creation template.
        float2: Style parameter in pattern creation template.
        float3: Style parameter in pattern creation template.
        int1: Style parameter in pattern creation template.
        int2: Style parameter in pattern creation template.
        name: Pattern name.
        name_unique: Pattern unique name.
        name_description: Pattern name description.
        value: Pattern value.
        manufacturer: Pattern manufacturer.
        datasheet: Pattern datasheet link.
        origin: Pattern origin parameters.
        def_pad: Default pad style name.
        pads: List of pads in the pattern.
        shapes: List of shapes and texts in the pattern.
        model_3d: Pattern 3D model (optional).
        category: Category assigned to pattern (optional).
    """
    
    id: int = 0
    ref_des: str = ""
    mounting: str = "None"
    width: float = 0.0
    height: float = 0.0
    orientation: str = "0"
    lock_type_change: Boolean = Boolean.No
    type: str = "Free"
    float1: float = 0.0
    float2: float = 0.0
    float3: float = 0.0
    int1: int = 0
    int2: int = 0
    name: str = ""
    name_unique: str = ""
    name_description: str = ""
    value: str = ""
    manufacturer: str = ""
    datasheet: str = ""
    origin: Origin = field(default_factory=Origin)
    def_pad: str = ""
    pads: list[Pad] = field(default_factory=list)
    shapes: list[Shape] = field(default_factory=list)
    model_3d: Optional[Model3D] = None
    category: Optional[Category] = None
    
    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> 'Pattern':
        """
        Parse Pattern from XML element.
        
        Args:
            element: XML element representing the Pattern.
            units: Units used in the XML file.
            
        Returns:
            Pattern instance.
        """
        # Parse main attributes
        id = int(element.get("Id", "0"))
        ref_des = element.get("RefDes", "")
        mounting = element.get("Mounting", "None")
        
        # Convert dimensions from file units to mm
        width = convert_units(float(element.get("Width", "0")), units, Units.MM)
        height = convert_units(float(element.get("Height", "0")), units, Units.MM)
        
        orientation = element.get("Orientation", "0")
        lock_type_change = Boolean(element.get("LockTypeChange", "N"))
        type = element.get("Type", "Free")
        float1 = float(element.get("Float1", "0"))
        float2 = float(element.get("Float2", "0"))
        float3 = float(element.get("Float3", "0"))
        int1 = int(element.get("Int1", "0"))
        int2 = int(element.get("Int2", "0"))
        
        # Parse sub-elements
        name = ""
        name_elem = element.find("Name")
        if name_elem is not None and name_elem.text:
            name = name_elem.text
            
        name_unique = ""
        name_unique_elem = element.find("Name_Unique")
        if name_unique_elem is not None and name_unique_elem.text:
            name_unique = name_unique_elem.text
            
        name_description = ""
        name_desc_elem = element.find("Name_Description")
        if name_desc_elem is not None and name_desc_elem.text:
            name_description = name_desc_elem.text
            
        value = ""
        value_elem = element.find("Value")
        if value_elem is not None and value_elem.text:
            value = value_elem.text
            
        manufacturer = ""
        manufacturer_elem = element.find("Manufacturer")
        if manufacturer_elem is not None and manufacturer_elem.text:
            manufacturer = manufacturer_elem.text
            
        datasheet = ""
        datasheet_elem = element.find("Datasheet")
        if datasheet_elem is not None and datasheet_elem.text:
            datasheet = datasheet_elem.text
        
        # Parse Origin
        origin = Origin()
        origin_elem = element.find("Origin")
        if origin_elem is not None:
            origin = Origin.from_xml(origin_elem, units)
        
        # Parse DefPad
        def_pad = ""
        def_pad_elem = element.find("DefPad")
        if def_pad_elem is not None:
            def_pad = def_pad_elem.get("Style", "")
        
        # Parse Pads
        pads = []
        pads_elem = element.find("Pads")
        if pads_elem is not None:
            for pad_elem in pads_elem.findall("Pad"):
                pads.append(Pad.from_xml(pad_elem, units))
        
        # Parse Shapes
        shapes = []
        shapes_elem = element.find("Shapes")
        if shapes_elem is not None:
            for shape_elem in shapes_elem.findall("Shape"):
                shapes.append(Shape.from_xml(shape_elem, units))
        
        # Parse Model3D (optional)
        model_3d = None
        model_elem = element.find("Model3D")
        if model_elem is not None:
            model_3d = Model3D.from_xml(model_elem, units)
        
        # Parse Category (optional)
        category = None
        category_elem = element.find("Category")
        if category_elem is not None:
            category = Category.from_xml(category_elem)
        
        return cls(
            id=id,
            ref_des=ref_des,
            mounting=mounting,
            width=width,
            height=height,
            orientation=orientation,
            lock_type_change=lock_type_change,
            type=type,
            float1=float1,
            float2=float2,
            float3=float3,
            int1=int1,
            int2=int2,
            name=name,
            name_unique=name_unique,
            name_description=name_description,
            value=value,
            manufacturer=manufacturer,
            datasheet=datasheet,
            origin=origin,
            def_pad=def_pad,
            pads=pads,
            shapes=shapes,
            model_3d=model_3d,
            category=category,
        )
    
    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert Pattern instance to XML element.
        
        Args:
            units: Units for coordinates in the output XML. Defaults to Units.MM.
            
        Returns:
            etree._Element: XML element representing the Pattern.
        """
        # Determine number of digits based on units
        if units == Units.INCH:
            digits = 6
        else:  # MM or MIL
            digits = 4
        
        # Convert dimensions from mm to target units
        width_out = convert_units(self.width, Units.MM, units)
        height_out = convert_units(self.height, Units.MM, units)
        
        # Build attributes dictionary
        attribs = {
            "Id": str(self.id),
            "RefDes": self.ref_des,
            "Mounting": self.mounting,
            "Width": f"{width_out:.{digits}f}",
            "Height": f"{height_out:.{digits}f}",
            "Orientation": self.orientation,
            "LockTypeChange": self.lock_type_change.value,
            "Type": self.type,
            "Float1": f"{self.float1:.{digits}f}",
            "Float2": f"{self.float2:.{digits}f}",
            "Float3": f"{self.float3:.{digits}f}",
            "Int1": str(self.int1),
            "Int2": str(self.int2),
        }
        
        # Create Pattern element
        pattern_elem = E("Pattern", attribs)
        
        # Add Name
        if self.name:
            pattern_elem.append(E("Name", self.name))
        
        # Add Name_Unique
        if self.name_unique:
            pattern_elem.append(E("Name_Unique", self.name_unique))
        
        # Add Name_Description
        if self.name_description:
            pattern_elem.append(E("Name_Description", self.name_description))
        
        # Add Value
        if self.value:
            pattern_elem.append(E("Value", self.value))
        
        # Add Manufacturer
        if self.manufacturer:
            pattern_elem.append(E("Manufacturer", self.manufacturer))
        
        # Add Datasheet
        if self.datasheet:
            pattern_elem.append(E("Datasheet", self.datasheet))
        
        # Add Category (if present)
        if self.category:
            pattern_elem.append(self.category.to_xml())
        
        # Add Origin
        pattern_elem.append(self.origin.to_xml(units))
        
        # Add DefPad
        if self.def_pad:
            pattern_elem.append(E("DefPad", {"Style": self.def_pad}))
        
        # Add Pads
        if self.pads:
            pads_elem = E("Pads")
            for pad in self.pads:
                pads_elem.append(pad.to_xml(units))
            pattern_elem.append(pads_elem)
        
        # Add Shapes
        if self.shapes:
            shapes_elem = E("Shapes")
            for shape in self.shapes:
                shapes_elem.append(shape.to_xml(units))
            pattern_elem.append(shapes_elem)
        
        # Add Model3D (if present)
        if self.model_3d:
            pattern_elem.append(self.model_3d.to_xml(units))
        
        return pattern_elem
