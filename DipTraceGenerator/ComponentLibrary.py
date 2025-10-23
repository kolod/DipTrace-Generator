#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

try:
    from typing import Self  # python>=3.11
except ImportError:
    from typing_extensions import Self  # type: ignore # python<3.11
from typing import Optional
from pathlib import Path
from lxml.etree import Element, fromstring, tostring, parse
from copy import deepcopy
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
        """
        Load a component library from an XML file.

        Args:
            path (Path): Path to the XML file.

        Returns:
            Self
        """
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

    
    def renumerate_all_ids(self) -> Self:
        """
        Renumerate all IDs in the library (components and their pins).

        Returns:
            Self
        """
        self.renumerate_ids()                   # renumerate component IDs
        for component in self.components:
            component.renumerate_part_ids()     # renumerate part IDs
            for part in component.parts:
                part.renumerate_pin_ids()       # renumerate pin IDs
                part.renumerate_shape_ids()     # renumerate shape IDs
        return self
    
    def sort_all(self) -> Self:
        """
        Sort all elements and attributes in the library according to their defined order.

        Returns:
            Self
        """
        self.sort()                            # sort component in library
        for component in self.components:
            component.sort()                   # sort parts in component
            for part in component.parts:
                part.sort()                    # sort part
                for pin in part.pins:
                    pin.sort()                 # sort pin attributes
                for shape in part.shapes:
                    shape.sort()               # sort shape attributes
        return self

    def save(self, path: Path) -> Self:
        """
        Save the component library to an XML file.

        Args:
            path (Path): Path to save the library file.

        Returns:
            Self
        """
        if self.root is None:
            raise ValueError("Library root is None, cannot save.")
        if path.suffix == self.extension:
            path = path.with_suffix(self.extension)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.sort_all()
        self.renumerate_all_ids()
        path.write_text(str(self), encoding="utf-8")
        return self

    @property
    def pattern_library(self) -> Optional[PatternLibrary]:
        """
        Get the pattern library associated with this component library.
        
        Returns:
            PatternLibrary or None if not found.
        """
        if (tag := self._root.find("./Library")) is not None:
            return PatternLibrary(tag)
        return None

    @pattern_library.setter
    def pattern_library(self, value: Optional[PatternLibrary]) -> None:
        """
        Set the pattern library associated with this component library.

        Args:
            value (PatternLibrary or None): The pattern library to set.
        """
        for tag in self._root.findall("./Library"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))
            lib = self.pattern_library
            lib.name = None
            lib.hint = None


if __name__ == "__main__":
    pass
