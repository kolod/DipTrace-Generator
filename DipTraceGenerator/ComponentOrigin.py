#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from typing import Optional
from copy import deepcopy
from lxml.etree import Element
from .Mixins import XMixin, YMixin, RootMixin, Order


class ComponentOrigin(XMixin, YMixin):
    _order = Order(args=["X", "Y"])

    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Origin")
        super().__init__(root, *args, **kwargs)


class ComponentOriginMixin(RootMixin):
    @property
    def origin(self) -> Optional[ComponentOrigin]:
        if (tag := self._root.find("Origin")) is not None:
            return ComponentOrigin(tag)
        return None

    @origin.setter
    def origin(self, value: Optional[ComponentOrigin]) -> None:
        for tag in self._root.findall("./Origin"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
