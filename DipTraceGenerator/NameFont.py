#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_NameFont.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.NameFont tests/test_NameFont.py -v --cov-report=term --cov-report=term-missing


from .xmltools import etree, dataclass, field


@dataclass
class NameFont:
    """
    Font settings for pin names.
    
    Attributes:
        size (int): Font size. Defaults to 5.
        width (int): Font width. Defaults to -2.
        scale (float): Font scale. Defaults to 1.0.
    """
    size: int = field(default=5)
    width: int = field(default=-2)
    scale: float = field(default=1.0)

    @classmethod
    def from_xml(cls, element: etree._Element) -> "NameFont":
        """
        Create NameFont from XML element.
        
        Args:
            element (etree._Element): XML element representing the NameFont.
            
        Returns:
            NameFont: NameFont instance created from the XML element.
        """
        size = int(element.get("Size", "5"))
        width = int(element.get("Width", "-2"))
        scale = float(element.get("Scale", "1.0"))
        return cls(size=size, width=width, scale=scale)

    def to_xml(self) -> etree._Element:
        """
        Convert NameFont to XML element.
        
        Returns:
            etree._Element: XML element representing the NameFont.
        """
        return etree.Element("NameFont",
            Size=str(self.size),
            Width=str(self.width),
            Scale=str(self.scale)
        )


if __name__ == "__main__":
    pass
