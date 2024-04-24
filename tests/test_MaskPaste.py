#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from DipTraceGenerator import MaskPaste, MaskType, PasteType, Segment, Side

# <MaskPaste BotMask="Open" CustomSwell="0" CustomShrink="0"/>
# <MaskPaste TopMask="Tented" BotMask="Tented" TopPaste="No Solder" BotPaste="No Solder"/>
# <MaskPaste TopMask="Open" BotMask="Open" TopPaste="Solder" BotPaste="Solder" CustomSwell="0.3" CustomShrink="0.2"/>
# <MaskPaste TopMask="By Paste" BotMask="By Paste" TopPaste="Segments" BotPaste="Segments" Segment_Percent="50" Segment_EdgeGap="0.3" Segment_Gap="0.2" Segment_Side="1.2">
#     <TopSegments>
#         <Item X1="-0.53" Y1="1.0605" X2="0.53" Y2="-1.0605"/>
#     </TopSegments>
#     <BotSegments>
#         <Item X1="-0.53" Y1="1.0605" X2="0.53" Y2="-1.0605"/>
#     </BotSegments>
# </MaskPaste>


class TestMaskPaste(unittest.TestCase):
    def test_001(self):
        expected = "<MaskPaste/>\n"
        actual = MaskPaste()
        self.assertEqual(expected, str(actual))

    def test_002(self):
        expected = '<MaskPaste TopMask="Open" BotMask="Tented" TopPaste="No Solder" BotPaste="Solder"/>\n'
        actual = MaskPaste(
            top_mask=MaskType.Open,
            bottom_mask=MaskType.Tented,
            top_paste=PasteType.NoSolder,
            bottom_paste=PasteType.Solder,
        )

        self.assertEqual(expected, str(actual))

    def test_003(self):
        expected = (
            '<MaskPaste TopMask="Open" BotMask="Tented" TopPaste="No Solder" BotPaste="Solder" '
            'CustomSwell="0.05" CustomShrink="0.1"/>\n'
        )
        actual = MaskPaste(
            top_mask=MaskType.Open,
            bottom_mask=MaskType.Tented,
            top_paste=PasteType.NoSolder,
            bottom_paste=PasteType.Solder,
            swell=0.05,
            shrink=0.1,
        )
        self.assertEqual(expected, str(actual))
        self.assertEqual(MaskType.Open, actual.top_mask)
        self.assertEqual(MaskType.Tented, actual.bottom_mask)
        self.assertEqual(PasteType.NoSolder, actual.top_paste)
        self.assertEqual(PasteType.Solder, actual.bottom_paste)
        self.assertEqual(0.05, actual.swell)
        self.assertEqual(0.1, actual.shrink)

        actual.top_mask = MaskType.Common
        actual.top_paste = None
        actual.bottom_mask = PasteType.Common
        actual.bottom_paste = None
        actual.swell = None
        actual.shrink = None

        self.assertEqual("<MaskPaste/>\n", str(actual))

    def test_004(self):
        expected = (
            '<MaskPaste TopMask="By Paste" BotMask="By Paste" TopPaste="Segments" '
            'BotPaste="Segments" Segment_Percent="50" Segment_EdgeGap="0.3" Segment_Gap="0.2" Segment_Side="1">\n'
            "  <TopSegments>\n"
            '    <Item X1="-0.53" Y1="0.53" X2="0.53" Y2="-0.53"/>\n'
            "  </TopSegments>\n"
            "  <BotSegments>\n"
            '    <Item X1="-0.53" Y1="0.53" X2="0.53" Y2="-0.53"/>\n'
            "  </BotSegments>\n"
            "</MaskPaste>\n"
        )
        mask_paste = MaskPaste(
            top_mask=MaskType.ByPaste,
            bottom_mask=MaskType.ByPaste,
            top_paste=PasteType.Segments,
            bottom_paste=PasteType.Segments,
            segment_percent=50.0,
            segment_edge_gap=0.3,
            segment_gap=0.2,
            segment_side=1.0,
            top_segments=(Segment(x1=-0.53, y1=0.53, x2=0.53, y2=-0.53),),
            bottom_segments=(Segment(x1=-0.53, y1=0.53, x2=0.53, y2=-0.53),),
        )

        self.assertEqual(expected, str(mask_paste))
        self.assertEqual(MaskType.ByPaste, mask_paste.top_mask)
        self.assertEqual(MaskType.ByPaste, mask_paste.bottom_mask)
        self.assertEqual(PasteType.Segments, mask_paste.top_paste)
        self.assertEqual(PasteType.Segments, mask_paste.bottom_paste)
        self.assertEqual(50.0, mask_paste.segment_percent)
        self.assertEqual(0.3, mask_paste.segment_edge_gap)
        self.assertEqual(0.2, mask_paste.segment_gap)
        self.assertEqual(1.0, mask_paste.segment_side)
        self.assertEqual(1, len(mask_paste.top_segments))
        self.assertEqual(1, len(mask_paste.bottom_segments))
        self.assertEqual(-0.53, mask_paste.top_segments[0].x1)
        self.assertEqual(0.53, mask_paste.top_segments[0].x2)
        self.assertEqual(0.53, mask_paste.top_segments[0].y1)
        self.assertEqual(-0.53, mask_paste.top_segments[0].y2)
        self.assertEqual(-0.53, mask_paste.bottom_segments[0].x1)
        self.assertEqual(0.53, mask_paste.bottom_segments[0].x2)
        self.assertEqual(0.53, mask_paste.bottom_segments[0].y1)
        self.assertEqual(-0.53, mask_paste.bottom_segments[0].y2)


if __name__ == "__main__":
    unittest.main()
