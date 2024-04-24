#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from enum import Enum
from copy import deepcopy
from typing import Optional, List
from lxml.etree import SubElement
from .Mixins import RootMixin, Order


class SpiceModelType(Enum):
    SubComponent = "SubCkt"
    Capacitor = "Capacitor"
    Resistor = "Resistor"
    Inductor = "Inductor"
    Diode = "Diode"
    BJT = "BJT"
    JFET = "JFET"
    MOSFET = "MOSFET"
    GaAsTransistor = "Ga As Transistor"
    VoltageSource = "Voltage Source"
    CurrentSource = "Current Source"
    CurrentDependentVoltageSource = "Current Dependent Voltage Source"
    VoltageDependentVoltageSource = "Voltage Dependent Voltage Source"
    CurrentDependentCurrentSource = "Current Dependent Current Source"
    VoltageDependentCurrentSource = "Voltage Dependent Current Source"
    MutualInductance = "Mutual Inductance"
    ArbitraryBehavioralSource = "Arbitrary Behavioral Source"
    TransmissionLine = "Transmission Line"
    LossyTransmissionLine = "Lossy Transmission Line"
    VoltageControlledSwitch = "Voltage-Controlled Switch"
    CurrentControlledSwitch = "Current-Controlled Switch"
    UniformlyDistributedRCLine = "Uniformly Distributed RC Line"


class SpiceModel(RootMixin):
    _order = Order(tags=["Model", "Details"])

    @property
    def type(self) -> Optional[SpiceModelType]:
        try:
            return SpiceModelType(self._root.get("Type"))
        except (AttributeError, ValueError, TypeError):
            return None

    @type.setter
    def type(self, value: Optional[SpiceModelType]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        elif "Type" in self._root.attrib:
            self._root.attrib.pop("Type")

    @property
    def model(self) -> Optional[str]:
        if (tag := self._root.find("./Model")) is not None:
            return tag.text
        return None

    @model.setter
    def model(self, value: Optional[str]) -> None:
        for tag in self._root.findall("./Model"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Model")
            tag.text = value

    @property
    def details(self) -> Optional[List[str]]:
        if (tag := self._root.find("./Details")) is not None:
            return [x.text for x in tag.findall("./Item")]
        return None

    @details.setter
    def details(self, value: Optional[List[str]]) -> None:
        for tag in self._root.findall("./Details"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Details")
            for line in value:
                SubElement(tag, "Item").text = line


class SpiceModelMixin(RootMixin):
    @property
    def spice(self) -> Optional[SpiceModel]:
        try:
            if (tag := self._root.find("SpiceModel")) is not None:
                return SpiceModel(tag)
            return None
        except (AttributeError, ValueError, KeyError):
            return None

    @spice.setter
    def spice(self, value: Optional[SpiceModel]) -> None:
        for tag in self._root.findall("./SpiceModel"):
            self._root.remove(tag)
        if value is not None:
            self._root.append(deepcopy(value.root))


if __name__ == "__main__":
    pass
