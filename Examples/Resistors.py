#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from tqdm import tqdm
from colorama import init, Fore
from pathlib import Path
from DipTraceGenerator import ComponentLibrary, format_xml
from Examples import iec_symbols


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


    for component in tqdm(library.components, desc='Elements'):
        for i in range(len(component.parts)):
            if len(component.parts[i].pins) != 2:
                msg = f"Component part must have two pins. Skip `{component.name}`."
                tqdm.write(msg)
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
        init()
        print(Fore.RED + "\nResistors\n" + Fore.RESET)

        directory = "resistors"
        path = Path(__file__).parent

        for source_path in (path / "source" / directory).glob("*.elixml"):
            destination_path = path / "actual" / directory / source_path.name
            expected_path = path / "expected" / directory / source_path.name

            print(Fore.GREEN + f"Generating {destination_path.name}..." + Fore.RESET)

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
        print(Fore.RED + str(e) + Fore.RESET)


if __name__ == "__main__":
    resistors()
