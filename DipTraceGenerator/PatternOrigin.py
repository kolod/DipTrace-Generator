#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from typing import Optional
from copy import deepcopy

from lxml.etree import Element
from .Enums import Boolean, Visible
from .Mixins import XMixin, YMixin, RootMixin


class PatternOrigin(XMixin, YMixin):
    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Origin")
        super().__init__(root, *args, **kwargs)

    @property
    def cross(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("Cross"))
        except ValueError:
            return None

    @cross.setter
    def cross(self, value: Optional[Boolean] = None) -> None:
        if value is not None:
            self._root.set("Cross", value.value)
        else:
            self._root.attrib.pop("Cross")

    @property
    def circle(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("Circle"))
        except ValueError:
            return None

    @circle.setter
    def circle(self, value: Optional[Boolean] = None) -> None:
        if value is not None:
            self._root.set("Circle", value.value)
        else:
            self._root.attrib.pop("Circle")

    @property
    def courtyard(self) -> Optional[Visible]:
        try:
            return Visible(self._root.get("Courtyard"))
        except ValueError:
            return None

    @courtyard.setter
    def courtyard(self, value: Optional[Visible] = None) -> None:
        if value is not None:
            self._root.set("Courtyard", value.value)
        else:
            self._root.attrib.pop("Courtyard")

    @property
    def common(self) -> Optional[Visible]:
        """Show on all layers [yes/no]"""
        try:
            return Visible(self._root.get("Common"))
        except ValueError:
            return None

    @common.setter
    def common(self, value: Optional[Visible] = None) -> None:
        if value is not None:
            self._root.set("Common", value.value)
        else:
            self._root.attrib.pop("Common")


class PatternOriginMixin(RootMixin):
    @property
    def origin(self) -> Optional[PatternOrigin]:
        if (tag := self._root.find("./Origin")) is not None:
            return PatternOrigin(tag)
        return None

    @origin.setter
    def origin(self, value: Optional[PatternOrigin]) -> None:
        for tag in self._root.findall("./Origin"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
