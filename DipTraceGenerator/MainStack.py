#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional
from copy import deepcopy
from .Mixins import RootMixin, WidthMixin, HeightMixin, CornerMixin, XOffsetMixin, YOffsetMixin
from .Enums import MainStackShape
from .Point import PointsMixin


class MainStack(WidthMixin, HeightMixin, CornerMixin, XOffsetMixin, YOffsetMixin, PointsMixin):
    @property
    def shape(self) -> Optional[MainStackShape]:
        try:
            return MainStackShape(self._root.get("Shape"))
        except (KeyError, ValueError):
            return None

    @shape.setter
    def shape(self, value: Optional[MainStackShape]) -> None:
        if value is not None:
            self._root.set("Shape", value.value)
            if value in [MainStackShape.Polygon, MainStackShape.Ellipse, MainStackShape.Rectangle]:
                self.x_offset = None
                self.y_offset = None
            if value in [MainStackShape.Polygon, MainStackShape.Ellipse, MainStackShape.Obround, MainStackShape.DShape]:
                self.corner = None
        else:
            self._root.attrib.pop("Shape")


class MainStackMixin(RootMixin):
    @property
    def main_stack(self) -> Optional[MainStack]:
        if (tag := self._root.find("./MainStack")) is not None:
            return MainStack(tag)
        return None

    @main_stack.setter
    def main_stack(self, value: Optional[MainStack]) -> None:
        for tag in self._root.findall("./MainStack"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
