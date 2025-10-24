#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


"""DipTrace Pattern Library classes."""

from .Shape import Shape
from .Pad import Pad
from .CategoryType import CategoryType
from .Origin import Origin
from .MainStack import MainStack
from .MaskPaste import MaskPaste, SegmentItem
from .PadStyle import PadStyle
from .Model3D import Model3D, Filename, Rotate, Offset, Zoom

__all__ = [
    'Shape',
    'Pad',
    'CategoryType',
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
    # 'Library',  # To be added when Pattern.Library is implemented
    # 'Pattern',  # To be added
]
