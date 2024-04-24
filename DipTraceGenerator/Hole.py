#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import List
from lxml.etree import SubElement
from .Mixins import RootMixin, IdMixin, LockedMixin, XMixin, YMixin, DiameterMixin, HoleDiameterMixin


class Hole(IdMixin, LockedMixin, XMixin, YMixin, DiameterMixin, HoleDiameterMixin):
    pass


class HolesMixin(RootMixin):
    @property
    def holes(self) -> List[Hole]:
        return [Hole(x) for x in self._root.findall("./Holes/Hole")]

    @holes.setter
    def holes(self, value: List[Hole]):
        for tag in self._root.findall("./Holes"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Holes")
            for point in value:
                tag.append(point.root)


if __name__ == "__main__":
    pass
