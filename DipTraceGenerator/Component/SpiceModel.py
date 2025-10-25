#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""SpiceModel representation for DipTrace component libraries."""


from ..Enums import SpiceModelType
from ..xmltools import etree, E, dataclass, field


@dataclass
class SpiceModel:
    """
    Represents a SPICE model for circuit simulation.
    
    SPICE (Simulation Program with Integrated Circuit Emphasis) models are used
    for circuit simulation and analysis. This class supports both SubCircuit and
    Model types.
    
    Attributes:
        type (SpiceModelType): Type of SPICE model. Defaults to SubCkt.
    """
    type: SpiceModelType = field(default=SpiceModelType.SubCkt)

    @classmethod
    def from_xml(cls, element: etree._Element) -> "SpiceModel":
        """
        Create SpiceModel instance from XML element.

        Args:
            element (etree._Element): XML element representing the SpiceModel.

        Returns:
            SpiceModel: The created SpiceModel instance.
            
        Example:
            >>> from lxml.etree import fromstring
            >>> xml = fromstring('<SpiceModel Type="Model"/>')
            >>> model = SpiceModel.from_xml(xml)
            >>> model.type
            <SpiceModelType.Model: 'Model'>
        """
        type_str = element.get("Type", "SubCkt")
        return cls(type=SpiceModelType(type_str))

    def to_xml(self) -> etree._Element:
        """
        Convert SpiceModel instance to XML element.

        Returns:
            etree._Element: XML element representing the SpiceModel.
            
        Example:
            >>> model = SpiceModel(type=SpiceModelType.SubCkt)
            >>> element = model.to_xml()
            >>> element.get("Type")
            'SubCkt'
        """
        return E.SpiceModel(Type=self.type.value)


if __name__ == "__main__":
    pass
