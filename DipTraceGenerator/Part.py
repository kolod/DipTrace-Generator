#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional, List, Tuple
from lxml.etree import SubElement
from copy import deepcopy
from .Mixins import (
    RootMixin,
    RefDesMixin,
    NameTagMixin,
    ValueTagMixin,
    DatasheetTagMixin,
    ManufacturerTagMixin,
    Order,
    WidthMixin,
    HeightMixin,
)
from .ComponentOrigin import ComponentOriginMixin
from .ComponentShape import ComponentShapesMixin
from .SpiceModel import SpiceModelMixin
from .Pin import PinsMixin
from .Enums import PartType, Boolean, PartStyle, ShapeType
from .Category import CategoryMixin


class Part(
    RefDesMixin,
    NameTagMixin,
    ValueTagMixin,
    ComponentOriginMixin,
    SpiceModelMixin,
    ComponentShapesMixin,
    PinsMixin,
    CategoryMixin,
    DatasheetTagMixin,
    ManufacturerTagMixin,
    WidthMixin,
    HeightMixin,
):
    _order = Order(
        args=[
            "RefDes",
            "PartType",
            "ShowNumbers",
            "Type",
            "Int1",
            "Int2",
            "Width",
            "Height",
            "LockTypeChange",
            "SubFolderIndex",
        ],
        tags=[
            "Name",
            "PartName",
            "Value",
            "Origin",
            "Datasheet",
            "SpiceModel",
            "Manufacturer",
            "Category",
            "Pins",
            "Shapes",
            "Pattern",
        ],
        subs=["pins"],
    )

    @property
    def part_name(self) -> Optional[str]:
        if (tag := self._root.find("PartName")) is not None:
            return tag.text
        return None

    @part_name.setter
    def part_name(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./PartName"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "PartName")
            tag.text = value

    @property
    def pattern(self) -> Optional[str]:
        if (tag := self._root.find("Pattern")) is not None:
            return tag.get("Style")
        return None

    @pattern.setter
    def pattern(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./Pattern"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Pattern")
            tag.set("Style", value)

    @property
    def part_type(self) -> Optional[PartType]:
        try:
            return PartType(self._root.get("PartType"))
        except (AttributeError, ValueError, TypeError):
            return None

    @part_type.setter
    def part_type(self, value: Optional[PartType]) -> None:
        if value is not None:
            self._root.set("PartType", value.value)
        elif "PartType" in self._root.attrib:
            self._root.attrib.pop("PartType")

    @property
    def style(self) -> Optional[PartStyle]:
        try:
            return PartStyle(self._root.get("Type"))
        except (AttributeError, ValueError, TypeError):
            return None

    @style.setter
    def style(self, value: Optional[PartStyle]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        elif "Type" in self._root.attrib:
            self._root.attrib.pop("Type")

    @property
    def show_numbers(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("ShowNumbers"))
        except (AttributeError, ValueError, TypeError):
            return None

    @show_numbers.setter
    def show_numbers(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("ShowNumbers", value.value)
        elif "ShowNumbers" in self._root.attrib:
            self._root.attrib.pop("ShowNumbers")

    @property
    def locked(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("LockTypeChange"))
        except (AttributeError, ValueError, TypeError):
            return None

    @locked.setter
    def locked(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("LockTypeChange", value.value)
        elif "LockTypeChange" in self._root.attrib:
            self._root.attrib.pop("LockTypeChange")

    @property
    def sub_folder_index(self) -> Optional[int]:
        try:
            return int(self._root.get("SubFolderIndex"))
        except (AttributeError, ValueError, TypeError):
            return None

    @sub_folder_index.setter
    def sub_folder_index(self, value: Optional[int]) -> None:
        if value is not None:
            self._root.set("SubFolderIndex", str(value))
        elif "SubFolderIndex" in self._root.attrib:
            self._root.attrib.pop("SubFolderIndex")

    @property
    def parameters(self) -> Optional[Tuple[int, int]]:
        try:
            return (int(self._root.get("Int1")), int(self._root.get("Int2")))
        except (ValueError, TypeError, ArithmeticError):
            return None

    @parameters.setter
    def parameters(self, value: Optional[Tuple[int, int]]) -> None:
        if "Int1" in self._root.attrib:
            self._root.attrib.pop("Int1")
        if "Int2" in self._root.attrib:
            self._root.attrib.pop("Int2")
        if value is not None:
            self._root.set("Int1", str(value[0]))
            self._root.set("Int2", str(value[1]))


class PartsMixin(RootMixin):
    @property
    def parts(self) -> List[Part]:
        return [Part(x) for x in self._root.findall("./Part")]

    @parts.setter
    def parts(self, value: List[Part]):
        for tag in self._root.findall("./Part"):
            self._root.remove(tag)
        for part in value:
            self._root.append(deepcopy(part.root))


if __name__ == "__main__":
    pass
