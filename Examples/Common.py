#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from typing import Optional
from pathlib import Path
from DipTraceGenerator import ComponentLibrary


path = Path(__file__).parent


def iec_symbols() -> Optional[ComponentLibrary]:
    iec_path = path.joinpath("source", "Symbols EIC.elixml")
    return ComponentLibrary.load(iec_path)


# def build(name: str, generator: Callable, *arg: Any, **kwarg: Any):
#     try:
#         print(colored(f"\n{name.title()}\n", "red"))
#         directory = name.lower().replace(" ", "-")

#         for source_path in path.joinpath("source", directory).glob("*.elixml"):
#             destination_path = path.joinpath("actual", directory, source_path.name)

#             print(colored(f"Generating {destination_path.name}...", "green"))

#             generator(source=source_path, destination=destination_path, name=name, *arg, **kwarg)

#             if destination_path.is_file():
#                 format_xml(destination_path)

#             expected_path = path.joinpath("expected", "resistors", source_path.name)
#             if expected_path.is_file():
#                 format_xml(expected_path)

#     except ValueError as e:
#         print(colored(str(e), "red"))


if __name__ == "__main__":
    pass
