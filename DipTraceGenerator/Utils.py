#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2021-... Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from os import remove, fdopen
from pathlib import Path
from typing import List, Union
from subprocess import Popen, call
from lxml.etree import parse, XMLParser, tostring
from tempfile import mkstemp
from DipTraceGenerator.ComponentLibrary import ComponentLibrary
from DipTraceGenerator.PatternLibrary import PatternLibrary


def get_correct_filename(path: Path, extensions: List[str]) -> Path:
    if path.is_file():
        return path

    for extension in extensions:
        if (p := Path(f"{path}{extension}")).is_file():
            return p

    raise ValueError(f'File "{path}" does not exist.')


def format_xml(filename: Path):
    if (filename := get_correct_filename(filename, ["xml", "libxml", "elixml"])) is not None:
        parser = XMLParser(remove_blank_text=True)
        xml = parse(filename, parser)
        xml.write(filename, method="xml", xml_declaration=True, encoding="utf-8", pretty_print=True)


def compare(*args: Union[Path, str]) -> None:
    """
    | Compare **two** or **three** XML files or it's parts by xpath's
    |
    | Note:
    |     Number of xpath arguments must be equal to number of files or less than two.
    |     If xpath argument is only one then it applies to all files.
    |
    | Examples:
    |     >>> from pathlib import Path # Initialize
    |     >>> expected_file = Path('ExpectedLibrary.xml')
    |     >>> actual_file = Path('ActualLibrary.xml')
    |     >>> source_file = Path('SourceLibrary.xml')
    |
    |     Compare two files:
    |     >>> compare(expected_file, actual_file)
    |
    |     Compare three files:
    |     >>> compare(expected_file, actual_file, source_file)
    |
    |     Compare fragments of two files by the same xpath (all variants equivalent):
    |     >>> compare(expected_file, actual_file, './Parts/Part["@id=1"]')
    |     >>> compare('./Parts/Part["@id=1"]', expected_file, actual_file)
    |
    |     Compare fragments of two files (all variants equivalent):
    |     >>> compare(Path(expected_file, actual_file, './Parts/Part["@id=1"]', './Parts/Part["@id=2"]')
    |     >>> compare(Path(expected_file, './Parts/Part["@id=1"]', actual_file, './Parts/Part["@id=2"]')
    |     >>> compare(Path('./Parts/Part["@id=1"]', './Parts/Part["@id=2"]', expected_file, actual_file)
    |
    | Args:
    |     args (Union[Path,str]): A list of files or xpath to compare
    |
    | Returns:
    |     None
    """

    extensions = ["", "xml"]
    files = [get_correct_filename(x, extensions) for x in args if isinstance(x, Path)]
    paths = [x for x in args if isinstance(x, str)]

    if len(files) < 2:
        raise ValueError("Too low files. Expected two or three files.")

    if len(files) > 3:
        raise ValueError("Too many files. Expected two or three files.")

    if (len(files) != len(paths)) and (len(paths) > 1):
        raise ValueError("Number of xpath's must be equal to the number of files or less then two.")

    if len(paths) == 0:
        for file in files:
            format_xml(file)
        Popen(["C:/Program Files/WinMerge/WinMergeU.exe", "/s", *files])
    else:
        parser = XMLParser(remove_blank_text=True)

        tmp_files = []

        try:
            for i, file in enumerate(files):
                tmp_fd, tmp_name = mkstemp(suffix=".xml")
                with fdopen(tmp_fd, "wb") as tmp_f:
                    xml = parse(file, parser)
                    tag = xml.find(paths[0] if len(paths) == 1 else paths[i])
                    tmp_f.write(tostring(tag, method="xml", xml_declaration=False, encoding="utf-8", pretty_print=True))
                    tmp_files.append(tmp_name)

            call(executable="C:/Program Files/WinMerge/WinMergeU.exe", args=["/s", *tmp_files])
        finally:
            for tmp_name in tmp_files:
                remove(tmp_name)


def load_from_xml_file(path: Path) -> Union[PatternLibrary, ComponentLibrary, None]:
    if path.suffix in [".xml", ".libxml", ".elixml"]:
        if path.is_file():
            if (root := parse(path).getroot()) is not None:
                library_type = root.get("Type")
                if library_type == "DipTrace-PatternLibrary":
                    return PatternLibrary(root)
                elif library_type == "DipTrace-ComponentLibrary":
                    return ComponentLibrary(root)
    return None


if __name__ == "__main__":
    pass
