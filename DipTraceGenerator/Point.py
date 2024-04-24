#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from typing import List, Optional
from copy import deepcopy
from lxml.etree import SubElement, Element
from .Mixins import RootMixin, XMixin, YMixin


class Point(XMixin, YMixin):
    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Item")
        super().__init__(root, *args, **kwargs)

    @property
    def flip_y(self):
        result = deepcopy(self)
        result.y = -self.y
        return result

    @property
    def flip_x(self):
        result = deepcopy(self)
        result.x = -self.x
        return result

    @property
    def flip_xy(self):
        result = deepcopy(self)
        result.x = -self.x
        result.y = -self.y
        return result


class PointsMixin(RootMixin):
    @property
    def points(self) -> Optional[List[Point]]:
        if (tag := self._root.find("./Points")) is not None:
            return [Point(x) for x in tag.findall("./Item")]
        return None

    @points.setter
    def points(self, value: Optional[List[Point]]):
        if (tag := self._root.find("./Points")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Points")
            for point in value:
                tag.append(deepcopy(point.root))


if __name__ == "__main__":
    pass
