#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""Represents solder mask and paste mask settings for a pad style in DipTrace component libraries."""


from typing import Optional
from ..xmltools import etree, E, dataclass, field
from ..Units import Units, convert_units
from .Enums import MaskSetting, PasteSetting


@dataclass
class SegmentItem:
    """Represents a rectangular segment for paste mask."""
    x1: float = field(default=0.0)
    y1: float = field(default=0.0)
    x2: float = field(default=0.0)
    y2: float = field(default=0.0)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "SegmentItem":
        """
        Create SegmentItem instance from XML element.

        Args:
            element (etree._Element): XML element representing the Item.
            units (Units): Units of the coordinates in the XML element. Defaults to Units.MM.

        Returns:
            SegmentItem: The created SegmentItem instance.
        """
        x1 = convert_units(float(element.get("X1", "0.0")), units, Units.MM)
        y1 = convert_units(float(element.get("Y1", "0.0")), units, Units.MM)
        x2 = convert_units(float(element.get("X2", "0.0")), units, Units.MM)
        y2 = convert_units(float(element.get("Y2", "0.0")), units, Units.MM)
        return cls(x1=x1, y1=y1, x2=x2, y2=y2)

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert SegmentItem instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the Item.
        """
        digits = 6 if units == Units.INCH else 4
        
        attrs = {
            "X1": f"{convert_units(self.x1, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "Y1": f"{convert_units(self.y1, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "X2": f"{convert_units(self.x2, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.'),
            "Y2": f"{convert_units(self.y2, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        }
        
        return E("Item", attrs)


@dataclass
class MaskPaste:
    """
    Represents solder mask and paste mask settings for a pad style.
    
    MaskPaste defines how solder mask openings and paste stencil apertures
    are created for a pad. Supports segmented paste for large pads.
    """
    
    top_mask: Optional[MaskSetting] = field(default=None)
    bot_mask: Optional[MaskSetting] = field(default=None)
    top_paste: Optional[PasteSetting] = field(default=None)
    bot_paste: Optional[PasteSetting] = field(default=None)
    segment_percent: Optional[float] = field(default=None)
    segment_edge_gap: Optional[float] = field(default=None)
    segment_gap: Optional[float] = field(default=None)
    segment_side: Optional[float] = field(default=None)
    custom_swell: Optional[float] = field(default=None)
    custom_shrink: Optional[float] = field(default=None)
    top_segments: list[SegmentItem] = field(default_factory=list)
    bot_segments: list[SegmentItem] = field(default_factory=list)

    @classmethod
    def from_xml(cls, element: etree._Element, units: Units = Units.MM) -> "MaskPaste":
        """
        Create MaskPaste instance from XML element.

        Args:
            element (etree._Element): XML element representing the MaskPaste.
            units (Units): Units of the dimensions in the XML element. Defaults to Units.MM.

        Returns:
            MaskPaste: The created MaskPaste instance.
        """
        # Parse mask and paste settings
        top_mask = None
        bot_mask = None
        top_paste = None
        bot_paste = None
        
        if "TopMask" in element.attrib:
            top_mask = MaskSetting(element.get("TopMask"))
        if "BotMask" in element.attrib:
            bot_mask = MaskSetting(element.get("BotMask"))
        if "TopPaste" in element.attrib:
            top_paste = PasteSetting(element.get("TopPaste"))
        if "BotPaste" in element.attrib:
            bot_paste = PasteSetting(element.get("BotPaste"))
        
        # Parse segment parameters
        segment_percent = None
        segment_edge_gap = None
        segment_gap = None
        segment_side = None
        
        if "Segment_Percent" in element.attrib:
            segment_percent = float(element.get("Segment_Percent"))
        if "Segment_EdgeGap" in element.attrib:
            segment_edge_gap = convert_units(float(element.get("Segment_EdgeGap")), units, Units.MM)
        if "Segment_Gap" in element.attrib:
            segment_gap = convert_units(float(element.get("Segment_Gap")), units, Units.MM)
        if "Segment_Side" in element.attrib:
            segment_side = convert_units(float(element.get("Segment_Side")), units, Units.MM)
        
        # Parse custom values
        custom_swell = None
        custom_shrink = None
        
        if "CustomSwell" in element.attrib:
            custom_swell = convert_units(float(element.get("CustomSwell")), units, Units.MM)
        if "CustomShrink" in element.attrib:
            custom_shrink = convert_units(float(element.get("CustomShrink")), units, Units.MM)
        
        # Parse segment lists
        top_segments = []
        bot_segments = []
        
        top_segments_element = element.find("TopSegments")
        if top_segments_element is not None:
            for item_element in top_segments_element.findall("Item"):
                top_segments.append(SegmentItem.from_xml(item_element, units))
        
        bot_segments_element = element.find("BotSegments")
        if bot_segments_element is not None:
            for item_element in bot_segments_element.findall("Item"):
                bot_segments.append(SegmentItem.from_xml(item_element, units))
        
        return cls(
            top_mask=top_mask,
            bot_mask=bot_mask,
            top_paste=top_paste,
            bot_paste=bot_paste,
            segment_percent=segment_percent,
            segment_edge_gap=segment_edge_gap,
            segment_gap=segment_gap,
            segment_side=segment_side,
            custom_swell=custom_swell,
            custom_shrink=custom_shrink,
            top_segments=top_segments,
            bot_segments=bot_segments
        )

    def to_xml(self, units: Units = Units.MM) -> etree._Element:
        """
        Convert MaskPaste instance to XML element.

        Args:
            units (Units): Units to use for the XML element. Defaults to Units.MM.

        Returns:
            etree._Element: XML element representing the MaskPaste.
        """
        digits = 6 if units == Units.INCH else 4
        
        # Create attributes dictionary
        attrs = {}
        
        # Add mask and paste settings
        if self.top_mask is not None:
            attrs["TopMask"] = self.top_mask.value
        if self.bot_mask is not None:
            attrs["BotMask"] = self.bot_mask.value
        if self.top_paste is not None:
            attrs["TopPaste"] = self.top_paste.value
        if self.bot_paste is not None:
            attrs["BotPaste"] = self.bot_paste.value
        
        # Add segment parameters
        if self.segment_percent is not None:
            attrs["Segment_Percent"] = str(int(self.segment_percent))
        if self.segment_edge_gap is not None:
            attrs["Segment_EdgeGap"] = f"{convert_units(self.segment_edge_gap, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        if self.segment_gap is not None:
            attrs["Segment_Gap"] = f"{convert_units(self.segment_gap, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        if self.segment_side is not None:
            attrs["Segment_Side"] = f"{convert_units(self.segment_side, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        
        # Add custom values
        if self.custom_swell is not None:
            attrs["CustomSwell"] = f"{convert_units(self.custom_swell, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        if self.custom_shrink is not None:
            attrs["CustomShrink"] = f"{convert_units(self.custom_shrink, Units.MM, units):.{digits}f}".rstrip('0').rstrip('.')
        
        # Create element
        element = E("MaskPaste", attrs)
        
        # Add segment lists
        if self.top_segments:
            top_segments_element = E("TopSegments")
            for segment in self.top_segments:
                top_segments_element.append(segment.to_xml(units))
            element.append(top_segments_element)
        
        if self.bot_segments:
            bot_segments_element = E("BotSegments")
            for segment in self.bot_segments:
                bot_segments_element.append(segment.to_xml(units))
            element.append(bot_segments_element)
        
        return element
