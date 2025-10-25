#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


"""DipTrace Component Library classes."""

from .Origin import Origin
from .Group import Group
from .SpiceModel import SpiceModel, SpiceModelType
from .Pin import Pin, PinType, ElectricType
from .Shape import Shape
from .Part import Part, PartType
from .Component import Component
from .Library import Library, Category, Type, SubType
from .Enums import ShapeType

__all__ = [
    'Origin',
    'Group',
    'SpiceModel',
    'SpiceModelType',
    'Pin',
    'PinType',
    'ElectricType',
    'Shape',
    'ShapeType',
    'Part',
    'PartType',
    'Component',
    'Library',
    'Category',
]
