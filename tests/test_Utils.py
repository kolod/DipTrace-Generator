#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from pathlib import Path
from DipTraceGenerator import format_xml, get_correct_filename


class Test(unittest.TestCase):
    def test_get_correct_filename(self):
        path = Path(__file__).parent
        path_test = path.joinpath("test")
        path_libxml = path_test.with_suffix(".libxml")
        path_elixml = path_test.with_suffix(".elixml")

        if path_libxml.is_file():
            path_libxml.unlink()

        if path_elixml.is_file():
            path_elixml.unlink()

        with self.assertRaises(TypeError) as cm:
            get_correct_filename(path_test)
        self.assertEqual(
            "get_correct_filename() missing 1 required positional argument: 'extensions'", str(cm.exception)
        )

        with self.assertRaises(ValueError) as cm:
            get_correct_filename(path_test, ["", ".libxml", ".elixml"])
        self.assertEqual(f'File "{str(path_test.resolve())}" does not exist.', str(cm.exception))

        path_libxml.touch()
        self.assertEqual(
            str(path_libxml.resolve()), str(get_correct_filename(path_test, ["", ".libxml", ".elixml"]).resolve())
        )
        path_libxml.unlink()

        path_elixml.touch()
        self.assertEqual(
            str(path_elixml.resolve()), str(get_correct_filename(path_test, ["", ".libxml", ".elixml"]).resolve())
        )
        path_elixml.unlink()

    def test_format(self):
        path = Path(__file__).parent
        expected_filename = path.joinpath("samples/part_test.sample.xml")
        actual_filename = path.joinpath("samples/format_test.sample.xml")

        with open(expected_filename, "r", encoding="utf-8") as expected_file:
            with open(actual_filename, "w", encoding="utf-8") as actual_file:
                for line in expected_file.readlines():
                    actual_file.write(line.strip() + "\n")
                actual_file.flush()
                actual_file.close()
            expected_file.close()

        format_xml(actual_filename)

        with open(expected_filename, "r", encoding="utf-8") as expected_file:
            with open(actual_filename, "r", encoding="utf-8") as actual_file:
                expected = expected_file.read()
                actual = actual_file.read()
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
