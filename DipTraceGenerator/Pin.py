#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional, List
from copy import deepcopy
from dataclasses import dataclass, field
from lxml.etree import SubElement
from .Enums import Boolean, PinType, ElectricType
from .Mixins import XMixin, YMixin, RootMixin, NameTagMixin, LockedMixin, OrientationMixin, GroupMixin, Order
from .NameFont import NameFontMixin


@dataclass
class Shift(object):
    x: float = field(default_factory=lambda: 0.0)
    y: float = field(default_factory=lambda: 0.0)
    orientation: float = field(default_factory=lambda: 0.0)


class Pin(XMixin, YMixin, NameTagMixin, LockedMixin, OrientationMixin, GroupMixin, NameFontMixin):
    _order = Order(
        args=[
            "X",
            "Y",
            "Locked",
            "Type",
            "ElectricType",
            "Orientation",
            "PadId",
            "Length",
            "ShowName",
            "NumXShift",
            "NumYShift",
            "NameXShift",
            "NameYShift",
            "SignalDelay",
            "NumOrientation",
            "NameOrientation",
            "Group",
        ],
        tags=["Name", "PadNumber", "NameFont"],
    )

    @property
    def type(self) -> Optional[PinType]:
        try:
            return PinType(self._root.get("Type"))
        except (AttributeError, ValueError, TypeError):
            return None

    @type.setter
    def type(self, value: Optional[PinType]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        elif "Type" in self._root.attrib:
            self._root.attrib.pop("Type")

    @property
    def pad_number(self) -> Optional[str]:
        if (tag := self._root.find("./PadNumber")) is not None:
            return tag.text
        return None

    @pad_number.setter
    def pad_number(self, value: Optional[str]) -> None:
        for tag in self._root.findall("./PadNumber"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "PadNumber")
            tag.text = value

    @property
    def electric_type(self) -> Optional[ElectricType]:
        try:
            return ElectricType(self._root.get("ElectricType"))
        except (AttributeError, ValueError, TypeError):
            return None

    @electric_type.setter
    def electric_type(self, value: Optional[ElectricType]) -> None:
        if value is not None:
            self._root.set("ElectricType", value.value)
        elif "ElectricType" in self._root.attrib:
            self._root.attrib.pop("ElectricType")

    @property
    def pad_id(self) -> Optional[int]:
        try:
            return int(self._root.get("PadId"))
        except (AttributeError, ValueError, TypeError):
            return None

    @pad_id.setter
    def pad_id(self, value: Optional[int]) -> None:
        if value is not None:
            self._root.set("PadId", str(value))
        elif "PadId" in self._root.attrib:
            self._root.attrib.pop("PadId")

    @property
    def length(self) -> Optional[float]:
        try:
            return float(self._root.get("Length"))
        except (AttributeError, ValueError, TypeError):
            return None

    @length.setter
    def length(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("Length", f"{value:.5g}")
        elif "Length" in self._root.attrib:
            self._root.attrib.pop("Length")

    @property
    def delay(self) -> Optional[float]:
        try:
            return float(self._root.get("SignalDelay"))
        except (AttributeError, ValueError, TypeError):
            return None

    @delay.setter
    def delay(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("SignalDelay", f"{value:.5g}")
        elif "SignalDelay" in self._root.attrib:
            self._root.attrib.pop("SignalDelay")

    @property
    def show_name(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("ShowName"))
        except (AttributeError, ValueError, TypeError):
            return None

    @show_name.setter
    def show_name(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("ShowName", value.value)
        elif "ShowName" in self._root.attrib:
            self._root.attrib.pop("ShowName")

    @property
    def name_shift(self) -> Optional[Shift]:
        try:
            return Shift(
                x=float(self._root.get("NameXShift")),
                y=float(self._root.get("NameYShift")),
                orientation=float(self._root.get("NameOrientation")),
            )
        except (ValueError, TypeError, AttributeError):
            return None

    @name_shift.setter
    def name_shift(self, value: Optional[Shift]) -> None:
        if value is not None:
            self._root.set("NameXShift", f"{value.x:.5g}")
            self._root.set("NameYShift", f"{value.y:.5g}")
            self._root.set("NameOrientation", f"{value.orientation:.5g}")
        else:
            if "NameXShift" in self._root.attrib:
                self._root.attrib.pop("NameXShift")
            if "NameYShift" in self._root.attrib:
                self._root.attrib.pop("NameYShift")
            if "NameOrientation" in self._root.attrib:
                self._root.attrib.pop("NameOrientation")

    @property
    def number_shift(self) -> Optional[Shift]:
        try:
            return Shift(
                x=float(self._root.get("NumXShift")),
                y=float(self._root.get("NumYShift")),
                orientation=float(self._root.get("NumOrientation")),
            )
        except (ValueError, TypeError, AttributeError):
            return None

    @number_shift.setter
    def number_shift(self, value: Optional[Shift]) -> None:
        if value is not None:
            self._root.set("NumXShift", f"{value.x:.5g}")
            self._root.set("NumYShift", f"{value.y:.5g}")
            self._root.set("NumOrientation", f"{value.orientation:.5g}")
        else:
            if "NumXShift" in self._root.attrib:
                self._root.attrib.pop("NumXShift")
            if "NumYShift" in self._root.attrib:
                self._root.attrib.pop("NumYShift")
            if "NumOrientation" in self._root.attrib:
                self._root.attrib.pop("NumOrientation")


class PinsMixin(RootMixin):
    @property
    def pins(self) -> List[Pin]:
        return [Pin(x) for x in self._root.findall("./Pins/Pin")]

    @pins.setter
    def pins(self, value: Optional[List[Pin]]):
        for tag in self._root.findall("./Pins"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Pins")
            for style in value:
                tag.append(deepcopy(style.root))


if __name__ == "__main__":
    pass
