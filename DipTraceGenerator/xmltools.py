#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # static type checkers get correct types
    from lxml import etree as etree  # type: ignore
    from lxml.builder import E as E  # type: ignore
    from dataclasses import dataclass as dataclass, field as field # type: ignore
    from enum import Enum as Enum  # type: ignore
else:
    from dataclasses import dataclass, field
    from lxml import etree
    from lxml.builder import E
    from enum import Enum

__all__ = ["etree", "E", "dataclass", "field", "Enum"]

if __name__ == "__main__":
    pass