#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from copy import deepcopy
from typing import Optional
from pathlib import Path
from lxml.etree import SubElement
from .Mixins import RootMixin


class Filename(RootMixin):
    @property
    def path(self) -> Optional[Path]:
        try:
            return Path(self._root.find("Path").text)
        except (TypeError, ValueError, AttributeError):
            return None

    @path.setter
    def path(self, value: Optional[Path]) -> None:
        for tag in self._root.findall("Path"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Path")
            tag.text = value

    @property
    def variant(self) -> Optional[Path]:
        try:
            return Path(self._root.find("Var").text)
        except (TypeError, ValueError, AttributeError):
            return None

    @variant.setter
    def variant(self, value: Optional[Path]) -> None:
        for tag in self._root.findall("Var"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Var")
            tag.text = value


class FilenameMixin(RootMixin):
    @property
    def filename(self) -> Optional[Filename]:
        if (tag := self._root.find("Filename")) is not None:
            return Filename(tag)
        return None

    @filename.setter
    def filename(self, value: Optional[Filename] = None) -> None:
        for tag in self._root.findall("Filename"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
