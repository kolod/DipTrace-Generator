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


class Layer(str, Enum):
    """Layer types for Pattern shapes"""
    TopSilk = "Top Silk"
    TopAssy = "Top Assy"
    TopMask = "Top Mask"
    TopPaste = "Top Paste"
    BottomPaste = "Bottom Paste"
    BottomMask = "Bottom Mask"
    BottomAssy = "Bottom Assy"
    BottomSilk = "Bottom Silk"
    Top = "Top"
    TopKeepout = "Top Keepout"
    BottomKeepout = "Bottom Keepout"
    Bottom = "Bottom"
    BoardCutout = "Board Cutout"
    TopDimension = "Top Dimension"
    BottomDimension = "Bottom Dimension"
    NonSignal = "Non-Signal"
    TopCourtyard = "Top Courtyard"
    BottomCourtyard = "Bottom Courtyard"
    TopOutline = "Top Outline"
    BottomOutline = "Bottom Outline"
    TopTerminals = "Top Terminals"
    BottomTerminals = "Bottom Terminals"


class TextShow(str, Enum):
    """Text display options for Pattern text shapes"""
    AnyText = "Any Text"
    Name = "Name"
    RefDes = "RefDes"
    Value = "Value"
    Manufacturer = "Manufacturer"
    UniqueName = "Unique Name"
    Datasheet = "Datasheet"


if __name__ == "__main__":
    pass  # pragma: no cover
