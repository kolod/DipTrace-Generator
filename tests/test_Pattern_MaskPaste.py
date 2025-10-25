#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


from lxml import etree
from unittest import TestCase, main
from DipTraceGenerator.Pattern import MaskPaste, SegmentItem,  MaskSetting, PasteSetting
from DipTraceGenerator import Units


class TestSegmentItem(TestCase):
    """Test cases for SegmentItem class."""

    def test_default_constructor(self):
        """Test creating SegmentItem with default values."""
        item = SegmentItem()
        self.assertEqual(item.x1, 0.0)
        self.assertEqual(item.y1, 0.0)
        self.assertEqual(item.x2, 0.0)
        self.assertEqual(item.y2, 0.0)

    def test_constructor_with_values(self):
        """Test creating SegmentItem with specific values."""
        item = SegmentItem(x1=-0.74, y1=1.3, x2=0.74, y2=0.17)
        self.assertEqual(item.x1, -0.74)
        self.assertEqual(item.y1, 1.3)
        self.assertEqual(item.x2, 0.74)
        self.assertEqual(item.y2, 0.17)

    def test_from_xml(self):
        """Test parsing SegmentItem from XML."""
        xml = '<Item X1="-0.74" Y1="1.3" X2="0.74" Y2="0.17"/>'
        element = etree.fromstring(xml)
        item = SegmentItem.from_xml(element)
        
        self.assertAlmostEqual(item.x1, -0.74, places=4)
        self.assertAlmostEqual(item.y1, 1.3, places=4)
        self.assertAlmostEqual(item.x2, 0.74, places=4)
        self.assertAlmostEqual(item.y2, 0.17, places=4)

    def test_to_xml(self):
        """Test converting SegmentItem to XML."""
        item = SegmentItem(x1=-0.74, y1=1.3, x2=0.74, y2=0.17)
        element = item.to_xml()
        
        self.assertEqual(element.tag, "Item")
        self.assertEqual(element.get("X1"), "-0.74")
        self.assertEqual(element.get("Y1"), "1.3")
        self.assertEqual(element.get("X2"), "0.74")
        self.assertEqual(element.get("Y2"), "0.17")

    def test_unit_conversion_mil(self):
        """Test unit conversion to MIL."""
        item = SegmentItem(x1=2.54, y1=1.27, x2=5.08, y2=2.54)  # 100, 50, 200, 100 mils
        element = item.to_xml(Units.MIL)
        
        self.assertEqual(element.get("X1"), "100")
        self.assertEqual(element.get("Y1"), "50")
        self.assertEqual(element.get("X2"), "200")
        self.assertEqual(element.get("Y2"), "100")


