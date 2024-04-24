#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional
from copy import deepcopy
from .Mixins import RootMixin, XMixin, YMixin, ZMixin
from .Enums import Boolean, Units3D, Model3DType
from .Filename import FilenameMixin


class Rotate(XMixin, YMixin, ZMixin):
    pass


class Offset(XMixin, YMixin, ZMixin):
    pass


class Zoom(XMixin, YMixin, ZMixin):
    pass


class Model3D(FilenameMixin):
    @property
    def type(self) -> Optional[Model3DType]:
        try:
            return Model3DType(self._root.get("Type"))
        except (ValueError, TypeError):
            return None

    @type.setter
    def type(self, value: Optional[Model3DType] = None) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        elif "Type" in self._root.attrib:
            self._root.attrib.pop("Type")

    @property
    def mirror(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("Mirror"))
        except (ValueError, TypeError):
            return None

    @mirror.setter
    def mirror(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("Mirror", value.value)
        elif "Mirror" in self._root.attrib:
            self._root.attrib.pop("Mirror")

    @property
    def no_search(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("NoSearch"))
        except (ValueError, TypeError):
            return None

    @no_search.setter
    def no_search(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("NoSearch", value.value)
        elif "NoSearch" in self._root.attrib:
            self._root.attrib.pop("NoSearch")

    @property
    def keep_pins(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("KeepPins"))
        except (ValueError, TypeError):
            return None

    @keep_pins.setter
    def keep_pins(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("KeepPins", value.value)
        elif "KeepPins" in self._root.attrib:
            self._root.attrib.pop("KeepPins")

    @property
    def auto_height(self) -> Optional[float]:
        try:
            return float(self._root.get("AutoHeight"))
        except (ValueError, TypeError):
            return None

    @auto_height.setter
    def auto_height(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("AutoHeight", f"{value:.5g}")
        elif "AutoHeight" in self._root.attrib:
            self._root.attrib.pop("AutoHeight")

    @property
    def auto_color(self) -> Optional[int]:
        try:
            return int(self._root.get("AutoColor"))
        except (ValueError, TypeError):
            return None

    @auto_color.setter
    def auto_color(self, value: Optional[int] = None) -> None:
        if value is not None:
            self._root.set("AutoColor", str(value))
        elif "AutoColor" in self._root.attrib:
            self._root.attrib.pop("AutoColor")

    @property
    def units(self) -> Optional[Units3D]:
        try:
            return Units3D(self._root.get("Units"))
        except (ValueError, TypeError):
            return None

    @units.setter
    def units(self, value: Optional[Units3D] = None) -> None:
        if value is not None:
            self._root.set("Units", value.value)
        elif "Units" in self._root.attrib:
            self._root.attrib.pop("Units")

    @property
    def x_offset(self) -> Optional[float]:
        try:
            return float(self._root.get("IPC_XOff"))
        except TypeError:
            return None

    @x_offset.setter
    def x_offset(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("IPC_XOff", f"{value:.6g}")
        elif "IPC_XOff" in self._root.attrib:
            self._root.attrib.pop("IPC_XOff")

    @property
    def y_offset(self) -> Optional[float]:
        try:
            return float(self._root.get("IPC_YOff"))
        except TypeError:
            return None

    @y_offset.setter
    def y_offset(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("IPC_YOff", f"{value:.6g}")
        elif "IPC_YOff" in self._root.attrib:
            self._root.attrib.pop("IPC_YOff")

    @property
    def rotate(self) -> Optional[Rotate]:
        if (tag := self._root.find("Rotate")) is not None:
            return Rotate(tag)
        return None

    @rotate.setter
    def rotate(self, value: Optional[Rotate] = None) -> None:
        for tag in self._root.findall("./Rotate"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))

    @property
    def offset(self) -> Optional[Rotate]:
        if (tag := self._root.find("Offset")) is not None:
            return Rotate(tag)
        return None

    @offset.setter
    def offset(self, value: Optional[Rotate] = None) -> None:
        for tag in self._root.findall("./Offset"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))

    @property
    def zoom(self) -> Optional[Zoom]:
        if (tag := self._root.find("Zoom")) is not None:
            return Zoom(tag)
        return None

    @zoom.setter
    def zoom(self, value: Optional[Zoom] = None) -> None:
        for tag in self._root.findall("./Zoom"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


class Model3DMixin(RootMixin):
    @property
    def model3d(self) -> Optional[Model3D]:
        if (tag := self._root.find("./Model3D")) is not None:
            return Model3D(tag)
        return None

    @model3d.setter
    def model3d(self, value: Optional[Model3D] = None) -> None:
        for tag in self._root.findall("./Model3D"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
