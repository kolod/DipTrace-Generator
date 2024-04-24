#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional
from pathlib import Path
from lxml.etree import Element, fromstring, tostring, parse
from copy import deepcopy

try:
    from typing import Self  # python>=3.11
except ImportError:
    from typing_extensions import Self  # python<3.11

from DipTraceGenerator.Mixins import NameMixin, HintMixin, VersionMixin, UnitsMixin, Order
from DipTraceGenerator.Component import ComponentsMixin
from DipTraceGenerator.PatternLibrary import PatternLibrary


class ComponentLibrary(NameMixin, HintMixin, VersionMixin, UnitsMixin, ComponentsMixin):
    extension: str = ".elixml"
    _order = Order(
        args=["Type", "Name", "Hint", "Version", "Units"],
        tags=["Library", "SubFolders", "Categories", "Components"],
        subs=["pattern_library", "components"],
    )

    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = fromstring('<Library Type="DipTrace-ComponentLibrary" Version="4.3.0.5" Units="mm"/>')
        super().__init__(root, *args, **kwargs)

    @classmethod
    def load(cls, path: Path) -> Self:
        if not path.is_file():
            path = path.with_suffix(cls.extension)
            if not path.is_file():
                raise ValueError(f"File `{path.absolute()}` isn't exists.")

        root = parse(path).getroot()
        if root is None:
            raise ValueError(f"File `{path.absolute()}` parsing failed.")

        if root.tag != "Library":
            raise ValueError(f"File `{path.absolute()}` isn't DipTrace Library.")

        lib_type = root.get("Type")
        if (not isinstance(lib_type, str)) or (lib_type != "DipTrace-ComponentLibrary"):
            raise ValueError(f"File `{path.absolute()}` isn't DipTrace Component Library.")

        return ComponentLibrary(root)

    def __str__(self) -> str:
        # Remove the unneeded whitespaces
        for element in self._root.iter():
            if not isinstance(element.text, type(None)):
                element.text = element.text.strip()
                if element.text == "":
                    element.text = "\n"

        return tostring(self._root, xml_declaration=True, pretty_print=True, encoding="utf-8").decode("utf-8")

    def save(self, path: Path) -> Self:
        if path.suffix == self.extension:
            path = path.with_suffix(self.extension)
        if self.root is not None:
            with open(path, "w", encoding="utf-8") as datafile:
                self.sort()
                datafile.write(str(self))
        return self

    @property
    def pattern_library(self) -> Optional[PatternLibrary]:
        if (tag := self._root.find("./Library")) is not None:
            return PatternLibrary(tag)
        return None

    @pattern_library.setter
    def pattern_library(self, value: Optional[PatternLibrary]) -> None:
        for tag in self._root.findall("./Library"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))
            lib = self.pattern_library
            lib.name = None
            lib.hint = None


if __name__ == "__main__":
    pass
