#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!


import unittest
from DipTraceGenerator.Pattern import PadStyle, MainStack, MaskPaste, SegmentItem
from DipTraceGenerator import Units
from DipTraceGenerator.Enums import PadType, HoleType, PadSide, PadStackShape, PasteSetting
from lxml import etree


class TestPadStyle(unittest.TestCase):
    """Test cases for Pattern.PadStyle class."""

    def test_default_constructor(self):
        """Test creating PadStyle with default values."""
        style = PadStyle()
        self.assertEqual(style.name, "")
        self.assertEqual(style.pad_type, PadType.Surface)
        self.assertEqual(style.side, PadSide.Top)
        self.assertIsNone(style.hole_type)
        self.assertIsNone(style.hole)
        self.assertIsNone(style.hole_h)
        self.assertIsNone(style.main_stack)
        self.assertIsNone(style.mask_paste)

    def test_constructor_with_values(self):
        """Test creating PadStyle with specific values."""
        main_stack = MainStack(shape=PadStackShape.Rectangle, width=0.6, height=2.0)
        style = PadStyle(
            name="PadT0",
            pad_type=PadType.Surface,
            side=PadSide.Top,
            main_stack=main_stack
        )
        self.assertEqual(style.name, "PadT0")
        self.assertEqual(style.pad_type, PadType.Surface)
        self.assertEqual(style.side, PadSide.Top)
        self.assertEqual(style.main_stack, main_stack)

    def test_from_xml_surface_simple(self):
        """Test parsing simple surface pad style from XML."""
        xml = '''<PadStyle Name="PadT0" Type="Surface" Side="Top">
            <MainStack Shape="Rectangle" Width="0.6" Height="2" Corner="25"/>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element)
        
        self.assertEqual(style.name, "PadT0")
        self.assertEqual(style.pad_type, PadType.Surface)
        self.assertEqual(style.side, PadSide.Top)
        self.assertIsNone(style.hole_type)
        self.assertIsNone(style.hole)
        self.assertIsNotNone(style.main_stack)
        self.assertEqual(style.main_stack.shape, PadStackShape.Rectangle)
        self.assertAlmostEqual(style.main_stack.width, 0.6, places=4)
        self.assertAlmostEqual(style.main_stack.height, 2.0, places=4)

    def test_from_xml_surface_with_mask_paste(self):
        """Test parsing surface pad with MaskPaste from XML."""
        xml = '''<PadStyle Name="PadT1" Type="Surface" Side="Top">
            <MainStack Shape="Rectangle" Width="2.1" Height="3.2" Corner="0"/>
            <MaskPaste TopPaste="Segments" Segment_Percent="50" Segment_EdgeGap="0.3" Segment_Gap="0.2" Segment_Side="1">
                <TopSegments>
                    <Item X1="-0.74" Y1="1.3" X2="0.74" Y2="0.17"/>
                    <Item X1="-0.74" Y1="-0.17" X2="0.74" Y2="-1.3"/>
                </TopSegments>
            </MaskPaste>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element)
        
        self.assertEqual(style.name, "PadT1")
        self.assertEqual(style.pad_type, PadType.Surface)
        self.assertIsNotNone(style.main_stack)
        self.assertIsNotNone(style.mask_paste)
        self.assertEqual(len(style.mask_paste.top_segments), 2)

    def test_from_xml_through_round(self):
        """Test parsing through-hole pad with round hole from XML."""
        xml = '''<PadStyle Name="PadT20" Type="Through" HoleType="Round" Hole="0.9" Side="Top">
            <MainStack Shape="Ellipse" Width="1.5" Height="1.5" XOff="0" YOff="0"/>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element)
        
        self.assertEqual(style.name, "PadT20")
        self.assertEqual(style.pad_type, PadType.Through)
        self.assertEqual(style.hole_type, HoleType.Round)
        self.assertAlmostEqual(style.hole, 0.9, places=4)
        self.assertIsNone(style.hole_h)
        self.assertIsNotNone(style.main_stack)
        self.assertEqual(style.main_stack.shape, PadStackShape.Ellipse)

    def test_from_xml_through_obround(self):
        """Test parsing through-hole pad with obround hole from XML."""
        xml = '''<PadStyle Name="TestPad" Type="Through" HoleType="Obround" Hole="0.9" HoleH="1.5" Side="Top">
            <MainStack Shape="Obround" Width="1.5" Height="2.0" XOff="0" YOff="0"/>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element)
        
        self.assertEqual(style.pad_type, PadType.Through)
        self.assertEqual(style.hole_type, HoleType.Obround)
        self.assertAlmostEqual(style.hole, 0.9, places=4)
        self.assertAlmostEqual(style.hole_h, 1.5, places=4)

    def test_from_xml_bottom_side(self):
        """Test parsing pad style with bottom side."""
        xml = '''<PadStyle Name="PadB0" Type="Surface" Side="Bottom">
            <MainStack Shape="Rectangle" Width="1.0" Height="1.0" Corner="0"/>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element)
        
        self.assertEqual(style.side, PadSide.Bottom)

    def test_to_xml_surface_simple(self):
        """Test converting simple surface pad style to XML."""
        main_stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=0.6,
            height=2.0,
            corner=25.0
        )
        style = PadStyle(
            name="PadT0",
            pad_type=PadType.Surface,
            side=PadSide.Top,
            main_stack=main_stack
        )
        element = style.to_xml()
        
        self.assertEqual(element.tag, "PadStyle")
        self.assertEqual(element.get("Name"), "PadT0")
        self.assertEqual(element.get("Type"), "Surface")
        self.assertEqual(element.get("Side"), "Top")
        self.assertIsNone(element.get("HoleType"))
        self.assertIsNone(element.get("Hole"))
        
        main_stack_elem = element.find("MainStack")
        self.assertIsNotNone(main_stack_elem)

    def test_to_xml_surface_with_mask_paste(self):
        """Test converting surface pad with MaskPaste to XML."""
        main_stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=2.1,
            height=3.2,
            corner=0.0
        )
        mask_paste = MaskPaste(
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
        style = PadStyle(
            name="PadT1",
            pad_type=PadType.Surface,
            side=PadSide.Top,
            main_stack=main_stack,
            mask_paste=mask_paste
        )
        element = style.to_xml()
        
        self.assertIsNotNone(element.find("MainStack"))
        self.assertIsNotNone(element.find("MaskPaste"))

    def test_to_xml_through_round(self):
        """Test converting through-hole pad with round hole to XML."""
        main_stack = MainStack(
            shape=PadStackShape.Ellipse,
            width=1.5,
            height=1.5,
            xoff=0.0,
            yoff=0.0
        )
        style = PadStyle(
            name="PadT20",
            pad_type=PadType.Through,
            side=PadSide.Top,
            hole_type=HoleType.Round,
            hole=0.9,
            main_stack=main_stack
        )
        element = style.to_xml()
        
        self.assertEqual(element.get("Type"), "Through")
        self.assertEqual(element.get("HoleType"), "Round")
        self.assertEqual(element.get("Hole"), "0.9")
        self.assertIsNone(element.get("HoleH"))

    def test_to_xml_through_obround(self):
        """Test converting through-hole pad with obround hole to XML."""
        main_stack = MainStack(
            shape=PadStackShape.Obround,
            width=1.5,
            height=2.0,
            xoff=0.0,
            yoff=0.0
        )
        style = PadStyle(
            name="TestPad",
            pad_type=PadType.Through,
            side=PadSide.Top,
            hole_type=HoleType.Obround,
            hole=0.9,
            hole_h=1.5,
            main_stack=main_stack
        )
        element = style.to_xml()
        
        self.assertEqual(element.get("HoleType"), "Obround")
        self.assertEqual(element.get("Hole"), "0.9")
        self.assertEqual(element.get("HoleH"), "1.5")

    def test_unit_conversion_mil(self):
        """Test unit conversion to MIL."""
        main_stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=2.54,  # 100 mils
            height=1.27  # 50 mils
        )
        style = PadStyle(
            name="Test",
            pad_type=PadType.Through,
            side=PadSide.Top,
            hole_type=HoleType.Round,
            hole=2.286,  # 90 mils
            main_stack=main_stack
        )
        element = style.to_xml(Units.MIL)
        
        self.assertEqual(element.get("Hole"), "90")

    def test_unit_conversion_inch(self):
        """Test unit conversion to INCH."""
        main_stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=2.54,  # 0.1 inches
            height=1.27  # 0.05 inches
        )
        style = PadStyle(
            name="Test",
            pad_type=PadType.Through,
            side=PadSide.Top,
            hole_type=HoleType.Round,
            hole=2.54,  # 0.1 inches
            main_stack=main_stack
        )
        element = style.to_xml(Units.INCH)
        
        self.assertEqual(element.get("Hole"), "0.1")

    def test_from_xml_unit_conversion_mil(self):
        """Test parsing PadStyle from XML in MIL units."""
        xml = '''<PadStyle Name="Test" Type="Through" HoleType="Round" Hole="90" Side="Top">
            <MainStack Shape="Ellipse" Width="100" Height="100" XOff="0" YOff="0"/>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element, Units.MIL)
        
        # Internal storage should be in MM
        self.assertAlmostEqual(style.hole, 2.286, places=4)

    def test_roundtrip_conversion(self):
        """Test that parsing and generating XML produces identical result."""
        xml = '''<PadStyle Name="PadT0" Type="Surface" Side="Top">
            <MainStack Shape="Rectangle" Width="0.6" Height="2" Corner="25"/>
        </PadStyle>'''
        element1 = etree.fromstring(xml)
        style = PadStyle.from_xml(element1)
        element2 = style.to_xml()
        
        self.assertEqual(element2.get("Name"), element1.get("Name"))
        self.assertEqual(element2.get("Type"), element1.get("Type"))
        self.assertEqual(element2.get("Side"), element1.get("Side"))

    def test_roundtrip_through_pad(self):
        """Test roundtrip conversion for through-hole pad."""
        xml = '''<PadStyle Name="PadT20" Type="Through" HoleType="Round" Hole="0.9" Side="Top">
            <MainStack Shape="Ellipse" Width="1.5" Height="1.5" XOff="0" YOff="0"/>
        </PadStyle>'''
        element1 = etree.fromstring(xml)
        style = PadStyle.from_xml(element1)
        element2 = style.to_xml()
        
        self.assertEqual(element2.get("HoleType"), "Round")
        self.assertEqual(element2.get("Hole"), "0.9")

    def test_all_pad_types(self):
        """Test all pad type values."""
        types = [PadType.Surface, PadType.Through]
        
        for pad_type in types:
            with self.subTest(pad_type=pad_type):
                style = PadStyle(name="Test", pad_type=pad_type, side=PadSide.Top)
                element = style.to_xml()
                self.assertEqual(element.get("Type"), pad_type.value)

    def test_all_hole_types(self):
        """Test all hole type values."""
        hole_types = [HoleType.Round, HoleType.Obround]
        
        for hole_type in hole_types:
            with self.subTest(hole_type=hole_type):
                style = PadStyle(
                    name="Test",
                    pad_type=PadType.Through,
                    side=PadSide.Top,
                    hole_type=hole_type,
                    hole=1.0
                )
                element = style.to_xml()
                self.assertEqual(element.get("HoleType"), hole_type.value)

    def test_all_pad_sides(self):
        """Test all pad side values."""
        sides = [PadSide.Top, PadSide.Bottom]
        
        for side in sides:
            with self.subTest(side=side):
                style = PadStyle(name="Test", pad_type=PadType.Surface, side=side)
                element = style.to_xml()
                self.assertEqual(element.get("Side"), side.value)

    def test_no_main_stack(self):
        """Test PadStyle without MainStack."""
        style = PadStyle(name="Test", pad_type=PadType.Surface, side=PadSide.Top)
        element = style.to_xml()
        
        self.assertIsNone(element.find("MainStack"))

    def test_no_mask_paste(self):
        """Test PadStyle without MaskPaste."""
        main_stack = MainStack(shape=PadStackShape.Rectangle, width=1.0, height=1.0)
        style = PadStyle(
            name="Test",
            pad_type=PadType.Surface,
            side=PadSide.Top,
            main_stack=main_stack
        )
        element = style.to_xml()
        
        self.assertIsNone(element.find("MaskPaste"))

    def test_empty_name(self):
        """Test PadStyle with empty name."""
        style = PadStyle(name="", pad_type=PadType.Surface, side=PadSide.Top)
        element = style.to_xml()
        
        self.assertEqual(element.get("Name"), "")

    def test_long_name(self):
        """Test PadStyle with long name."""
        long_name = "PadStyle_With_Very_Long_Name_123456789"
        style = PadStyle(name=long_name, pad_type=PadType.Surface, side=PadSide.Top)
        element = style.to_xml()
        
        self.assertEqual(element.get("Name"), long_name)

    def test_complex_pad_style(self):
        """Test complex pad style with all features."""
        main_stack = MainStack(
            shape=PadStackShape.Rectangle,
            width=2.5,
            height=4.2,
            corner=0.0
        )
        mask_paste = MaskPaste(
            top_paste=PasteSetting.Segments,
            segment_percent=50.0,
            segment_edge_gap=0.3,
            segment_gap=0.2,
            segment_side=1.0,
            top_segments=[
                SegmentItem(-0.88, 1.79, 0.88, 0.31),
                SegmentItem(-0.88, -0.31, 0.88, -1.79)
            ]
        )
        style = PadStyle(
            name="PadT7",
            pad_type=PadType.Surface,
            side=PadSide.Top,
            main_stack=main_stack,
            mask_paste=mask_paste
        )
        element = style.to_xml()
        
        self.assertEqual(element.get("Name"), "PadT7")
        self.assertIsNotNone(element.find("MainStack"))
        self.assertIsNotNone(element.find("MaskPaste"))

    def test_through_pad_without_hole(self):
        """Test that through pad can be created without hole specifications."""
        style = PadStyle(
            name="Test",
            pad_type=PadType.Through,
            side=PadSide.Top
        )
        element = style.to_xml()
        
        self.assertEqual(element.get("Type"), "Through")
        self.assertIsNone(element.get("HoleType"))
        self.assertIsNone(element.get("Hole"))

    def test_hole_without_hole_h(self):
        """Test round hole without HoleH attribute."""
        style = PadStyle(
            name="Test",
            pad_type=PadType.Through,
            side=PadSide.Top,
            hole_type=HoleType.Round,
            hole=1.0
        )
        element = style.to_xml()
        
        self.assertEqual(element.get("Hole"), "1")
        self.assertIsNone(element.get("HoleH"))

    def test_parse_real_world_sample_surface(self):
        """Test parsing real-world surface pad sample."""
        xml = '''<PadStyle Name="PadT5" Type="Surface" Side="Top">
            <MainStack Shape="Rectangle" Width="2.5" Height="3.25" Corner="0"/>
            <MaskPaste TopPaste="Segments" Segment_Percent="50" Segment_EdgeGap="0.3" Segment_Gap="0.2" Segment_Side="1">
                <TopSegments>
                    <Item X1="-0.88" Y1="1.325" X2="0.88" Y2="0.185"/>
                    <Item X1="-0.88" Y1="-0.185" X2="0.88" Y2="-1.325"/>
                </TopSegments>
            </MaskPaste>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element)
        
        self.assertEqual(style.name, "PadT5")
        self.assertIsNotNone(style.main_stack)
        self.assertIsNotNone(style.mask_paste)
        self.assertEqual(len(style.mask_paste.top_segments), 2)

    def test_parse_real_world_sample_through(self):
        """Test parsing real-world through-hole pad sample."""
        xml = '''<PadStyle Name="PadT21" Type="Through" HoleType="Round" Hole="0.9" Side="Top">
            <MainStack Shape="Rectangle" Width="1.5" Height="1.5" XOff="0" YOff="0" Corner="0"/>
        </PadStyle>'''
        element = etree.fromstring(xml)
        style = PadStyle.from_xml(element)
        
        self.assertEqual(style.name, "PadT21")
        self.assertEqual(style.pad_type, PadType.Through)
        self.assertEqual(style.hole_type, HoleType.Round)
        self.assertAlmostEqual(style.hole, 0.9, places=4)
        self.assertIsNotNone(style.main_stack)


if __name__ == "__main__":
    unittest.main()
