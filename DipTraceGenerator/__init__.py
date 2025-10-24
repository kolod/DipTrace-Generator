#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""
DipTrace Generator - Python library for generating DipTrace component and pattern libraries.

This package provides classes and utilities for creating and manipulating DipTrace
library files programmatically.

Usage:
    # Import submodules for namespaced access (recommended to avoid conflicts)
    from DipTraceGenerator import Component, Pattern
    comp_lib = Component.Library(name="My Components")
    pattern_lib = Pattern.Library(name="My Patterns")
    
    # Or import specific classes
    from DipTraceGenerator.Component import Library as ComponentLibrary
    from DipTraceGenerator.Pattern import Library as PatternLibrary
"""

__version__ = "0.2.0"

# Core utilities
from DipTraceGenerator.Units import Units, convert_units
from DipTraceGenerator.Point import Point

# Enums
from DipTraceGenerator.Enums import (
    Boolean,
    HorizontalAlign,
    VerticalAlign,
    TextAlign,
    TextShow,
    ShapeType,
    PinType,
    ElectricType,
    PartType,
    ShowNumbers,
    ComponentType,
    SpiceModelType,
)

# Import submodules as namespaces to avoid conflicts between Component.Library and Pattern.Library
from DipTraceGenerator import Component
from DipTraceGenerator import Pattern

# Declare public API
__all__ = [
    # Version
    '__version__',
    
    # Core utilities
    'Units',
    'convert_units',
    'Point',
    
    # Enums
    'Boolean',
    'HorizontalAlign',
    'VerticalAlign',
    'TextAlign',
    'TextShow',
    'ShapeType',
    'PinType',
    'ElectricType',
    'PartType',
    'ShowNumbers',
    'ComponentType',
    'SpiceModelType',
    
    # Submodules (namespaces for Component and Pattern libraries)
    'Component',
    'Pattern',
]

