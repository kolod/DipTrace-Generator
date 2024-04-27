#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from tqdm import tqdm
from typing import List
from pathlib import Path
from colorama import init, Fore
from dataclasses import dataclass
from DipTraceGenerator import *
from math import sin, radians


@dataclass
class TVS:
    voltage: float
    uni: str
    bi: str


def pins() -> List[Pin]:
    font = NameFont(size=5.0, width=-2, scale=1.0)

    return [
        Pin(
            x=-1.27,
            y=0.0,
            locked=Boolean.Yes,
            type=PinType.Default,
            electric_type=ElectricType.Undefined,
            orientation=0.0,
            length=2.54,
            show_name=Boolean.No,
            number_shift=Shift(),
            name_shift=Shift(),
            delay=0.0,
            name="1",
            pad_number="1",
            name_font=font,
            pad_id=1,
        ),
        Pin(
            x=1.27,
            y=0.0,
            locked=Boolean.Yes,
            type=PinType.Default,
            electric_type=ElectricType.Undefined,
            orientation=180.0,
            length=2.54,
            show_name=Boolean.No,
            number_shift=Shift(),
            name_shift=Shift(),
            delay=0.0,
            name="2",
            pad_number="2",
            name_font=font,
            pad_id=2,
        ),
    ]


def pin_shape_uni() -> List[ComponentShape]:
    x = 1.27 * sin(radians(60.0))

    point_1 = Point(x=1.27, y=0.0)
    point_2 = Point(x=x, y=0.0)
    point_3 = Point(x=x, y=1.27)
    point_4 = Point(x=x - 1.27 / 2, y=-1.27)

    return [
        ComponentShape(type=ShapeType.Line, line_width=0.25, locked=Boolean.Yes, points=[point_1.flip_x, point_1]),
        ComponentShape(
            type=ShapeType.Polyline,
            line_width=0.25,
            locked=Boolean.Yes,
            points=[point_3.flip_x, point_2, point_3.flip_xy, point_3.flip_x],
        ),
        ComponentShape(
            type=ShapeType.Polyline, line_width=0.25, locked=Boolean.Yes, points=[point_3, point_3.flip_y, point_4]
        ),
    ]


def pin_shape_bi() -> List[ComponentShape]:
    x = 2.54 * sin(radians(60.0))

    point_1 = Point(x=1.27, y=0.0)
    point_2 = Point(x=0.0, y=0.0)
    point_3 = Point(x=x, y=1.27)
    point_4 = Point(x=1.27 / 2, y=1.27)
    point_5 = Point(x=0.0, y=1.27)

    return [
        ComponentShape(type=ShapeType.Line, line_width=0.25, locked=Boolean.Yes, points=[point_1.flip_x, point_1]),
        ComponentShape(
            type=ShapeType.Polyline,
            line_width=0.25,
            locked=Boolean.Yes,
            points=[point_2, point_3.flip_x, point_3.flip_xy, point_2, point_3, point_3.flip_y, point_2],
        ),
        ComponentShape(
            type=ShapeType.Polyline,
            line_width=0.25,
            locked=Boolean.Yes,
            points=[point_4, point_5, point_5.flip_y, point_4.flip_xy],
        ),
    ]


def component(name: str, voltage: float, pattern: str, origin: ComponentOrigin, category: Category, spice: SpiceModel, shapes: List[ComponentShape]) -> Component:
    return Component(parts=[Part(
        ref_des="D",
        part_type=PartType.Normal,
        show_numbers=Visible.Hide,
        style=PartStyle.TwoSides,
        parameters=(1, 1),
        part_name="Part 1",
        origin=origin,
        datasheet="https://www.diodes.com/assets/Datasheets/SMAJ5.0CA-SMAJ200CA.pdf",
        spice=spice,
        manufacturer="Diodes",
        category=category,
        pins=pins(),
        width=2.54,
        height=2.54,
        locked=Boolean.Yes,
        sub_folder_index=-1,
        name=name,
        value=f'{voltage:.5g} V',
        shapes=shapes,
        pattern=pattern
    )])


def diode_tvs(source: Path, destination: Path, name: str, data: List[TVS]):
    pattern_library = PatternLibrary.load(source.with_suffix(PatternLibrary.extension))
    origin = ComponentOrigin(x=0.0, y=0.0)
    category = Category(name="Diodes")
    spice = SpiceModel(type=SpiceModelType.SubComponent)
    components: List[Component] = []

    print(Fore.GREEN + 'Bidirectional' + Fore.RESET)
    components.append(Component(name='--- Bidirectional --'))
    for tvs in tqdm(data, desc='Elements'):
        components.append(component(tvs.bi, tvs.voltage, 'PatType0', origin, category, spice, pin_shape_bi()))

    print(Fore.GREEN + 'Unidirectional' + Fore.RESET)
    components.append(Component(name='-- Unidirectional --'))
    for tvs in tqdm(data, desc='Elements'):
        components.append(component(tvs.uni, tvs.voltage, 'PatType1', origin, category, spice, pin_shape_uni()))

    component_library = ComponentLibrary()
    component_library.name = name
    component_library.hint = name
    component_library.pattern_library = pattern_library.renumerate()
    component_library.components = components
    component_library.save(destination)


