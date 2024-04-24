#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional
from copy import deepcopy
from .Mixins import RootMixin, WidthMixin


class NameFont(WidthMixin):
    @property
    def scale(self) -> Optional[float]:
        try:
            return float(self._root.get("Scale"))
        except (ValueError, TypeError, AttributeError):
            return None

    @scale.setter
    def scale(self, value: Optional[float]):
        if value is not None:
            self._root.set("Scale", f"{value:.5g}")
        elif "Scale" in self._root.attrib:
            self._root.attrib.pop("Scale")

    @property
    def size(self) -> Optional[float]:
        try:
            return float(self._root.get("Size"))
        except (ValueError, TypeError, AttributeError):
            return None

    @size.setter
    def size(self, value: Optional[float]):
        if value is not None:
            self._root.set("Size", f"{value:.5g}")
        elif "Size" in self._root.attrib:
            self._root.attrib.pop("Size")


class NameFontMixin(RootMixin):
    @property
    def name_font(self) -> Optional[NameFont]:
        if (tag := self._root.find("./NameFont")) is not None:
            return NameFont(tag)
        return None

    @name_font.setter
    def name_font(self, value: Optional[NameFont]) -> None:
        for tag in self._root.findall("./NameFont"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
