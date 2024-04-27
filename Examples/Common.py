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


if __name__ == "__main__":
    pass