def diodes_tvs():
    try:
        init()
        print(Fore.RED + "\nDiodes TVS\n" + Fore.RESET)

        name = "Diodes TVS"
        directory = "diodes-tvs"
        path = Path(__file__).parent

        source_path = path / "source" / directory / f"{name}.libxml"
        destination_path = path / "actual" / directory / f"{name}.elixml"
        expected_path = path / "expected" / directory / f"{name}.elixml"

        print(Fore.GREEN + f"Generating {destination_path.name}..." + Fore.RESET)

        diode_tvs(
            source=source_path,
            destination=destination_path,
            name=name,
            data=[
                TVS(uni="SMAJ5.0A", bi="SMAJ5.0CA", voltage=5.0),
                TVS(uni="SMAJ6.0A", bi="SMAJ6.0CA", voltage=6.0),
                TVS(uni="SMAJ6.5A", bi="SMAJ6.5CA", voltage=6.5),
                TVS(uni="SMAJ7.0A", bi="SMAJ7.0CA", voltage=7.0),
                TVS(uni="SMAJ7.5A", bi="SMAJ7.5CA", voltage=7.5),
                TVS(uni="SMAJ8.0A", bi="SMAJ8.0CA", voltage=8.0),
                TVS(uni="SMAJ8.5A", bi="SMAJ8.5CA", voltage=8.5),
                TVS(uni="SMAJ9.0A", bi="SMAJ9.0CA", voltage=9.0),
                TVS(uni="SMAJ10A", bi="SMAJ10CA", voltage=10.0),
                TVS(uni="SMAJ11A", bi="SMAJ11CA", voltage=11.0),
                TVS(uni="SMAJ12A", bi="SMAJ12CA", voltage=12.0),
                TVS(uni="SMAJ13A", bi="SMAJ13CA", voltage=13.0),
                TVS(uni="SMAJ14A", bi="SMAJ14CA", voltage=14.0),
                TVS(uni="SMAJ15A", bi="SMAJ15CA", voltage=15.0),
                TVS(uni="SMAJ16A", bi="SMAJ16CA", voltage=16.0),
                TVS(uni="SMAJ17A", bi="SMAJ17CA", voltage=17.0),
                TVS(uni="SMAJ18A", bi="SMAJ18CA", voltage=18.0),
                TVS(uni="SMAJ20A", bi="SMAJ20CA", voltage=20.0),
                TVS(uni="SMAJ22A", bi="SMAJ22CA", voltage=22.0),
                TVS(uni="SMAJ24A", bi="SMAJ24CA", voltage=24.0),
                TVS(uni="SMAJ26A", bi="SMAJ26CA", voltage=26.0),
                TVS(uni="SMAJ28A", bi="SMAJ28CA", voltage=28.0),
                TVS(uni="SMAJ30A", bi="SMAJ30CA", voltage=30.0),
                TVS(uni="SMAJ33A", bi="SMAJ33CA", voltage=33.0),
                TVS(uni="SMAJ36A", bi="SMAJ36CA", voltage=36.0),
                TVS(uni="SMAJ40A", bi="SMAJ40CA", voltage=40.0),
                TVS(uni="SMAJ43A", bi="SMAJ43CA", voltage=43.0),
                TVS(uni="SMAJ45A", bi="SMAJ45CA", voltage=45.0),
                TVS(uni="SMAJ48A", bi="SMAJ48CA", voltage=48.0),
                TVS(uni="SMAJ51A", bi="SMAJ51CA", voltage=51.0),
                TVS(uni="SMAJ54A", bi="SMAJ54CA", voltage=54.0),
                TVS(uni="SMAJ58A", bi="SMAJ58CA", voltage=58.0),
                TVS(uni="SMAJ60A", bi="SMAJ60CA", voltage=60.0),
                TVS(uni="SMAJ64A", bi="SMAJ64CA", voltage=64.0),
                TVS(uni="SMAJ70A", bi="SMAJ70CA", voltage=70.0),
                TVS(uni="SMAJ75A", bi="SMAJ75CA", voltage=75.0),
                TVS(uni="SMAJ78A", bi="SMAJ78CA", voltage=78.0),
                TVS(uni="SMAJ85A", bi="SMAJ85CA", voltage=85.0),
                TVS(uni="SMAJ90A", bi="SMAJ90CA", voltage=90.0),
                TVS(uni="SMAJ100A", bi="SMAJ100CA", voltage=100.0),
                TVS(uni="SMAJ110A", bi="SMAJ110CA", voltage=110.0),
                TVS(uni="SMAJ120A", bi="SMAJ120CA", voltage=120.0),
                TVS(uni="SMAJ130A", bi="SMAJ130CA", voltage=130.0),
                TVS(uni="SMAJ150A", bi="SMAJ150CA", voltage=150.0),
                TVS(uni="SMAJ160A", bi="SMAJ160CA", voltage=160.0),
                TVS(uni="SMAJ170A", bi="SMAJ170CA", voltage=170.0),
                TVS(uni="SMAJ180A", bi="SMAJ180CA", voltage=180.0),
                TVS(uni="SMAJ200A", bi="SMAJ200CA", voltage=200.0),
                TVS(uni="SMAJ220A", bi="SMAJ220CA", voltage=220.0),
                TVS(uni="SMAJ250A", bi="SMAJ250CA", voltage=250.0),
                TVS(uni="SMAJ300A", bi="SMAJ300CA", voltage=300.0),
                TVS(uni="SMAJ350A", bi="SMAJ350CA", voltage=350.0),
                TVS(uni="SMAJ400A", bi="SMAJ400CA", voltage=400.0),
                TVS(uni="SMAJ440A", bi="SMAJ440CA", voltage=440.0),
            ]
        )

        if destination_path.is_file():
            format_xml(destination_path)

        if expected_path.is_file():
            format_xml(expected_path)


    except ValueError as e:
        print(Fore.RED + str(e) + Fore.RESET)


if __name__ == "__main__":
    diodes_tvs()
