#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import List, Optional
from copy import deepcopy
from lxml.etree import SubElement
from .Mixins import RootMixin, WidthMixin, HeightMixin, XMixin, YMixin, AngleMixin, CornerMixin
from .Enums import TerminalShape
from .Point import PointsMixin


class Terminal(WidthMixin, HeightMixin, XMixin, YMixin, AngleMixin, CornerMixin, PointsMixin):
    @property
    def shape(self) -> Optional[TerminalShape]:
        try:
            return TerminalShape(self._root.get("Shape"))
        except (AttributeError, TypeError, ValueError):
            return None

    @shape.setter
    def shape(self, value: Optional[TerminalShape]) -> None:
        if value is not None:
            self._root.set("Shape", value.value)
            if value in [TerminalShape.Obround, TerminalShape.DShape, TerminalShape.Polygon]:
                self.corner = None
        elif "Shape" in self._root.attrib:
            self._root.attrib.pop("Shape")


class TerminalsMixin(RootMixin):
    @property
    def terminals(self) -> List[Terminal]:
        return [Terminal(x) for x in self._root.findall("./Terminals/Terminal")]

    @terminals.setter
    def terminals(self, value: List[Terminal]):
        for tag in self._root.findall("./Terminals"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Terminals")
            for terminal in value:
                tag.append(deepcopy(terminal.root))


if __name__ == "__main__":
    pass
