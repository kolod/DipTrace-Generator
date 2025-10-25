#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Pattern-specific enumerations for DipTrace pattern libraries."""

from enum import Enum


class ShapeType(str, Enum):
    """Shape types supported in Pattern libraries (no Arrow)"""
    Line = "Line"
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
