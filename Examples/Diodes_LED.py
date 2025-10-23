#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from copy import deepcopy
from typing import List
from pathlib import Path
from rich.progress import track
from rich.console import Console
from rich.style import Style
from DipTraceGenerator import *
from . import iec_symbols

console = Console()


def led(source: Path, destination: Path, template_name: str, name:str, colors: List[str], sizes: List[str], **_):
    pattern_library = PatternLibrary.load(source)
    if pattern_library is None:
        raise ValueError(f'Pattern library "{source.name}" was not loaded.')

    template_library = iec_symbols()
    if template_library is None:
        raise ValueError(f'Component library "{source.name}" was not loaded.')

    component_template = template_library.find(template_name)
    if component_template is None:
        raise ValueError(f'Template component `{template_name}` not loaded.')

    components = []
    for size in sizes:
        pattern = pattern_library.find(f'LED-{size}')
        if pattern is None:
            raise ValueError(f'Template component `{pattern}` not loaded.')

        console.print(size, style="green")
        components.append(Component(name=f'--- {size} ---'))

        for color in track(colors, description='Elements'):
            component = deepcopy(component_template)
            component.parts[0].name = f'led-{size}-{color}'
            component.parts[0].pattern = pattern.style
            component.parts[0].pins[0].pad_number = pattern.pads[0].number
            component.parts[0].pins[1].pad_number = pattern.pads[1].number
            components.append(component)

    library = ComponentLibrary()
    library.name = name.title()
    library.hint = name.title()
    library.pattern_library = pattern_library
    library.components = components
    library.save(destination)


def diodes_led():
    try:
        console.print("\nDiodes LED\n", style="red bold")

        name = "leds"
        directory = "leds"
        path = Path(__file__).parent

        source_path = path / "source" / directory / f"{name}.libxml"
        destination_path = path / "actual" / directory / f"{name}.elixml"
        expected_path = path / "expected" / directory / f"{name}.elixml"

        console.print(f"Generating {destination_path.name}...", style="green")

        led(
            source=source_path,
            destination=destination_path,
            template_name='DIO_LIGHT',
            name='leds',
            colors = ["green", "red", "orange", "clear"],
            sizes = ["3mm", "5mm"]
        )

        if destination_path.is_file():
            format_xml(destination_path)

        if expected_path.is_file():
            format_xml(expected_path)


    except ValueError as e:
        console.print(str(e), style="red bold")


def main():
    diodes_led()

if __name__ == "__main__":
    main()
