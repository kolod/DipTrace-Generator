#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from pathlib import Path
from lxml.etree import Element, parse

try:
    from typing import Self  # python>=3.11
except ImportError:
    from typing_extensions import Self  # python<3.11

from .Mixins import *
from .Pattern import PatternsMixin
from .PadStyle import PadStylesMixin
from .Category import CategoriesMixin


class PatternLibrary(NameMixin, HintMixin, VersionMixin, UnitsMixin, PatternsMixin, PadStylesMixin, CategoriesMixin):
    extension: str = ".libxml"
    _order = Order(args=["Type", "Hint", "Version", "Units"], subs=["patterns"])

    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element("Library")
            root.set("Type", "DipTrace-PatternLibrary")
            root.set("Version", "4.3.0.5")
            root.set("Units", "mm")

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

        if root.tag != 'Library':
            raise ValueError(f"File `{path.absolute()}` isn't DipTrace Library.")

        lib_type = root.get('Type')
        if (not isinstance(lib_type, str)) or (lib_type != "DipTrace-PatternLibrary"):
            raise ValueError(f"File `{path.absolute()}` isn't DipTrace Pattern Library.")

        return PatternLibrary(root)

    def __str__(self) -> str:
        # Remove the unneeded whitespaces
        for element in self._root.iter():
            if not isinstance(element.text, type(None)):
                element.text = element.text.strip()
                if element.text == "":
                    element.text = "\n"

        return tostring(self._root, xml_declaration=True, pretty_print=True, encoding="utf-8").decode("utf-8")

    def save(self, path: Path) -> Self:
        if path.suffix != self.extension:
            path = path.with_suffix(self.extension)
        if self.root is not None:
            with open(path, "w", encoding="utf-8") as datafile:
                datafile.write(str(self))
        return self


if __name__ == "__main__":
    pass
