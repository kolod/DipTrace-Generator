#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from tqdm import tqdm
from pathlib import Path
from colorama import init, Fore
from DipTraceGenerator import Component, ComponentLibrary, format_xml
from Examples import iec_symbols


def is_polarized(component: Component) -> bool:
    if component.name is not None:
        if component.name.lower().startswith("capp"):
            return True
        if component.name.lower().startswith("cap"):
            return False

    if component.pattern is not None:
        if component.pattern.name is not None:
            if component.pattern.name.lower().startswith("capp"):
                return True
            if component.pattern.name.lower().startswith("cap"):
                return False

    raise ValueError(
        f"It isn't possible to determine if the capacitor `{component.name}` is polarized."
    )


def capacitor(source: Path, destination: Path, polarized_name: str, non_polarized_name: str):
    library = ComponentLibrary.load(source)

    template_library = iec_symbols()
    if template_library is None:
        raise ValueError("Template library not loaded.")

    polarized = template_library.find(polarized_name)
    if polarized is None:
        raise ValueError(f"Template component `{polarized_name}` not loaded.")

    non_polarized = template_library.find(non_polarized_name)
    if non_polarized is None:
        raise ValueError(f"Template component `{non_polarized_name}` not loaded.")

    for component in tqdm(library.components, desc='Elements'):
        if component.name is None:
            raise ValueError("Component must have name")

        try:
            template_component = polarized if is_polarized(component) else polarized
        except ValueError as e:
            print(Fore.RED + str(e) + Fore.RESET)
            continue

        for i in range(len(component.parts)):
            if len(component.parts[i].pins) != 2:
                tqdm.write(f"Component part must have two pins. Skip `{component.name}`.")
                continue

            pads = [x.pad_number for x in component.parts[i].pins]
            component.parts[i].shapes = template_component.parts[0].shapes
            component.parts[i].pins = template_component.parts[0].pins
            component.parts[i].origin = template_component.parts[0].origin

            for j, pad in enumerate(pads):
                component.parts[i].pins[j].pad_number = pad

    library.save(destination)


def capacitors() -> None:
    try:
        init()
        print(Fore.RED + "\nCapacitors\n" + Fore.RESET)

        directory = "capacitors"
        path = Path(__file__).parent

        for source_path in (path / "source" / directory).glob("*.elixml"):
            destination_path = path / "actual" / directory / source_path.name
            expected_path = path / "expected" / directory / source_path.name

            print(Fore.GREEN + f"Generating {destination_path.name}..." + Fore.RESET)

            capacitor(
                source=source_path,
                destination=destination_path,
                polarized_name="CAP",
                non_polarized_name="CAP_POLARIZED",
            )

            if destination_path.is_file():
                format_xml(destination_path)

            if expected_path.is_file():
                format_xml(expected_path)

    except ValueError as e:
        print(Fore.RED + str(e) + Fore.RESET)


if __name__ == "__main__":
    capacitors()
