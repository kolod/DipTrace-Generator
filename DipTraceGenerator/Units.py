#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from enum import Enum


class Units(str, Enum):
    MM = "mm"
    INCH = "inch"
    MIL = "mil"


def convert_units(value: float, from_unit: Units, to_unit: Units) -> float:
    """
    Convert value from one unit to another.
    
    Args:
        value (float): The value to convert.
        from_unit (Units): The unit of the input value.
        to_unit (Units): The unit to convert the value to.

    Returns:
        float: The converted value.

    """

    # No conversion needed
    if from_unit == to_unit:
        return value

    # Convert from 'from_unit' to millimeters first
    if from_unit == Units.MM:
        value_mm = value
    elif from_unit == Units.INCH:
        value_mm = value * 25.4
    elif from_unit == Units.MIL:
        value_mm = value * 0.0254
    else:
        raise ValueError(f"Unsupported from_unit: {from_unit}")

    # Convert from millimeters to 'to_unit'
    if to_unit == Units.MM:
        return value_mm
    elif to_unit == Units.INCH:
        return value_mm / 25.4
    elif to_unit == Units.MIL:
        return value_mm / 0.0254
    else:
        raise ValueError(f"Unsupported to_unit: {to_unit}")


if __name__ == "__main__":
    pass
