#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

__version__ = "0.1.0"

from DipTraceGenerator.Utils import get_correct_filename, format_xml, compare, load_from_xml_file
from DipTraceGenerator.PatternLibrary import PatternLibrary
from DipTraceGenerator.ComponentLibrary import ComponentLibrary
from DipTraceGenerator.Enums import *
from DipTraceGenerator.PatternOrigin import PatternOrigin
from DipTraceGenerator.PatternShape import PatternShape
from DipTraceGenerator.Model3D import Model3D, Rotate, Offset, Zoom
from DipTraceGenerator.Pattern import Pattern
from DipTraceGenerator.Point import Point
from DipTraceGenerator.Filename import Filename
from DipTraceGenerator.MainStack import MainStack
from DipTraceGenerator.Pad import Pad
from DipTraceGenerator.PadStyle import PadStyle
from DipTraceGenerator.Dimension import Dimension
from DipTraceGenerator.Category import Category, CategoryType
from DipTraceGenerator.Terminal import Terminal
from DipTraceGenerator.RecoveryCode import RecoveryCode
from DipTraceGenerator.ComponentOrigin import ComponentOrigin
from DipTraceGenerator.ComponentShape import ComponentShape
from DipTraceGenerator.Pin import Pin, Shift
from DipTraceGenerator.RecoveryCode import RecoveryCode
from DipTraceGenerator.SpiceModel import SpiceModel, SpiceModelType
from DipTraceGenerator.Component import Component
from DipTraceGenerator.Part import Part
from DipTraceGenerator.Group import Group
from DipTraceGenerator.NameFont import NameFont
from DipTraceGenerator.MaskPaste import MaskPaste, Segment


if __name__ == "__main__":
    pass
