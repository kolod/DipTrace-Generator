#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from enum import Enum


class Boolean(str, Enum):
    Yes = "Y"
    No = "N"


class HorizontalAlign(str, Enum):
    Left = "Left"
    Center = "Center"
    Right = "Right"


class VerticalAlign(str, Enum):
    Top = "Top"
    Center = "Center"
    Bottom = "Bottom"


class TextAlign(str, Enum):
    Left = "Left"
    Center = "Center"
    Right = "Right"


class TextShow(str, Enum):
    AnyText = "Any Text"
    RefDes = "RefDes"
    PartType = "Part Type"
    Value = "Value"
    Comment = "Comment"


class PinType(str, Enum):
    Default = "Default"
    Dot = "Dot"
    PolarityIn = "Polarity In"
    PolarityOut = "Polarity Out"
    NonLogic = "Non Logic"
    Open = "Open"
    OpenLow = "Open Low"
    ThreeState = "3 State"
    Hysteresis = "Hysteresis"
    Amplifier = "Amplifier"
    Postponed = "Postponed"
    Shift = "Shift"
    Clock = "Clock"
    Generator = "Generator"


class ElectricType(str, Enum):
    Undefined = "Undefined"
    Passive = "Passive"
    Input = "Input"
    Output = "Output"
    Bidirectional = "Bidirectional"
    OpenHigh = "Open High"
    OpenLow = "Open Low"
    PassiveHigh = "Passive High"
    PassiveLow = "Passive Low"
    ThreeState = "3 State"
    Power = "Power"


class PartType(str, Enum):
    """Enumeration of part types"""
    Normal = "Normal"
    Power = "Power"
    Ground = "Ground"


class ShowNumbers(str, Enum):
    """Enumeration of show numbers options"""
    Hide = "Hide"
    Show = "Show"
    Auto = "Auto"


class ComponentType(str, Enum):
    """Enumeration of component types"""
    Free = "Free"
    Fixed = "Fixed"


class SpiceModelType(str, Enum):
    """Enumeration of SPICE model types"""
    SubCkt = "SubCkt"
    Model = "Model"
    

if __name__ == "__main__":
    pass  # pragma: no cover