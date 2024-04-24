#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional, List
from copy import deepcopy
from lxml.etree import SubElement
from .Mixins import IdMixin, XMixin, YMixin, RootMixin


class Group(IdMixin, XMixin, YMixin):
    pass


class GroupsMixin(RootMixin):
    @property
    def groups(self) -> List[Group]:
        return [Group(x) for x in self._root.findall("./Groups/Group")]

    @groups.setter
    def groups(self, value: Optional[List[Group]]):
        for tag in self._root.findall("./Groups"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Groups")
            for style in value:
                tag.append(deepcopy(style.root))


if __name__ == "__main__":
    pass
