#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional, List
from lxml.etree import Element, SubElement
from copy import deepcopy
from .Mixins import RootMixin, NameTagMixin, NumberMixin, NumberTagMixin


class CategoryType(NameTagMixin, NumberMixin):
    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Type")
        super().__init__(root, *args, **kwargs)


class Category(NameTagMixin, NumberMixin):
    @property
    def types(self) -> Optional[List[CategoryType]]:
        if (tag := self._root.find("./Types")) is not None:
            return [CategoryType(x) for x in tag.findall("./Type")]
        return None

    @types.setter
    def types(self, value: Optional[List[CategoryType]]) -> None:
        if tag := self._root.find("./Types") is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Types")
            for t in value:
                tag.append(deepcopy(t.root))

    def renumerate(self) -> None:
        for i, t in enumerate(self.types):
            t.number = i


class CategoryMixin(RootMixin):
    @property
    def category(self) -> Optional[Category]:
        if (tag := self._root.find("./Category")) is not None:
            return Category(tag)
        return None

    @category.setter
    def category(self, value: Optional[Category]):
        for tag in self._root.findall("./Category"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


class CategoriesMixin(RootMixin):
    @property
    def categories(self) -> List[Category]:
        return [Category(x) for x in self._root.findall("./Categories/Category")]

    @categories.setter
    def categories(self, value: Optional[List[Category]]) -> None:
        for tag in self.root.findall("./Categories"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Categories")
            for category in value:
                tag.append(deepcopy(category.root))

    def renumerate(self) -> None:
        for i, t in enumerate(self.categories):
            t.number = i


if __name__ == "__main__":
    pass
