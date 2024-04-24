#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import List, Optional, Union
from copy import deepcopy
from lxml.etree import SubElement
from .Mixins import (
    RootMixin,
    WidthMixin,
    HeightMixin,
    NameTagMixin,
    NameDescriptionTagMixin,
    RefDesMixin,
    ManufacturerTagMixin,
    ValueTagMixin,
    NameUniqueTagMixin,
    DatasheetTagMixin,
    OrientationMixin,
    Order,
)

try:
    from typing import Self  # python>=3.11
except ImportError:
    from typing_extensions import Self  # python<3.11

from .Pad import PadsMixin
from .PatternOrigin import PatternOriginMixin
from .Model3D import Model3DMixin
from .PatternShape import PatternShapesMixin
from .Hole import HolesMixin
from .RecoveryCode import RecoveryCodeMixin
from .Enums import Boolean, PatternType, PatternMounting


class Pattern(
    RefDesMixin,
    WidthMixin,
    HeightMixin,
    NameTagMixin,
    NameDescriptionTagMixin,
    PadsMixin,
    PatternOriginMixin,
    Model3DMixin,
    ValueTagMixin,
    NameUniqueTagMixin,
    DatasheetTagMixin,
    ManufacturerTagMixin,
    OrientationMixin,
    PatternShapesMixin,
    HolesMixin,
    RecoveryCodeMixin,
):
    _order = Order(
        args=[
            "PatternStyle",
            "RefDes",
            "Mounting",
            "Width",
            "Height",
            "Orientation",
            "LockTypeChange",
            "Type",
            "Float1",
            "Float2",
            "Float3",
            "Int1",
            "Int2",
        ],
        tags=["Name", "Name_Description", "Category", "Origin", "RecoveryCode", "DefPad", "Pads", "Shapes", "Model3D"],
    )

    @property
    def mounting(self) -> Optional[PatternMounting]:
        try:
            return PatternMounting(self._root.get("Mounting"))
        except (AttributeError, ValueError, TypeError):
            return None

    @mounting.setter
    def mounting(self, value: Optional[PatternMounting]) -> None:
        if value is not None:
            self._root.set("Mounting", value.value)
        elif "Mounting" in self._root.attrib:
            self._root.attrib.pop("Mounting")

    @property
    def default_pad_style(self) -> Optional[str]:
        if (tag := self._root.find("DefPad")) is not None:
            return tag.get("Style")
        else:
            return None

    @default_pad_style.setter
    def default_pad_style(self, value: Optional[str]) -> None:
        for tag in self._root.findall("./DefPad"):
            self._root.remove(tag)
        if value is not None:
            SubElement(self._root, "DefPad").set("Style", value)

    @property
    def locked(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("LockTypeChange"))
        except (ValueError, TypeError):
            return None

    @locked.setter
    def locked(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("LockTypeChange", value.value)
        else:
            self._root.attrib.pop("LockTypeChange")

    @property
    def type(self) -> Optional[PatternType]:
        try:
            return PatternType(self._root.get("Type"))
        except (ValueError, TypeError):
            return None

    @type.setter
    def type(self, value: Optional[PatternType]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        else:
            self._root.attrib.pop("Type")

    @property
    def parameters(self) -> List[Union[float, int]]:
        try:
            result = []
            for i in range(3):
                if (value := self._root.get(f"Float{i + 1}")) is not None:
                    result.append(float(value))
            for i in range(2):
                if (value := self._root.get(f"Int{i + 1}")) is not None:
                    result.append(int(value))
            return result
        except (ValueError, TypeError):
            return []

    @parameters.setter
    def parameters(self, value: List[Union[float, int]]):
        for i, v in enumerate([v for v in value if isinstance(v, float)]):
            self._root.set(f"Float{i + 1}", f"{v:.5g}")
        for i, v in enumerate([v for v in value if isinstance(v, int)]):
            self._root.set(f"Int{i + 1}", str(v))

    @property
    def style(self) -> Optional[str]:
        return self._root.get("PatternStyle")

    @style.setter
    def style(self, value: Optional[str]) -> None:
        if "PatternStyle" in self._root.attrib:
            self._root.attrib.pop("PatternStyle")
        if value is not None:
            self._root.set("PatternStyle", value)

    @property
    def category(self) -> Optional[int]:
        try:
            if (tag := self._root.find("Category")) is not None:
                return int(tag.get("Index"))
            return None
        except (TypeError, ValueError, AttributeError):
            return None

    @category.setter
    def category(self, value: Optional[int]) -> None:
        for tag in self._root.findall("./Category"):
            self._root.remove(tag)
        if value is not None:
            SubElement(self._root, "Category").set("Index", str(value))


class PatternsMixin(RootMixin):
    @property
    def patterns(self) -> Optional[List[Pattern]]:
        return [Pattern(x) for x in self._root.findall("./Patterns/Pattern")]

    @patterns.setter
    def patterns(self, value: Optional[List[Pattern]]):
        if (tag := self._root.find("./Patterns")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Patterns")
            for pattern in value:
                tag.append(deepcopy(pattern.root))

    def renumerate_styles(self) -> Self:
        for i, pattern in enumerate(self.patterns, start=0):
            pattern.style = f"PatType{i}"
        return self

    def find(self, name: str) -> Optional[Pattern]:
        if name.startswith("PatType"):
            for tag in self._root.findall("./Patterns/Pattern"):
                if tag.get("PatternStyle") == name:
                    return Pattern(tag)
        else:
            for tag in self._root.findall("./Patterns/Pattern/Name"):
                if tag.text == name:
                    return Pattern(tag.getparent())
        return None


if __name__ == "__main__":
    pass
