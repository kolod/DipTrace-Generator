#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from copy import deepcopy
from typing import Optional
from .Enums import Boolean
from .Mixins import RootMixin


class RecoveryCode(RootMixin):
    @property
    def generator(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("Generator"))
        except (AttributeError, ValueError, TypeError):
            return None

    @generator.setter
    def generator(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("Generator", value.value)
        elif "Generator" in self._root.attrib:
            self._root.attrib.pop("Generator")

    @property
    def model(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("Model"))
        except (AttributeError, ValueError, TypeError):
            return None

    @model.setter
    def model(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("Model", value.value)
        elif "Model" in self._root.attrib:
            self._root.attrib.pop("Model")

    @property
    def text(self) -> str:
        return self._root.text

    @text.setter
    def text(self, value: str) -> None:
        self._root.text = value


class RecoveryCodeMixin(RootMixin):
    @property
    def recovery_code(self) -> Optional[RecoveryCode]:
        if (tag := self._root.find("./RecoveryCode")) is not None:
            return RecoveryCode(tag)
        else:
            return None

    @recovery_code.setter
    def recovery_code(self, value: Optional[RecoveryCode]) -> None:
        for tag in self._root.findall("./RecoveryCode"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
