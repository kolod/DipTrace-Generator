#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2025-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

# To run the tests, use:
# poetry run pytest tests/test_NameFont.py -v

# To run the tests with coverage report in terminal, use:
# poetry run pytest --cov=DipTraceGenerator.NameFont tests/test_NameFont.py -v --cov-report=term --cov-report=term-missing


from unittest import TestCase, main
from lxml.etree import fromstring as xml
from DipTraceGenerator import NameFont


class TestNameFont(TestCase):
    """Test cases for NameFont class"""

    def test_namefont_default_initialization(self):
        """Test NameFont initializes with default values"""
        font = NameFont()
        self.assertEqual(font.size, 5)
        self.assertEqual(font.width, -2)
        self.assertEqual(font.scale, 1.0)

    def test_namefont_initialization_with_values(self):
        """Test NameFont initialization with explicit values"""
        font = NameFont(size=10, width=-3, scale=1.5)
        self.assertEqual(font.size, 10)
        self.assertEqual(font.width, -3)
        self.assertEqual(font.scale, 1.5)

    def test_namefont_from_xml(self):
        """Test creating NameFont from XML"""
        xml_str = '<NameFont Size="12" Width="-4" Scale="2.0"/>'
        element = xml(xml_str)
        font = NameFont.from_xml(element)
        
        self.assertEqual(font.size, 12)
        self.assertEqual(font.width, -4)
        self.assertEqual(font.scale, 2.0)

    def test_namefont_from_xml_with_defaults(self):
        """Test creating NameFont from XML with missing attributes"""
        xml_str = '<NameFont/>'
        element = xml(xml_str)
        font = NameFont.from_xml(element)
        
        self.assertEqual(font.size, 5)
        self.assertEqual(font.width, -2)
        self.assertEqual(font.scale, 1.0)

    def test_namefont_to_xml(self):
        """Test converting NameFont to XML"""
        font = NameFont(size=8, width=-1, scale=1.2)
        element = font.to_xml()
        
        self.assertEqual(element.tag, "NameFont")
        self.assertEqual(element.get("Size"), "8")
        self.assertEqual(element.get("Width"), "-1")
        self.assertEqual(element.get("Scale"), "1.2")

    def test_namefont_roundtrip(self):
        """Test NameFont XML roundtrip conversion"""
        original = NameFont(size=15, width=-5, scale=2.5)
        element = original.to_xml()
        restored = NameFont.from_xml(element)
        
        self.assertEqual(restored.size, original.size)
        self.assertEqual(restored.width, original.width)
        self.assertEqual(restored.scale, original.scale)


if __name__ == "__main__":
    main()
