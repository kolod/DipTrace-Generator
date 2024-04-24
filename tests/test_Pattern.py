#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Pattern import Pattern, PatternsMixin
from DipTraceGenerator.Enums import Boolean, Visible, PatternType, PatternMounting


class TestPattern(unittest.TestCase):
    def test_001(self):
        pattern = Pattern(xml("<Pattern/>"))

        self.assertIsNone(pattern.ref_des)
        self.assertIsNone(pattern.width)
        self.assertIsNone(pattern.height)
        self.assertIsNone(pattern.name)
        self.assertIsNone(pattern.name_description)
        self.assertIsNone(pattern.name_unique)
        self.assertIsNone(pattern.manufacturer)
        self.assertIsNone(pattern.value)
        self.assertIsNone(pattern.datasheet)
        self.assertIsNone(pattern.orientation)
        self.assertIsNone(pattern.type)
        self.assertIsNone(pattern.origin)
        self.assertIsNone(pattern.model3d)
        self.assertIsNone(pattern.mounting)

        self.assertListEqual([], pattern.parameters)

        self.assertEqual(0, len(pattern.pads))

    def test_002(self):
        pattern = Pattern(
            xml(
                '<Pattern PatternStyle="PatType0" RefDes="U1" Mounting="None" Width="0" Height="0" '
                '       Orientation="0" LockTypeChange="N" Type="Free"'
                '		Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">\n'
                "	<Name>Untitled</Name>\n"
                '	<Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>\n'
                '	<DefPad Style="PadT2"/>\n'
                '	<Model3D Mirror="N" NoSearch="N" Units="mil" IPC_XOff="0" IPC_YOff="0" AutoHeight="0"\n'
                '			AutoColor="4934475" Type="File" KeepPins="N">\n'
                "		<Filename>\n"
                "			<Path>WF-02_Right_Angle.wrl</Path>\n"
                "			<Var>WF-02_Right_Angle.wrl</Var>\n"
                "		</Filename>\n"
                '		<Rotate X="0" Y="0" Z="0"/>\n'
                '		<Offset X="0" Y="0" Z="0"/>\n'
                '		<Zoom X="1" Y="1" Z="1"/>\n'
                "	</Model3D>\n"
                "</Pattern>\n"
            )
        )

        self.assertEqual("U1", pattern.ref_des)
        self.assertEqual(0.0, pattern.width)
        self.assertEqual(0.0, pattern.height)
        self.assertEqual(0.0, pattern.orientation)
        self.assertEqual(Boolean.No, pattern.locked)
        self.assertEqual(PatternType.Free, pattern.type)
        self.assertEqual(PatternMounting.Default, pattern.mounting)

        self.assertListEqual([0.0, 0.0, 0.0, 0, 0], pattern.parameters)

        self.assertEqual("Untitled", pattern.name)
        self.assertEqual(None, pattern.name_description)
        self.assertEqual(None, pattern.name_unique)
        self.assertEqual(None, pattern.manufacturer)
        self.assertEqual(None, pattern.value)
        self.assertEqual(None, pattern.datasheet)

        self.assertEqual("PadT2", pattern.default_pad_style)
        self.assertEqual("PatType0", pattern.style)

        pattern.style = "PatType1"
        self.assertEqual("PatType1", pattern.style)

        self.assertEqual(0.0, pattern.origin.x)
        self.assertEqual(0.0, pattern.origin.y)
        self.assertEqual(Boolean.Yes, pattern.origin.cross)
        self.assertEqual(Boolean.Yes, pattern.origin.circle)
        self.assertEqual(Visible.Hide, pattern.origin.common)
        self.assertEqual(Visible.Show, pattern.origin.courtyard)

        self.assertEqual("WF-02_Right_Angle.wrl", pattern.model3d.filename.path.name)
        self.assertEqual("WF-02_Right_Angle.wrl", pattern.model3d.filename.variant.name)
        self.assertEqual(0.0, pattern.model3d.rotate.x)
        self.assertEqual(0.0, pattern.model3d.offset.y)
        self.assertEqual(1.0, pattern.model3d.zoom.z)

        self.assertEqual(0, len(pattern.pads))

        pattern.mounting = None
        self.assertIsNone(pattern.mounting)

        pattern.default_pad_style = None
        self.assertIsNone(pattern.default_pad_style)

        pattern.locked = None
        self.assertIsNone(pattern.locked)

        pattern.type = None
        self.assertIsNone(pattern.type)

        pattern.style = None
        self.assertIsNone(pattern.style)

    def test_003(self):
        pattern = Pattern(
            xml(
                '<Pattern RefDes="U1" Mounting="None" Width="0" Height="0" Orientation="0" LockTypeChange="N" Type="Free"\n'
                '		Float1="q" Float2="0" Float3="0" Int1="0" Int2="0"/>\n'
            )
        )

        self.assertListEqual([], pattern.parameters)

    def test_mixin_001(self):
        class PatternLibrary(PatternsMixin):
            pass

        library = PatternLibrary()

        self.assertIsNotNone(library.patterns)
        self.assertEqual(0, len(library.patterns))

        library.patterns = [
            Pattern(
                xml(
                    '<Pattern RefDes="U1" Mounting="None" Width="0" Height="0" Orientation="0" LockTypeChange="N" Type="Free"\n'
                    '		Float1="0" Float2="0" Float3="0" Int1="0" Int2="0">\n'
                    "	<Name>Untitled</Name>\n"
                    '	<Origin X="0" Y="0" Cross="Y" Circle="Y" Common="Hide" Courtyard="Show"/>\n'
                    '	<DefPad Style="PadT2"/>\n'
                    '	<Model3D Mirror="N" NoSearch="N" Units="mil" IPC_XOff="0" IPC_YOff="0" AutoHeight="0"\n'
                    '			AutoColor="4934475" Type="File" KeepPins="N">\n'
                    "		<Filename>\n"
                    "			<Path>WF-02_Right_Angle.wrl</Path>\n"
                    "			<Var>WF-02_Right_Angle.wrl</Var>\n"
                    "		</Filename>\n"
                    '		<Rotate X="0" Y="0" Z="0"/>\n'
                    '		<Offset X="0" Y="0" Z="0"/>\n'
                    '		<Zoom X="1" Y="1" Z="1"/>\n'
                    "	</Model3D>\n"
                    "</Pattern>\n"
                )
            )
        ]

        self.assertIsNotNone(library.patterns)
        self.assertEqual(1, len(library.patterns))
        self.assertEqual("WF-02_Right_Angle.wrl", library.patterns[0].model3d.filename.path.name)

        library.renumerate_styles()
        self.assertEqual("PatType0", library.patterns[0].style)

        library.patterns = None

        self.assertIsNotNone(library.patterns)
        self.assertEqual(0, len(library.patterns))


if __name__ == "__main__":
    unittest.main()
