#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from lxml.etree import fromstring as xml
from DipTraceGenerator.Category import Category, CategoryType, CategoriesMixin


class TestCategories(unittest.TestCase):
    def test_001(self):
        category = Category()

        self.assertEqual(None, category.name)
        self.assertEqual(None, category.number)
        self.assertEqual(None, category.types)

    def test_002(self):
        category = Category(
            xml(
                '<Category Number="0">\n'
                "	<Name>'BGA</Name>\n"
                "	<Types>\n"
                '		<Type Number="0">\n'
                "			<Name>'''''''''Package Length (X) 0.57mm</Name>\n"
                "			<SubTypes/>\n"
                "		</Type>\n"
                '		<Type Number="1">\n'
                "			<Name>'''''''''Package Length (X) 0.626mm</Name>\n"
                "			<SubTypes/>\n"
                "		</Type>\n"
                "	</Types>\n"
                "</Category>\n"
            )
        )

        self.assertEqual("'BGA", category.name)
        self.assertEqual(0, category.number)
        self.assertEqual(2, len(category.types))

        self.assertEqual(0, category.types[0].number)
        self.assertEqual("'''''''''Package Length (X) 0.57mm", category.types[0].name)

        self.assertEqual(1, category.types[1].number)
        self.assertEqual("'''''''''Package Length (X) 0.626mm", category.types[1].name)

    def test_003(self):
        type_1 = CategoryType()
        type_1.name = "''''''Atypical Numeration"

        type_2 = CategoryType()
        type_2.name = "'''''Overall Length (Y) by Leads 16.8mm"

        category = Category()
        category.number = 1
        category.name = "'BQFP"
        category.types = [type_1, type_2]
        category.renumerate()

        self.assertEqual("'BQFP", category.name)
        self.assertEqual(1, category.number)
        self.assertEqual(2, len(category.types))

        self.assertEqual(0, category.types[0].number)
        self.assertEqual("''''''Atypical Numeration", category.types[0].name)

        self.assertEqual(1, category.types[1].number)
        self.assertEqual("'''''Overall Length (Y) by Leads 16.8mm", category.types[1].name)

        expected = (
            '<Category Number="1">\n'
            "  <Name>'BQFP</Name>\n"
            "  <Types>\n"
            '    <Type Number="0">\n'
            "      <Name>''''''Atypical Numeration</Name>\n"
            "    </Type>\n"
            '    <Type Number="1">\n'
            "      <Name>'''''Overall Length (Y) by Leads 16.8mm</Name>\n"
            "    </Type>\n"
            "  </Types>\n"
            "</Category>\n"
        )

        actual = str(category)

        self.assertEqual(expected, actual)

    def test_mixin_001(self):
        class Library(CategoriesMixin):
            pass

        library = Library()

        self.assertIsNotNone(library.categories)
        self.assertListEqual([], library.categories)

        library.categories = [
            Category(
                xml(
                    '<Category Number="3">\n'
                    "  <Name>'BQFP</Name>\n"
                    "  <Types>\n"
                    '    <Type Number="0">\n'
                    "      <Name>''''''Atypical Numeration</Name>\n"
                    "    </Type>\n"
                    '    <Type Number="1">\n'
                    "      <Name>'''''Overall Length (Y) by Leads 16.8mm</Name>\n"
                    "    </Type>\n"
                    "  </Types>\n"
                    "</Category>\n"
                )
            )
        ]

        self.assertIsNotNone(library.categories)
        self.assertEqual(1, len(library.categories))
        self.assertEqual("''''''Atypical Numeration", library.categories[0].types[0].name)
        self.assertEqual(3, library.categories[0].number)

        library.renumerate()
        self.assertEqual(0, library.categories[0].number)

        library.categories = None

        self.assertIsNotNone(library.categories)
        self.assertListEqual([], library.categories)


if __name__ == "__main__":
    unittest.main()