class TestMaskPaste(TestCase):
    """Test cases for Pattern.MaskPaste class."""

    def test_default_constructor(self):
        """Test creating MaskPaste with default values."""
        mp = MaskPaste()
        self.assertIsNone(mp.top_mask)
        self.assertIsNone(mp.bot_mask)
        self.assertIsNone(mp.top_paste)
        self.assertIsNone(mp.bot_paste)
        self.assertIsNone(mp.segment_percent)
        self.assertIsNone(mp.segment_edge_gap)
        self.assertIsNone(mp.segment_gap)
        self.assertIsNone(mp.segment_side)
        self.assertIsNone(mp.custom_swell)
        self.assertIsNone(mp.custom_shrink)
        self.assertEqual(mp.top_segments, [])
        self.assertEqual(mp.bot_segments, [])

    def test_constructor_with_values(self):
        """Test creating MaskPaste with specific values."""
        mp = MaskPaste(
            top_mask=MaskSetting.Open,
            bot_mask=MaskSetting.Tented,
            top_paste=PasteSetting.Solder,
            bot_paste=PasteSetting.NoSolder
        )
        self.assertEqual(mp.top_mask, MaskSetting.Open)
        self.assertEqual(mp.bot_mask, MaskSetting.Tented)
        self.assertEqual(mp.top_paste, PasteSetting.Solder)
        self.assertEqual(mp.bot_paste, PasteSetting.NoSolder)

    def test_from_xml_simple(self):
        """Test parsing simple MaskPaste from XML."""
        xml = '<MaskPaste TopMask="Open" BotMask="Tented" TopPaste="Solder" BotPaste="No Solder"/>'
        element = etree.fromstring(xml)
        mp = MaskPaste.from_xml(element)
        
        self.assertEqual(mp.top_mask, MaskSetting.Open)
        self.assertEqual(mp.bot_mask, MaskSetting.Tented)
        self.assertEqual(mp.top_paste, PasteSetting.Solder)
        self.assertEqual(mp.bot_paste, PasteSetting.NoSolder)

    def test_from_xml_with_segments(self):
        """Test parsing MaskPaste with segmented paste from XML."""
        xml = '''<MaskPaste TopPaste="Segments" Segment_Percent="50" Segment_EdgeGap="0.3" Segment_Gap="0.2" Segment_Side="1">
            <TopSegments>
                <Item X1="-0.74" Y1="1.3" X2="0.74" Y2="0.17"/>
                <Item X1="-0.74" Y1="-0.17" X2="0.74" Y2="-1.3"/>
            </TopSegments>
        </MaskPaste>'''
        element = etree.fromstring(xml)
        mp = MaskPaste.from_xml(element)
        
        self.assertEqual(mp.top_paste, PasteSetting.Segments)
        self.assertEqual(mp.segment_percent, 50.0)
        self.assertAlmostEqual(mp.segment_edge_gap, 0.3, places=4)
        self.assertAlmostEqual(mp.segment_gap, 0.2, places=4)
        self.assertAlmostEqual(mp.segment_side, 1.0, places=4)
        self.assertEqual(len(mp.top_segments), 2)
        self.assertAlmostEqual(mp.top_segments[0].x1, -0.74, places=4)

    def test_from_xml_with_custom_values(self):
        """Test parsing MaskPaste with custom swell/shrink values."""
        xml = '<MaskPaste TopMask="Common" CustomSwell="0.1" CustomShrink="0.05"/>'
        element = etree.fromstring(xml)
        mp = MaskPaste.from_xml(element)
        
        self.assertEqual(mp.top_mask, MaskSetting.Common)
        self.assertAlmostEqual(mp.custom_swell, 0.1, places=4)
        self.assertAlmostEqual(mp.custom_shrink, 0.05, places=4)

    def test_from_xml_bot_segments(self):
        """Test parsing MaskPaste with bottom segments."""
        xml = '''<MaskPaste BotPaste="Segments">
            <BotSegments>
                <Item X1="0" Y1="0" X2="1" Y2="1"/>
            </BotSegments>
        </MaskPaste>'''
        element = etree.fromstring(xml)
        mp = MaskPaste.from_xml(element)
        
        self.assertEqual(mp.bot_paste, PasteSetting.Segments)
        self.assertEqual(len(mp.bot_segments), 1)
        self.assertAlmostEqual(mp.bot_segments[0].x2, 1.0, places=4)

    def test_to_xml_simple(self):
        """Test converting simple MaskPaste to XML."""
        mp = MaskPaste(
            top_mask=MaskSetting.Open,
            bot_mask=MaskSetting.Tented,
            top_paste=PasteSetting.Solder,
            bot_paste=PasteSetting.NoSolder
        )
        element = mp.to_xml()
        
        self.assertEqual(element.tag, "MaskPaste")
        self.assertEqual(element.get("TopMask"), "Open")
        self.assertEqual(element.get("BotMask"), "Tented")
        self.assertEqual(element.get("TopPaste"), "Solder")
        self.assertEqual(element.get("BotPaste"), "No Solder")

    def test_to_xml_with_segments(self):
        """Test converting MaskPaste with segments to XML."""
        mp = MaskPaste(
            top_paste=PasteSetting.Segments,
            segment_percent=50.0,
            segment_edge_gap=0.3,
            segment_gap=0.2,
            segment_side=1.0,
            top_segments=[
                SegmentItem(-0.74, 1.3, 0.74, 0.17),
                SegmentItem(-0.74, -0.17, 0.74, -1.3)
            ]
        )
        element = mp.to_xml()
        
        self.assertEqual(element.get("TopPaste"), "Segments")
        self.assertEqual(element.get("Segment_Percent"), "50")
        self.assertEqual(element.get("Segment_EdgeGap"), "0.3")
        self.assertEqual(element.get("Segment_Gap"), "0.2")
        self.assertEqual(element.get("Segment_Side"), "1")
        
        top_segments = element.find("TopSegments")
        self.assertIsNotNone(top_segments)
        items = top_segments.findall("Item")
        self.assertEqual(len(items), 2)

    def test_to_xml_with_custom_values(self):
        """Test converting MaskPaste with custom values to XML."""
        mp = MaskPaste(
            top_mask=MaskSetting.Common,
            custom_swell=0.1,
            custom_shrink=0.05
        )
        element = mp.to_xml()
        
        self.assertEqual(element.get("CustomSwell"), "0.1")
        self.assertEqual(element.get("CustomShrink"), "0.05")

    def test_to_xml_empty_segments(self):
        """Test converting MaskPaste with empty segment lists."""
        mp = MaskPaste(
            top_paste=PasteSetting.Segments,
            top_segments=[]
        )
        element = mp.to_xml()
        
        top_segments = element.find("TopSegments")
        self.assertIsNone(top_segments)

    def test_all_mask_settings(self):
        """Test all mask setting values."""
        settings = [
            MaskSetting.Common,
            MaskSetting.Open,
            MaskSetting.Tented,
            MaskSetting.ByPaste
        ]
        
        for setting in settings:
            with self.subTest(setting=setting):
                mp = MaskPaste(top_mask=setting)
                element = mp.to_xml()
                self.assertEqual(element.get("TopMask"), setting.value)

    def test_all_paste_settings(self):
        """Test all paste setting values."""
        settings = [
            PasteSetting.Common,
            PasteSetting.Solder,
            PasteSetting.NoSolder,
            PasteSetting.Segments
        ]
        
        for setting in settings:
            with self.subTest(setting=setting):
                mp = MaskPaste(top_paste=setting)
                element = mp.to_xml()
                self.assertEqual(element.get("TopPaste"), setting.value)

    def test_unit_conversion_mil(self):
        """Test unit conversion to MIL."""
        mp = MaskPaste(
            segment_edge_gap=0.254,  # 10 mils
            segment_gap=0.508,       # 20 mils
            segment_side=2.54,       # 100 mils
            custom_swell=0.127,      # 5 mils
            custom_shrink=0.0762     # 3 mils
        )
        element = mp.to_xml(Units.MIL)
        
        self.assertEqual(element.get("Segment_EdgeGap"), "10")
        self.assertEqual(element.get("Segment_Gap"), "20")
        self.assertEqual(element.get("Segment_Side"), "100")
        self.assertEqual(element.get("CustomSwell"), "5")
        self.assertEqual(element.get("CustomShrink"), "3")

    def test_unit_conversion_inch(self):
        """Test unit conversion to INCH."""
        mp = MaskPaste(
            segment_edge_gap=2.54,  # 0.1 inches
            custom_swell=1.27       # 0.05 inches
        )
        element = mp.to_xml(Units.INCH)
        
        self.assertEqual(element.get("Segment_EdgeGap"), "0.1")
        self.assertEqual(element.get("CustomSwell"), "0.05")

    def test_from_xml_unit_conversion_mil(self):
        """Test parsing MaskPaste from XML in MIL units."""
        xml = '<MaskPaste Segment_EdgeGap="10" CustomSwell="5"/>'
        element = etree.fromstring(xml)
        mp = MaskPaste.from_xml(element, Units.MIL)
        
        # Internal storage should be in MM
        self.assertAlmostEqual(mp.segment_edge_gap, 0.254, places=4)
        self.assertAlmostEqual(mp.custom_swell, 0.127, places=4)

    def test_roundtrip_conversion(self):
        """Test that parsing and generating XML produces identical result."""
        xml = '<MaskPaste TopMask="Open" BotPaste="Solder"/>'
        element1 = etree.fromstring(xml)
        mp = MaskPaste.from_xml(element1)
        element2 = mp.to_xml()
        
        self.assertEqual(element2.get("TopMask"), element1.get("TopMask"))
        self.assertEqual(element2.get("BotPaste"), element1.get("BotPaste"))

    def test_roundtrip_with_segments(self):
        """Test roundtrip conversion with segment data."""
        xml = '''<MaskPaste TopPaste="Segments" Segment_Percent="50">
            <TopSegments>
                <Item X1="-0.74" Y1="1.3" X2="0.74" Y2="0.17"/>
            </TopSegments>
        </MaskPaste>'''
        element1 = etree.fromstring(xml)
        mp = MaskPaste.from_xml(element1)
        element2 = mp.to_xml()
        
        self.assertEqual(element2.get("TopPaste"), "Segments")
        self.assertEqual(element2.get("Segment_Percent"), "50")
        top_segments = element2.find("TopSegments")
        self.assertIsNotNone(top_segments)
        items = top_segments.findall("Item")
        self.assertEqual(len(items), 1)

    def test_partial_attributes(self):
        """Test MaskPaste with only some attributes set."""
        mp = MaskPaste(top_mask=MaskSetting.Open)
        element = mp.to_xml()
        
        self.assertEqual(element.get("TopMask"), "Open")
        self.assertIsNone(element.get("BotMask"))
        self.assertIsNone(element.get("TopPaste"))
        self.assertIsNone(element.get("BotPaste"))

    def test_both_segment_lists(self):
        """Test MaskPaste with both top and bottom segments."""
        mp = MaskPaste(
            top_paste=PasteSetting.Segments,
            bot_paste=PasteSetting.Segments,
            top_segments=[SegmentItem(0, 0, 1, 1)],
            bot_segments=[SegmentItem(0, 0, 2, 2)]
        )
        element = mp.to_xml()
        
        top_segments = element.find("TopSegments")
        bot_segments = element.find("BotSegments")
        self.assertIsNotNone(top_segments)
        self.assertIsNotNone(bot_segments)
        self.assertEqual(len(top_segments.findall("Item")), 1)
        self.assertEqual(len(bot_segments.findall("Item")), 1)

    def test_segment_percent_integer(self):
        """Test that segment percent is output as integer."""
        mp = MaskPaste(segment_percent=50.0)
        element = mp.to_xml()
        
        self.assertEqual(element.get("Segment_Percent"), "50")
        # Ensure no decimal point
        self.assertNotIn(".", element.get("Segment_Percent"))

    def test_negative_custom_values(self):
        """Test MaskPaste with negative custom values."""
        mp = MaskPaste(
            custom_swell=-0.1,
            custom_shrink=-0.05
        )
        element = mp.to_xml()
        
        self.assertEqual(element.get("CustomSwell"), "-0.1")
        self.assertEqual(element.get("CustomShrink"), "-0.05")

    def test_zero_values(self):
        """Test MaskPaste with zero values."""
        mp = MaskPaste(
            segment_edge_gap=0.0,
            segment_gap=0.0,
            custom_swell=0.0
        )
        element = mp.to_xml()
        
        self.assertEqual(element.get("Segment_EdgeGap"), "0")
        self.assertEqual(element.get("Segment_Gap"), "0")
        self.assertEqual(element.get("CustomSwell"), "0")


if __name__ == "__main__":
    main()
