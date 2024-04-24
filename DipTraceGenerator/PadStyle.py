#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import List, Optional
from copy import deepcopy
from lxml.etree import SubElement
from .Mixins import RootMixin, NameMixin, SideMixin, PadTypeMixin
from .MainStack import MainStackMixin
from .Terminal import TerminalsMixin
from .Enums import HoleType


class PadStyle(NameMixin, SideMixin, MainStackMixin, PadTypeMixin, TerminalsMixin):
    @property
    def hole_type(self) -> Optional[HoleType]:
        try:
            return HoleType(self._root.get("HoleType"))
        except (AttributeError, ValueError, KeyError):
            return None

    @hole_type.setter
    def hole_type(self, value: Optional[HoleType]) -> None:
        if value is not None:
            self._root.set("HoleType", value.value)
        elif "HoleType" in self._root.attrib:
            self._root.attrib.pop("HoleType")

    @property
    def hole_width(self) -> Optional[float]:
        try:
            return float(self._root.get("Hole"))
        except (AttributeError, ValueError, KeyError):
            return None

    @hole_width.setter
    def hole_width(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("Hole", f"{value:.5g}")
        elif "Hole" in self._root.attrib:
            self._root.attrib.pop("Hole")

    @property
    def hole_height(self) -> Optional[float]:
        try:
            return float(self._root.get("HoleH"))
        except (AttributeError, ValueError, KeyError):
            return None

    @hole_height.setter
    def hole_height(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("HoleH", f"{value:.5g}")
        elif "HoleH" in self._root.attrib:
            self._root.attrib.pop("HoleH")


class PadStylesMixin(RootMixin):
    @property
    def pad_styles(self) -> List[PadStyle]:
        return [PadStyle(x) for x in self._root.findall("./PadStyles/PadStyle")]

    @pad_styles.setter
    def pad_styles(self, value: Optional[List[PadStyle]]):
        if (tag := self._root.find("./PadStyles")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "PadStyles")
            for style in value:
                tag.append(deepcopy(style.root))


if __name__ == "__main__":
    pass
