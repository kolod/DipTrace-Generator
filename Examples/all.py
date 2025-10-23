#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from Examples.Diodes_LED import diodes_led
from Examples.Diodes_TVS import diodes_tvs
from Examples.Capacitors import capacitors
from Examples.Resistors import resistors


def main():
    diodes_led()
    diodes_tvs()
    resistors()
    capacitors()
