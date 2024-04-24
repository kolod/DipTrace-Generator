#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import List
from copy import deepcopy
from lxml.etree import SubElement
from .Mixins import RootMixin, XMixin, YMixin, SideMixin, IdMixin, LockedMixin, StyleMixin, NumberTagMixin, AngleMixin


class Pad(XMixin, YMixin, SideMixin, IdMixin, LockedMixin, StyleMixin, NumberTagMixin, AngleMixin):
    pass


class PadsMixin(RootMixin):
    @property
    def pads(self) -> List[Pad]:
        return [Pad(x) for x in self._root.findall("./Pads/Pad")]

    @pads.setter
    def pads(self, value: List[Pad]):
        if (tag := self._root.find("./Pads")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Pads")
            for pad in value:
                tag.append(deepcopy(pad.root))


if __name__ == "__main__":
    pass
