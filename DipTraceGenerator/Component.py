#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

try:
    from typing import Self  # python>=3.11
except ImportError:
    from typing_extensions import Self  # type: ignore # python<3.11
from typing import Optional, List
from lxml.etree import SubElement
from copy import deepcopy
from DipTraceGenerator.Mixins import RootMixin, Order, IdMixin
from DipTraceGenerator.Part import Part, PartsMixin
from DipTraceGenerator.Pattern import Pattern
from DipTraceGenerator.PatternLibrary import PatternLibrary


class Component(PartsMixin, IdMixin):
    _order = Order(subs=["parts"])

    @property
    def name(self) -> Optional[str]:
        if isinstance(self.parts, list) and len(self.parts) > 0:
            return self.parts[0].name
        return None

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if value is not None:
            if (self.parts is None) or (len(self.parts) < 1):
                self.parts = [Part()]
            self.parts[0].name = value

    @property
    def pattern(self) -> Optional[Pattern]:
        if isinstance(self.parts, list) and len(self.parts) > 0:
            if (pattern_style := self.parts[0].pattern) is not None:
                if (tag := self._root.getroottree().find("./Library")) is not None:
                    return PatternLibrary(tag).find(pattern_style)
        return None

    @pattern.setter
    def pattern(self, value: Optional[str]) -> None:
        if value is not None:
            if (self.parts is None) or (len(self.parts) < 1):
                self.parts = [Part()]
            self.parts[0].pattern = value


class ComponentsMixin(RootMixin):
    @property
    def components(self) -> List[Component]:
        return [Component(x) for x in self._root.findall("./Components/Component")]

    @components.setter
    def components(self, value: Optional[List[Component]]):
        if (tag := self._root.find("./Components")) is not None:
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Components")
            for component in value:
                tag.append(deepcopy(component.root))

    def find(self, name: str) -> Optional[Component]:
        """
        Find component by its name.
        
        Args:
            name (str): Component name.

        Returns:
            Component or None if not found.
        """
        for tag in self._root.findall("./Components/Component/Part/Name"):
            if tag.text == name:
                return Component(tag.getparent().getparent())
        return None
    
    def renumerate_ids(self) -> Self:
        """
        Renumerate component IDs starting from 0.

        Returns:
            Self
        """
        for i, component in enumerate(self.components, start=0):
            component.id = i
        return self


if __name__ == "__main__":
    pass
