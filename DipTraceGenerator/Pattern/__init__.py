#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


"""DipTrace Pattern Library classes."""

from .Shape import Shape
from .Pad import Pad
from .Origin import Origin
from .MainStack import MainStack
from .MaskPaste import MaskPaste, SegmentItem
from .PadStyle import PadStyle
from .Model3D import Model3D, Filename, Rotate, Offset, Zoom
from .Category import Category
from .Pattern import Pattern
from .Library import Library
from .Enums import ShapeType, Layer, TextShow, Side, MaskSetting, PasteSetting, PadStackShape, \
    Model3DType, Model3DUnits, PadType, HoleType, PadSide

__all__ = [
    'Shape',
    'ShapeType',
    'Layer',
    'TextShow',
    'Side',
    'Pad',
    'Origin',
    'MainStack',
    'MaskPaste',
    'SegmentItem',
    'PadStyle',
    'Model3D',
    'Filename',
    'Rotate',
    'Offset',
    'Zoom',
    'Category',
    'Pattern',
    'Library',
    'MaskSetting',
    'PasteSetting',
    'PadStackShape',
    'Model3DType',
    'Model3DUnits',
    'PadType',
    'HoleType',
    'PadSide',
]