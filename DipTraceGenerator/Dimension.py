#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from dataclasses import dataclass
from typing import List, Optional
from copy import deepcopy
from lxml.etree import SubElement
from .Mixins import RootMixin, LockedMixin, AngleMixin, FontVectorMixin, FontMixin, LayerMixin
from .Enums import DimensionType, Boolean, PointerMode


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


class Dimension(LockedMixin, AngleMixin, FontVectorMixin, FontMixin, LayerMixin):
    @dataclass
    class Connection:
        connected: str
        object: int
        sub_object: int
        point: int

    @dataclass
    class Point:
        x: float
        y: float

    @property
    def type(self) -> Optional[DimensionType]:
        try:
            return DimensionType(self._root.get("Type"))
        except (AttributeError, ValueError, TypeError):
            return None

    @type.setter
    def type(self, value: Optional[DimensionType]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        else:
            self._root.attrib.pop("Type")

    @property
    def connection_1(self) -> Optional[Connection]:
        try:
            return Dimension.Connection(
                connected=self._root.get("Connected1"),
                object=int_or_zero(self._root.get("Object1")),
                sub_object=int_or_zero(self._root.get("SubObject1")),
                point=int_or_zero(self._root.get("Point1")),
            )
        except (TypeError, ValueError, AttributeError):
            return None

    @connection_1.setter
    def connection_1(self, value: Optional[Connection]) -> None:
        if isinstance(value, Dimension.Connection):
            self._root.set("Connected1", value.connected)
            self._root.set("Object1", str(value.object))
            self._root.set("SubObject1", str(value.sub_object))
            self._root.set("Point1", str(value.point))
        else:
            if "Connected1" in self._root.attrib:
                self._root.attrib.pop("Connected1")
            if "Object1" in self._root.attrib:
                self._root.attrib.pop("Object1")
            if "SubObject1" in self._root.attrib:
                self._root.attrib.pop("SubObject1")
            if "Point1" in self._root.attrib:
                self._root.attrib.pop("Point1")

    @property
    def connection_2(self) -> Optional[Connection]:
        try:
            return Dimension.Connection(
                connected=self._root.get("Connected2"),
                object=int_or_zero(self._root.get("Object2")),
                sub_object=int_or_zero(self._root.get("SubObject2")),
                point=int_or_zero(self._root.get("Point2")),
            )
        except (TypeError, ValueError, AttributeError):
            return None

    @connection_2.setter
    def connection_2(self, value: Optional[Connection]) -> None:
        if isinstance(value, Dimension.Connection):
            self._root.set("Connected2", value.connected)
            self._root.set("Object2", str(value.object))
            self._root.set("SubObject2", str(value.sub_object))
            self._root.set("Point2", str(value.point))
        else:
            if "Connected2" in self._root.attrib:
                self._root.attrib.pop("Connected2")
            if "Object2" in self._root.attrib:
                self._root.attrib.pop("Object2")
            if "SubObject2" in self._root.attrib:
                self._root.attrib.pop("SubObject2")
            if "Point2" in self._root.attrib:
                self._root.attrib.pop("Point2")

    @property
    def point_1(self) -> Optional[Point]:
        try:
            return Dimension.Point(float(self._root.get("X1")), float(self._root.get("Y1")))
        except (TypeError, ValueError, AttributeError):
            return None

    @point_1.setter
    def point_1(self, value: Optional[Point]) -> None:
        if value is not None:
            self._root.set("X1", f"{value.x:.5g}")
            self._root.set("Y1", f"{value.y:.5g}")
        else:
            self._root.attrib.pop("X1")
            self._root.attrib.pop("Y1")

    @property
    def point_2(self) -> Optional[Point]:
        try:
            return Dimension.Point(float(self._root.get("X2")), float(self._root.get("Y2")))
        except (TypeError, ValueError, AttributeError):
            return None

    @point_2.setter
    def point_2(self, value: Optional[Point]) -> None:
        if value is not None:
            self._root.set("X2", f"{value.x:.5g}")
            self._root.set("Y2", f"{value.y:.5g}")
        else:
            self._root.attrib.pop("X2")
            self._root.attrib.pop("Y2")

    @property
    def point_d(self) -> Optional[Point]:
        try:
            return Dimension.Point(float(self._root.get("XD")), float(self._root.get("YD")))
        except (TypeError, ValueError, AttributeError):
            return None

    @point_d.setter
    def point_d(self, value: Optional[Point]) -> None:
        if value is not None:
            self._root.set("XD", f"{value.x:.5g}")
            self._root.set("YD", f"{value.y:.5g}")
        else:
            self._root.attrib.pop("XD")
            self._root.attrib.pop("YD")

    @property
    def show_units(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("ShowUnits"))
        except (TypeError, ValueError, AttributeError):
            return None

    @show_units.setter
    def show_units(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("ShowUnits", value.value)
        else:
            self._root.attrib.pop("ShowUnits")

    @property
    def external_radius(self) -> Optional[float]:
        try:
            return float(self._root.get("ExternalRadius"))
        except (ValueError, TypeError):
            return None

    @external_radius.setter
    def external_radius(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("ExternalRadius", f"{value:.5g}")
        else:
            self._root.attrib.pop("ExternalRadius")

    @property
    def pointer_mode(self) -> Optional[PointerMode]:
        try:
            return PointerMode(int(self._root.get("PointerMode")))
        except (TypeError, ValueError, AttributeError):
            return None

    @pointer_mode.setter
    def pointer_mode(self, value: Optional[PointerMode]) -> None:
        if value is not None:
            self._root.set("PointerMode", value.value)
        else:
            self._root.attrib.pop("PointerMode")

    @property
    def pointer_text(self) -> Optional[str]:
        if (tag := self._root.find("PointerText")) is not None:
            return tag.text
        return None

    @pointer_text.setter
    def pointer_text(self, value: Optional[str] = None) -> None:
        if value is not None:
            tag = SubElement(self._root, "PointerText")
            tag.text = value
        else:
            self._root.remove(self._root.find("PointerText"))

    @property
    def arrow_size(self) -> Optional[float]:
        try:
            return float(self._root.get("ArrowSize"))
        except (ValueError, TypeError):
            return None

    @arrow_size.setter
    def arrow_size(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("ArrowSize", f"{value:.5g}")
        else:
            self._root.attrib.pop("ArrowSize")


class DimensionsMixin(RootMixin):
    @property
    def dimensions(self) -> List[Dimension]:
        return [Dimension(x) for x in self._root.findall("./Dimensions/Dimension")]

    @dimensions.setter
    def dimensions(self, value: Optional[List[Dimension]]) -> None:
        for tag in self._root.findall("./Dimensions"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Dimensions")
            for dimension in value:
                tag.append(deepcopy(dimension.root))


if __name__ == "__main__":
    pass
