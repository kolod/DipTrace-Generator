#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Component-specific enumerations for DipTrace component libraries."""


from enum import Enum


class ShapeType(str, Enum):
    """Shape types supported in Component libraries"""
    Line = "Line"
    Arrow = "Arrow"
    Arc = "Arc"
    Rectangle = "Rectangle"
    FillRect = "FillRect"
    Obround = "Obround"
    FillObround = "FillObround"
    Polyline = "Polyline"
    Polygon = "Polygon"
    Text = "Text"


if __name__ == "__main__":
    pass  # pragma: no cover
