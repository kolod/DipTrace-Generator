#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional, List
from lxml.etree import SubElement
from copy import deepcopy
from lxml.etree import Element
from .Mixins import (
    RootMixin,
    IdMixin,
    LockedMixin,
    AllLayersMixin,
    LayerMixin,
    FontVectorMixin,
    AngleMixin,
    FontMixin,
    LineWidthMixin,
)
from .Point import PointsMixin
from .Enums import ShapeType, HorizontalAlignment, VerticalAlignment, TextShow


class PatternShape(
    IdMixin,
    LockedMixin,
    PointsMixin,
    AllLayersMixin,
    LayerMixin,
    FontVectorMixin,
    AngleMixin,
    FontMixin,
    LineWidthMixin,
):
    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Shape")
        super().__init__(root, *args, **kwargs)

    @property
    def type(self) -> Optional[ShapeType]:
        try:
            return ShapeType(self._root.get("Type"))
        except (KeyError, ValueError):
            return None

    @type.setter
    def type(self, value: Optional[ShapeType]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        elif "Type" in self._root.attrib:
            self._root.attrib.pop("Type")

    @property
    def horizontal_alignment(self) -> Optional[HorizontalAlignment]:
        try:
            return HorizontalAlignment(self._root.get("HorzAlign"))
        except (AttributeError, ValueError, TypeError):
            return None

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: Optional[HorizontalAlignment]) -> None:
        if value is not None:
            self._root.set("HorzAlign", value.value)
        elif "HorzAlign" in self._root.attrib:
            self._root.attrib.pop("HorzAlign")

    @property
    def vertical_alignment(self) -> Optional[VerticalAlignment]:
        try:
            return VerticalAlignment(self._root.get("VertAlign"))
        except (AttributeError, ValueError, TypeError):
            return None

    @vertical_alignment.setter
    def vertical_alignment(self, value: Optional[VerticalAlignment]) -> None:
        if value is not None:
            self._root.set("VertAlign", value.value)
        elif "VertAlign" in self._root.attrib:
            self._root.attrib.pop("VertAlign")

    @property
    def text_alignment(self) -> Optional[HorizontalAlignment]:
        try:
            return HorizontalAlignment(self._root.get("TextAlign"))
        except (AttributeError, ValueError, TypeError):
            return None

    @text_alignment.setter
    def text_alignment(self, value: Optional[HorizontalAlignment]) -> None:
        if value is not None:
            self._root.set("TextAlign", value.value)
        elif "TextAlign" in self._root.attrib:
            self._root.attrib.pop("TextAlign")

    @property
    def line_spacing(self) -> Optional[float]:
        try:
            return float(self._root.get("LineSpacing"))
        except (AttributeError, ValueError, TypeError):
            return None

    @line_spacing.setter
    def line_spacing(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("LineSpacing", f"{value:.5g}")
        elif "LineSpacing" in self._root.attrib:
            self._root.attrib.pop("LineSpacing")

    @property
    def text_show(self) -> Optional[TextShow]:
        try:
            return TextShow(self._root.get("TextShow"))
        except (AttributeError, ValueError, TypeError):
            return None

    @text_show.setter
    def text_show(self, value: Optional[TextShow]) -> None:
        if value is not None:
            self._root.set("TextShow", value.value)
        elif "TextShow" in self._root.attrib:
            self._root.attrib.pop("TextShow")

    @property
    def lines(self) -> Optional[List[str]]:
        if (tag := self._root.find("./Lines")) is not None:
            return [x.text for x in tag.findall("./Item")]
        return None

    @lines.setter
    def lines(self, value: Optional[str]) -> None:
        if (tag := self._root.find("Lines")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Lines")
            for line in value:
                SubElement(tag, "Item").text = line


class PatternShapesMixin(RootMixin):
    @property
    def shapes(self) -> List[PatternShape]:
        return [PatternShape(x) for x in self._root.findall("./Shapes/Shape")]

    @shapes.setter
    def shapes(self, value: Optional[List[PatternShape]]):
        if (tag := self._root.find("./Shapes")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Shapes")
            for shape in value:
                tag.append(deepcopy(shape.root))


if __name__ == "__main__":
    pass
