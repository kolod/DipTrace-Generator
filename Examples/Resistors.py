#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from pathlib import Path
from rich.progress import track
from rich.console import Console
from rich.style import Style
from DipTraceGenerator import ComponentLibrary, format_xml
from Examples import iec_symbols

console = Console()


def resistor(source: Path, destination: Path, template_name: str):
    library = ComponentLibrary.load(source)
    if library is None:
        raise ValueError(f'Source file "{source}" not loaded.')

    template_library = iec_symbols()
    if template_library is None:
        raise ValueError("Template library not loaded.")

    template_component = template_library.find(template_name)
    if template_component is None:
        raise ValueError(f"Template component `{template_name}` not loaded.")


    for component in track(library.components, description='Elements'):
        for i in range(len(component.parts)):
            if len(component.parts[i].pins) != 2:
                msg = f"Component part must have two pins. Skip `{component.name}`."
                console.print(msg)
                continue

            pads = [x.pad_number for x in component.parts[i].pins]
            component.parts[i].shapes = template_component.parts[0].shapes
            component.parts[i].pins = template_component.parts[0].pins
            component.parts[i].origin = template_component.parts[0].origin

            for j, pad in enumerate(pads):
                component.parts[i].pins[j].pad_number = pad

    library.save(destination)


def resistors() -> None:
    try:
        console.print("\nResistors\n", style="red bold")

        directory = "resistors"
        path = Path(__file__).parent

        for source_path in (path / "source" / directory).glob("*.elixml"):
            destination_path = path / "actual" / directory / source_path.name
            expected_path = path / "expected" / directory / source_path.name

            console.print(f"Generating {destination_path.name}...", style="green")

            resistor(
                source=source_path,
                destination=destination_path,
                template_name="RES"
            )

            if destination_path.is_file():
                format_xml(destination_path)

            if expected_path.is_file():
                format_xml(expected_path)


    except ValueError as e:
        console.print(str(e), style="red bold")


if __name__ == "__main__":
    resistors()
