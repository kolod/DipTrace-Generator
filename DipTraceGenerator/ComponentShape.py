#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional, List
from lxml.etree import SubElement
from copy import deepcopy
from lxml.etree import Element
from .Mixins import RootMixin, LockedMixin, LineWidthMixin, GroupMixin, Order
from .Point import PointsMixin
from .Enums import ShapeType, Boolean


class ComponentShape(LockedMixin, LineWidthMixin, PointsMixin, GroupMixin):
    _order = Order(args=["Type", "LineWidth", "Locked", "Group"])

    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Shape")
        super().__init__(root, *args, **kwargs)

    @property
    def type(self) -> Optional[ShapeType]:
        try:
            return ShapeType(self._root.get("Type"))
        except (KeyError, ValueError):
            return None

    @type.setter
    def type(self, value: Optional[ShapeType]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        else:
            self._root.attrib.pop("Type")

    @property
    def enabled(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("Enabled"))
        except (ValueError, TypeError):
            return None

    @enabled.setter
    def enabled(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("Enabled", value.value)
        elif "Enabled" in self._root.attrib:
            self._root.attrib.pop("Enabled")


class ComponentShapesMixin(RootMixin):
    @property
    def shapes(self) -> List[ComponentShape]:
        return [ComponentShape(x) for x in self._root.findall("./Shapes/Shape")]

    @shapes.setter
    def shapes(self, value: Optional[List[ComponentShape]]):
        if (tag := self._root.find("./Shapes")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Shapes")
            for shape in value:
                tag.append(deepcopy(shape.root))


if __name__ == "__main__":
    pass
