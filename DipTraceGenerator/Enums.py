#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from enum import Enum


class Boolean(Enum):
    No = "N"
    Yes = "Y"


class Visible(Enum):
    Hide = "Hide"
    Show = "Show"


class Units(Enum):
    mm = "mm"
    mil = "mil"
    inch = "inch"
    default = mm


class Units3D(Enum):
    wings = "Wings"
    mm = "mm"
    mil = "mil"
    inch = "inch"
    default = mm


class Model3DType(Enum):
    IPC_7351 = "IPC-7351"
    File = "File"
    Outline = "Outline"


class MountType(Enum):
    Surface = "Surface"
    ThroughHole = "Through"


class Side(Enum):
    Top = "Top"
    Bottom = "Bottom"


class MainStackShape(Enum):
    Rectangle = "Rectangle"
    Obround = "Obround"
    Polygon = "Polygon"
    Ellipse = "Ellipse"
    DShape = "D-shape"


class TerminalShape(Enum):
    Rectangle = "Rectangle"
    Obround = "Obround"
    Polygon = "Polygon"
    DShape = "D-shape"


class PatternType(Enum):
    Free = "Free"
    IPC_7351 = "IPC-7351"
    Circle = "Circle"
    Lines = "Lines"
    Square = "Square"
    Matrix = "Matrix"
    Rectangle = "Rectangle"
    ZigZag = "Zig-Zag"


class ShapeType(Enum):
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


class Layer(Enum):
    Top = "Top"
    TopDimension = "Top Dimension"
    TopAssembly = "Top Assy"
    TopSilk = "Top Silk"
    TopOutline = "Top Outline"
    TopCourtyard = "Top Courtyard"
    TopKeepout = "Top Keepout"
    TopMask = "Top Mask"
    TopPaste = "Top Paste"
    Bottom = "Bottom"
    BottomAssembly = "Bottom Assy"
    BottomSilk = "Bottom Silk"
    BottomOutline = "Bottom Outline"
    BottomCourtyard = "Bottom Courtyard"
    BottomKeepout = "Bottom Keepout"
    BottomMask = "Bottom Mask"
    BottomPaste = "Bottom Paste"
    BottomDimension = "Bottom Dimension"
    BoardCutout = "Board Cutout"


class DimensionType(Enum):
    Horizontal = "Horizontal"
    Vertical = "Vertical"
    Free = "Free"
    Radius = "Radius"
    Pointer = "Pointer"


class HoleType(Enum):
    Round = "Round"
    Obround = "Obround"


class FontWidth(Enum):
    Thin = -3
    Normal = -2
    Bold = -1


class PointerMode(Enum):
    Coordinates = 0
    Comment = 1


class HorizontalAlignment(Enum):
    Center = "Center"
    Left = "Left"
    Right = "Right"


class VerticalAlignment(Enum):
    Center = "Center"
    Top = "Top"
    Bottom = "Bottom"


class PatternMounting(Enum):
    Default = "None"
    SMD = "SMD"
    Through = "Through"


class PinType(Enum):
    Default = "Default"
    Dot = "Dot"
    PolarityIn = "Polarity In"
    PolarityOut = "Polarity Out"
    NonLogic = "Non Logic"
    Open = "Open"
    OpenHigh = "Open High"
    ThreeState = "3 State"
    Hysteresis = "Hysteresis"
    Amplifier = "Amplifier"
    Postponed = "Postponed"
    Shift = "Shift"
    Clock = "Clock"
    Generator = "Generator"


class ElectricType(Enum):
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


class SpiceModelType(Enum):
    SubCkt = "SubCkt"
    Resistor = "Resistor"
    Capacitor = "Capacitor"
    Inductor = "Inductor"
    Diode = "Diode"
    BJT = "BJT"
    JFET = "JFET"
    MOSFET = "MOSFET"
    GaAsTransistor = "Ga As Transistor"
    CurrentSource = "Current Source"
    VoltageSource = "Voltage Source"
    VoltageDependentCurrentSource = "Voltage Dependent Current Source"
    VoltageDependentVoltageSource = "Voltage Dependent Voltage Source"
    CurrentDependentCurrentSource = "Current Dependent Current Source"
    CurrentDependentVoltageSource = "Current Dependent Voltage Source"
    ArbitraryBehavioralSource = "Arbitrary Behavioral Source"
    MutualInductance = "Mutual Inductance"
    TransmissionLine = "Transmission Line"


class PartType(Enum):
    Normal = "Normal"
    Power = "Power"
    NetPort = "Net Port"


class PartStyle(Enum):
    Free = "Free"
    TwoSides = "2 Sides"
    ChipTwoSides = "IC-2 Sides"
    ChipFourSides = "IC-4 Sides"


class TextShow(Enum):
    Text = "Any Text"
    Name = "Name"
    UniqueName = "Unique Name"
    RefDes = "RefDes"
    Value = "Value"
    Manufacturer = "Manufacturer"
    Datasheet = "Datasheet"


class MaskType(Enum):
    Common = None
    Open = "Open"
    Tented = "Tented"
    ByPaste = "By Paste"


class PasteType(Enum):
    Common = None
    NoSolder = "No Solder"
    Solder = "Solder"
    Segments = "Segments"


if __name__ == "__main__":
    pass
