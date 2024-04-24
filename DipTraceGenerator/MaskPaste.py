#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional, List
from copy import deepcopy
from lxml.etree import Element, SubElement
from .Mixins import RootMixin, Order
from .Enums import MaskType, PasteType

# <MaskPaste TopMask="Open" BotMask="Tented" TopPaste="No Solder" BotPaste="Solder"
# CustomSwell="0.05" CustomShrink="0.1"/>

# <MaskPaste TopMask="By Paste" BotMask="By Paste" TopPaste="Segments" BotPaste="Segments"
# Segment_Percent="50" Segment_EdgeGap="0.3" Segment_Gap="0.2" Segment_Side="1">
#   <TopSegments>
#     <Item X1="-0.53" Y1="0.53" X2="0.53" Y2="-0.53"/>
#   </TopSegments>
#   <BotSegments>
#     <Item X1="-0.53" Y1="0.53" X2="0.53" Y2="-0.53"/>
#   </BotSegments>
# </MaskPaste>


class Segment(RootMixin):
    _order = Order(args=["X1", "Y1", "X2", "Y2"])

    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Item")
        super().__init__(root, *args, **kwargs)

    @property
    def x1(self) -> Optional[float]:
        try:
            return float(self._root.get("X1"))
        except (ValueError, TypeError):
            return None

    @x1.setter
    def x1(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("X1", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "X1" in self._root.attrib:
            self._root.attrib.pop("X1")

    @property
    def y1(self) -> Optional[float]:
        try:
            return float(self._root.get("Y1"))
        except (ValueError, TypeError):
            return None

    @y1.setter
    def y1(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Y1", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "Y1" in self._root.attrib:
            self._root.attrib.pop("Y1")

    @property
    def x2(self) -> Optional[float]:
        try:
            return float(self._root.get("X2"))
        except (ValueError, TypeError):
            return None

    @x2.setter
    def x2(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("X2", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "X2" in self._root.attrib:
            self._root.attrib.pop("X2")

    @property
    def y2(self) -> Optional[float]:
        try:
            return float(self._root.get("Y2"))
        except (ValueError, TypeError):
            return None

    @y2.setter
    def y2(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Y2", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "Y2" in self._root.attrib:
            self._root.attrib.pop("Y2")


class MaskPaste(RootMixin):
    @property
    def top_mask(self) -> Optional[MaskType]:
        try:
            return MaskType(self._root.get("TopMask"))
        except (AttributeError, ValueError, TypeError):
            return None

    @top_mask.setter
    def top_mask(self, value: Optional[MaskType]) -> None:
        if value is not None and value.value is not None:
            self._root.set("TopMask", value.value)
        elif "TopMask" in self._root.attrib:
            self._root.attrib.pop("TopMask")

    @property
    def bottom_mask(self) -> Optional[MaskType]:
        try:
            return MaskType(self._root.get("BotMask"))
        except (AttributeError, ValueError, TypeError):
            return None

    @bottom_mask.setter
    def bottom_mask(self, value: Optional[MaskType]) -> None:
        if value is not None and value.value is not None:
            self._root.set("BotMask", value.value)
        elif "BotMask" in self._root.attrib:
            self._root.attrib.pop("BotMask")

    @property
    def top_paste(self) -> Optional[PasteType]:
        try:
            return PasteType(self._root.get("TopPaste"))
        except (AttributeError, ValueError, TypeError):
            return None

    @top_paste.setter
    def top_paste(self, value: Optional[PasteType]) -> None:
        if value is not None:
            self._root.set("TopPaste", value.value)
        elif "TopPaste" in self._root.attrib:
            self._root.attrib.pop("TopPaste")

    @property
    def bottom_paste(self) -> Optional[PasteType]:
        try:
            return PasteType(self._root.get("BotPaste"))
        except (AttributeError, ValueError, TypeError):
            return None

    @bottom_paste.setter
    def bottom_paste(self, value: Optional[PasteType]) -> None:
        if value is not None:
            self._root.set("BotPaste", value.value)
        elif "BotPaste" in self._root.attrib:
            self._root.attrib.pop("BotPaste")

    @property
    def top_segments(self) -> List[Segment]:
        return [Segment(x) for x in self._root.findall("./TopSegments/Item")]

    @top_segments.setter
    def top_segments(self, value: Optional[Segment]) -> None:
        for tag in self._root.findall("./TopSegments"):
            self._remove(tag)
        if value is not None:
            tag = SubElement(self._root, "TopSegments")
            for segment in value:
                tag.append(deepcopy(segment.root))

    @property
    def bottom_segments(self) -> List[Segment]:
        return [Segment(x) for x in self._root.findall("./BotSegments/Item")]

    @bottom_segments.setter
    def bottom_segments(self, value: Optional[Segment]) -> None:
        for tag in self._root.findall("./BotSegments"):
            self._remove(tag)
        if value is not None:
            tag = SubElement(self._root, "BotSegments")
            for segment in value:
                tag.append(deepcopy(segment.root))

    @property
    def segment_percent(self) -> Optional[float]:
        try:
            return float(self._root.get("Segment_Percent"))
        except (ValueError, TypeError):
            return None

    @segment_percent.setter
    def segment_percent(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Segment_Percent", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "Segment_Percent" in self._root.attrib:
            self._root.attrib.pop("Segment_Percent")

    @property
    def segment_edge_gap(self) -> Optional[float]:
        try:
            return float(self._root.get("Segment_EdgeGap"))
        except (ValueError, TypeError):
            return None

    @segment_edge_gap.setter
    def segment_edge_gap(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Segment_EdgeGap", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "Segment_EdgeGap" in self._root.attrib:
            self._root.attrib.pop("Segment_EdgeGap")

    @property
    def segment_gap(self) -> Optional[float]:
        try:
            return float(self._root.get("Segment_Gap"))
        except (ValueError, TypeError):
            return None

    @segment_gap.setter
    def segment_gap(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Segment_Gap", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "Segment_Gap" in self._root.attrib:
            self._root.attrib.pop("Segment_Gap")

    @property
    def segment_side(self) -> Optional[float]:
        try:
            return float(self._root.get("Segment_Side"))
        except (ValueError, TypeError):
            return None

    @segment_side.setter
    def segment_side(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Segment_Side", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "Segment_Side" in self._root.attrib:
            self._root.attrib.pop("Segment_Side")

    @property
    def swell(self) -> Optional[float]:
        try:
            return float(self._root.get("CustomSwell"))
        except (ValueError, TypeError):
            return None

    @swell.setter
    def swell(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("CustomSwell", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "CustomSwell" in self._root.attrib:
            self._root.attrib.pop("CustomSwell")

    @property
    def shrink(self) -> Optional[float]:
        try:
            return float(self._root.get("CustomShrink"))
        except (ValueError, TypeError):
            return None

    @shrink.setter
    def shrink(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("CustomShrink", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "CustomShrink" in self._root.attrib:
            self._root.attrib.pop("CustomShrink")


if __name__ == "__main__":
    pass
