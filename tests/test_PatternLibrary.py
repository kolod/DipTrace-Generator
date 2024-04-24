#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from pathlib import Path
from DipTraceGenerator import (
    MainStack,
    MainStackShape,
    PadStyle,
    MountType,
    Side,
    Pattern,
    PatternLibrary,
    Units,
    load_from_xml_file,
    Boolean,
    PatternType,
    PatternOrigin,
    Visible,
    compare,
    format_xml,
    Pad,
    Model3D,
    Model3DType,
    Units3D,
    PatternShape,
    ShapeType,
    Terminal,
    TerminalShape,
    HoleType,
    RecoveryCode,
    PatternMounting,
    Layer,
    Point,
    Rotate,
    Offset,
    Zoom,
)


class TestDipTracePatternLibrary(unittest.TestCase):
    path = Path(__file__).parent

    def test_pattern_library(self):
        library = PatternLibrary()

        self.assertIsNone(library.name)
        self.assertIsNone(library.hint)
        self.assertEqual("4.3.0.5", library.version)
        self.assertEqual(Units.mm, library.units)

        self.assertListEqual([], library.categories)
        self.assertListEqual([], library.patterns)
        self.assertListEqual([], library.pad_styles)

    def test_led_3mm(self):
        main_stack_1 = MainStack()
        main_stack_1.shape = MainStackShape.Obround
        main_stack_1.width = 1.5
        main_stack_1.height = 1.5
        main_stack_1.x_offset = 0.0
        main_stack_1.y_offset = 0.0

        main_stack_2 = MainStack()
        main_stack_2.shape = MainStackShape.Rectangle
        main_stack_2.width = 1.5
        main_stack_2.height = 1.5
        main_stack_2.x_offset = 0.0
        main_stack_2.y_offset = 0.0
        main_stack_2.corner = 0.0

        terminal = Terminal()
        terminal.shape = TerminalShape.Rectangle
        terminal.x = 0.0
        terminal.y = 0.0
        terminal.angle = 0.0
        terminal.width = 0.5
        terminal.height = 0.5
        terminal.corner = 0.0

        pad_style_1 = PadStyle()
        pad_style_1.name = "PadT0"
        pad_style_1.type = MountType.ThroughHole
        pad_style_1.main_stack = main_stack_1
        pad_style_1.terminals = [terminal]
        pad_style_1.hole_type = HoleType.Round
        pad_style_1.hole_width = 0.889
        pad_style_1.side = Side.Top

        pad_style_2 = PadStyle()
        pad_style_2.name = "PadT1"
        pad_style_2.type = MountType.ThroughHole
        pad_style_2.main_stack = main_stack_2
        pad_style_2.terminals = [terminal]
        pad_style_2.hole_type = HoleType.Round
        pad_style_2.hole_width = 0.889
        pad_style_2.side = Side.Top

        origin = PatternOrigin()
        origin.x = 0.0
        origin.y = 0.0
        origin.cross = Boolean.Yes
        origin.circle = Boolean.Yes
        origin.common = Visible.Hide
        origin.courtyard = Visible.Show

        pad_1 = Pad()
        pad_1.id = 1
        pad_1.number = "1"
        pad_1.style = pad_style_2.name
        pad_1.x = -1.27
        pad_1.y = 0.0
        pad_1.angle = 0.0
        pad_1.locked = Boolean.Yes
        pad_1.side = Side.Top

        pad_2 = Pad()
        pad_2.id = 2
        pad_2.number = "2"
        pad_2.style = pad_style_1.name
        pad_2.x = 1.27
        pad_2.y = 0.0
        pad_2.angle = 3.1416
        pad_2.locked = Boolean.Yes
        pad_2.side = Side.Top

        rotate = Rotate()
        rotate.x = 0.0
        rotate.y = 0.0
        rotate.z = 0.0

        offset = Offset()
        offset.x = 0.0
        offset.y = 0.0
        offset.z = -0.05

        zoom = Zoom()
        zoom.x = 1.0
        zoom.y = 1.0
        zoom.z = 1.0

        model3d = Model3D()
        model3d.mirror = Boolean.No
        model3d.no_search = Boolean.No
        model3d.units = Units3D.mm
        model3d.x_offset = 0.0
        model3d.y_offset = 0.0
        model3d.auto_height = 8.4
        model3d.auto_color = 4934475
        model3d.type = Model3DType.IPC_7351
        model3d.keep_pins = Boolean.No
        model3d.rotate = rotate
        model3d.offset = offset
        model3d.zoom = zoom

        recovery_code = RecoveryCode()
        recovery_code.generator = Boolean.Yes
        recovery_code.model = Boolean.Yes
        recovery_code.text = (
            "[N;Radial (Round LED);1;Y;Y;0;0;0;Y;Y;N;N;101;Default;|2.54;0;;;8.4;;;0.4;0.5;0.75;0.25;"
            "-0.1;0.4;0.5;0.75;0.25;-0.1;2.95;3.2;3.45;0.25;-0.25;0.889;1.5;N;2.65;2.9;3.15;0.25;-0.25;"
            "3.3;3.6;3.9;0.3;-0.3;;;3.5;;;0;2;0|0;|;;;;0.5|||||;;;;1|||||||||4079359;15461355;16119285;N]"
        )

        point_1 = Point()
        point_1.x = -1.6
        point_1.y = 1.6

        point_2 = Point()
        point_2.x = 1.45
        point_2.y = 0.93

        point_3 = Point()
        point_3.x = 0.0
        point_3.y = 1.73

        point_4 = Point()
        point_4.x = -1.7774
        point_4.y = 1.7774

        point_5 = Point()
        point_5.x = -1.2774
        point_5.y = 1.2774

        point_6 = Point()
        point_6.x = -1.73
        point_6.y = 1.73

        point_7 = Point()
        point_7.x = -2.2466
        point_7.y = 2.2466

        point_8 = Point()
        point_8.x = -1.2466
        point_8.y = 1.2466

        point_9 = Point()
        point_9.x = -2.27
        point_9.y = 2.27

        shape_1 = PatternShape()
        shape_1.id = 1
        shape_1.type = ShapeType.Obround
        shape_1.locked = Boolean.Yes
        shape_1.layer = Layer.TopOutline
        shape_1.line_width = 0.05
        shape_1.all_layers = Boolean.No
        shape_1.points = [point_1, point_1.flip_xy]

        shape_2 = PatternShape()
        shape_2.id = 2
        shape_2.type = ShapeType.Arc
        shape_2.locked = Boolean.Yes
        shape_2.layer = Layer.TopSilk
        shape_2.line_width = 0.12
        shape_2.all_layers = Boolean.No
        shape_2.points = [point_2, point_3, point_2.flip_x]

        shape_3 = PatternShape()
        shape_3.id = 3
        shape_3.type = ShapeType.Arc
        shape_3.locked = Boolean.Yes
        shape_3.layer = Layer.TopSilk
        shape_3.line_width = 0.12
        shape_3.all_layers = Boolean.No
        shape_3.points = [point_2.flip_y, point_3.flip_y, point_2.flip_xy]

        shape_4 = PatternShape()
        shape_4.id = 4
        shape_4.type = ShapeType.FillObround
        shape_4.locked = Boolean.Yes
        shape_4.layer = Layer.TopSilk
        shape_4.all_layers = Boolean.No
        shape_4.points = [point_4, point_5]

        shape_5 = PatternShape()
        shape_5.id = 5
        shape_5.type = ShapeType.Obround
        shape_5.locked = Boolean.Yes
        shape_5.layer = Layer.TopAssembly
        shape_5.line_width = 0.12
        shape_5.all_layers = Boolean.No
        shape_5.points = [point_6, point_6.flip_xy]

        shape_6 = PatternShape()
        shape_6.id = 6
        shape_6.type = ShapeType.FillObround
        shape_6.locked = Boolean.Yes
        shape_6.layer = Layer.TopAssembly
        shape_6.all_layers = Boolean.No
        shape_6.points = [point_7, point_8]

        shape_7 = PatternShape()
        shape_7.id = 7
        shape_7.type = ShapeType.Obround
        shape_7.locked = Boolean.Yes
        shape_7.layer = Layer.TopCourtyard
        shape_7.line_width = 0.05
        shape_7.all_layers = Boolean.No
        shape_7.points = [point_9, point_9.flip_xy]

        pattern = Pattern()
        pattern.name = "LED-3mm Round Red"
        pattern.ref_des = "D"
        pattern.mounting = PatternMounting.Through
        pattern.width = 4.54
        pattern.height = 4.54
        pattern.orientation = 0.0
        pattern.locked = Boolean.Yes
        pattern.type = PatternType.IPC_7351
        pattern.parameters = 0.0, 0.0, 0.0, 1, 0
        pattern.name_description = (
            "LED, Radial Diameter, 2.54mm lead spacing, 0.5mm lead width, " "3.45mm body diameter, 8.4mm height, red"
        )
        pattern.name_unique = "KINGBRIGHT_LED-3R_RED"
        pattern.manufacturer = "Kingbright"
        pattern.datasheet = "http://drawings.diptrace.com/kingbright/LED-3R_RED.pdf"
        pattern.origin = origin
        pattern.recovery_code = recovery_code
        pattern.default_pad_style = pad_style_1.name
        pattern.pads = [pad_1, pad_2]
        pattern.shapes = [shape_1, shape_2, shape_3, shape_4, shape_5, shape_6, shape_7]
        pattern.model3d = model3d

        library = PatternLibrary()
        library.name = "LED Radial Round 3mm"
        library.hint = "LED - Radial - Round - 3mm (T1) Lens Diameter"
        library.version = "4.3.0.5"
        library.units = Units.mm
        library.pad_styles = [pad_style_1, pad_style_2]
        library.patterns = [pattern]

        actual_filename = self.path.joinpath("./samples/actual_led_3mm")
        expected_filename = self.path.joinpath("./samples/expected_led_3mm.libxml")

        library.save(actual_filename)

        actual_filename = actual_filename.with_suffix(".libxml")

        format_xml(expected_filename)
        format_xml(actual_filename)

        expected = str(load_from_xml_file(expected_filename))
        actual = str(load_from_xml_file(actual_filename))
        # compare(expected_filename, actual_filename)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
