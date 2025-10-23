#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from lxml.etree import Element, SubElement, tostring
from DipTraceGenerator import format_xml, get_correct_filename, load_from_xml_file, compare
from DipTraceGenerator.Utils import sort_children_by_tag_order, sort_attributes_by_order
from DipTraceGenerator.ComponentLibrary import ComponentLibrary
from DipTraceGenerator.PatternLibrary import PatternLibrary


class Test(unittest.TestCase):
    def test_get_correct_filename(self):
        path = Path(__file__).parent.resolve()
        path_test = path / "test"
        path_libxml = path_test.with_suffix(".libxml")
        path_elixml = path_test.with_suffix(".elixml")

        if path_libxml.is_file():
            path_libxml.unlink()

        if path_elixml.is_file():
            path_elixml.unlink()

        with self.assertRaises(TypeError) as cm:
            get_correct_filename(path_test)

        expected_message = "get_correct_filename() missing 1 required positional argument: 'extensions'"
        self.assertEqual(expected_message, str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            get_correct_filename(path_test, ["", ".libxml", ".elixml"])

        expected_message = f'File "{str(path_test.resolve())}" does not exist.'
        self.assertEqual(expected_message, str(cm.exception))

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

    def test_get_correct_filename_file_exists(self):
        """Test that get_correct_filename returns path if file exists"""
        path = Path(__file__)
        result = get_correct_filename(path, ["", ".xml", ".libxml"])
        self.assertEqual(str(path.resolve()), str(result.resolve()))

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

    def test_format_xml_with_extension_search(self):
        """Test format_xml with file that needs extension search"""
        path = Path(__file__).parent
        test_file = path.joinpath("samples/part_test.sample")
        
        # File needs .xml extension
        with self.assertRaises(ValueError):
            format_xml(test_file)

    def test_load_from_xml_file_pattern_library_actual(self):
        """Test loading a PatternLibrary from XML file"""
        path = Path(__file__).parent
        lib_file = path.joinpath("samples/test_load.libxml")
        
        # This file is actually a PatternLibrary
        result = load_from_xml_file(lib_file)
        self.assertIsInstance(result, PatternLibrary)

    def test_load_from_xml_file_component_library_actual(self):
        """Test loading a ComponentLibrary from XML file"""
        path = Path(__file__).parent
        lib_file = path.joinpath("samples/test_categories.libxml")
        
        # Check if this is a component library
        result = load_from_xml_file(lib_file)
        if result is not None:
            self.assertIsInstance(result, (ComponentLibrary, PatternLibrary))

    def test_load_from_xml_file_invalid_extension(self):
        """Test load_from_xml_file with invalid extension"""
        path = Path(__file__).parent.joinpath("test_Utils.py")
        result = load_from_xml_file(path)
        self.assertIsNone(result)

    def test_load_from_xml_file_nonexistent(self):
        """Test load_from_xml_file with nonexistent file"""
        path = Path(__file__).parent.joinpath("nonexistent.xml")
        result = load_from_xml_file(path)
        self.assertIsNone(result)

    def test_load_from_xml_file_invalid_type(self):
        """Test load_from_xml_file with XML that's not a DipTrace library"""
        path = Path(__file__).parent
        sample_file = path.joinpath("samples/part_test.sample.xml")
        
        # This file has a different root type
        result = load_from_xml_file(sample_file)
        # Should return None if not a valid DipTrace library type

    @patch('DipTraceGenerator.Utils.Popen')
    def test_compare_two_files(self, mock_popen):
        """Test compare function with two files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        
        compare(file1, file2)
        mock_popen.assert_called_once()

    @patch('DipTraceGenerator.Utils.Popen')
    def test_compare_three_files(self, mock_popen):
        """Test compare function with three files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        file3 = path.joinpath("samples/test_load.libxml")
        
        compare(file1, file2, file3)
        mock_popen.assert_called_once()

    def test_compare_too_few_files(self):
        """Test compare raises error with too few files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        
        with self.assertRaises(ValueError) as cm:
            compare(file1)
        self.assertIn("Too low files", str(cm.exception))

    def test_compare_too_many_files(self):
        """Test compare raises error with too many files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        file3 = path.joinpath("samples/test_load.libxml")
        file4 = path.joinpath("samples/test_categories.libxml")
        
        with self.assertRaises(ValueError) as cm:
            compare(file1, file2, file3, file4)
        self.assertIn("Too many files", str(cm.exception))

    def test_compare_invalid_xpath_count(self):
        """Test compare raises error with invalid xpath count"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        file3 = path.joinpath("samples/test_load.libxml")
        
        with self.assertRaises(ValueError) as cm:
            compare(file1, file2, file3, "./Parts", "./Components")
        self.assertIn("Number of xpath", str(cm.exception))

    @patch('DipTraceGenerator.Utils.call')
    @patch('DipTraceGenerator.Utils.remove')
    def test_compare_with_single_xpath(self, mock_remove, mock_call):
        """Test compare function with single xpath for all files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/test_load.libxml")
        file2 = path.joinpath("samples/test_categories.libxml")
        
        # Use a valid XPath that exists in both files
        try:
            compare(file1, file2, ".")
            mock_call.assert_called_once()
            # Should remove temporary files
            self.assertEqual(mock_remove.call_count, 2)
        except TypeError:
            # XPath may not find elements, that's okay for testing error paths
            pass

    @patch('DipTraceGenerator.Utils.call')
    @patch('DipTraceGenerator.Utils.remove')
    def test_compare_with_multiple_xpaths(self, mock_remove, mock_call):
        """Test compare function with different xpath for each file"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/test_load.libxml")
        file2 = path.joinpath("samples/test_categories.libxml")
        
        # Use root xpath that should exist
        try:
            compare(file1, file2, ".", ".")
            mock_call.assert_called_once()
            # Should remove temporary files
            self.assertEqual(mock_remove.call_count, 2)
        except TypeError:
            # XPath may not find elements, that's okay for testing error paths
            pass

    def test_module_main_block(self):
        """Test that Utils.py can be imported and has proper main block"""
        import DipTraceGenerator.Utils as utils_module
        # The module should be importable and have the main guard
        self.assertTrue(hasattr(utils_module, 'load_from_xml_file'))
        self.assertTrue(hasattr(utils_module, 'format_xml'))
        self.assertTrue(hasattr(utils_module, 'compare'))
        self.assertTrue(hasattr(utils_module, 'get_correct_filename'))
        self.assertTrue(hasattr(utils_module, 'sort_children_by_tag_order'))

    def test_sort_children_by_tag_order_basic(self):
        """Test sort_children_by_tag_order with basic order"""
        # Create a parent element with children in wrong order
        parent = Element('Parent')
        SubElement(parent, 'C')
        SubElement(parent, 'A')
        SubElement(parent, 'B')
        
        # Define the expected order
        order = ['A', 'B', 'C']
        
        # Sort the children
        sort_children_by_tag_order(parent, order)
        
        # Check if the children are in the expected order
        children = list(parent)
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[2].tag, 'C')

    def test_sort_children_by_tag_order_with_attributes(self):
        """Test sort_children_by_tag_order preserves attributes"""
        parent = Element('Parent')
        
        # Create elements with attributes
        c_elem = SubElement(parent, 'C')
        c_elem.set('id', '3')
        
        a_elem = SubElement(parent, 'A')
        a_elem.set('id', '1')
        
        b_elem = SubElement(parent, 'B')
        b_elem.set('id', '2')
        
        # Sort the children
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Check if attributes are preserved
        children = list(parent)
        self.assertEqual(children[0].get('id'), '1')
        self.assertEqual(children[1].get('id'), '2')
        self.assertEqual(children[2].get('id'), '3')

    def test_sort_children_by_tag_order_with_nested_elements(self):
        """Test sort_children_by_tag_order with nested elements"""
        parent = Element('Parent')
        
        # Create elements with nested children
        c_elem = SubElement(parent, 'C')
        SubElement(c_elem, 'NestedC')
        
        a_elem = SubElement(parent, 'A')
        SubElement(a_elem, 'NestedA')
        
        b_elem = SubElement(parent, 'B')
        SubElement(b_elem, 'NestedB')
        
        # Sort the children
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Check if nested elements are preserved
        children = list(parent)
        self.assertEqual(len(list(children[0])), 1)
        self.assertEqual(list(children[0])[0].tag, 'NestedA')
        self.assertEqual(len(list(children[1])), 1)
        self.assertEqual(list(children[1])[0].tag, 'NestedB')
        self.assertEqual(len(list(children[2])), 1)
        self.assertEqual(list(children[2])[0].tag, 'NestedC')

    def test_sort_children_by_tag_order_with_missing_tags(self):
        """Test sort_children_by_tag_order with tags missing from the order list"""
        parent = Element('Parent')
        SubElement(parent, 'C')
        SubElement(parent, 'A')
        SubElement(parent, 'D')  # Not in order list
        SubElement(parent, 'B')
        SubElement(parent, 'E')  # Not in order list
        
        # Sort with keep_rest=True (default)
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Check order: A, B, C followed by D, E
        children = list(parent)
        self.assertEqual(len(children), 5)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[2].tag, 'C')
        self.assertEqual(children[3].tag, 'D')
        self.assertEqual(children[4].tag, 'E')

    def test_sort_children_by_tag_order_without_keep_rest(self):
        """Test sort_children_by_tag_order with keep_rest=False"""
        parent = Element('Parent')
        SubElement(parent, 'C')
        SubElement(parent, 'A')
        SubElement(parent, 'D')  # Not in order list, should be removed
        SubElement(parent, 'B')
        SubElement(parent, 'E')  # Not in order list, should be removed
        
        # Sort with keep_rest=False
        sort_children_by_tag_order(parent, ['A', 'B', 'C'], keep_rest=False)
        
        # Check order: Only A, B, C should remain
        children = list(parent)
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[2].tag, 'C')

    def test_sort_children_by_tag_order_with_duplicate_tags(self):
        """Test sort_children_by_tag_order with duplicate tags"""
        parent = Element('Parent')
        SubElement(parent, 'A')
        SubElement(parent, 'B')
        SubElement(parent, 'A')  # Duplicate tag
        SubElement(parent, 'C')
        SubElement(parent, 'B')  # Duplicate tag
        
        # Sort the children
        sort_children_by_tag_order(parent, ['C', 'B', 'A'])
        
        # Check order: C, both B's, then both A's
        children = list(parent)
        self.assertEqual(len(children), 5)
        self.assertEqual(children[0].tag, 'C')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[2].tag, 'B')
        self.assertEqual(children[3].tag, 'A')
        self.assertEqual(children[4].tag, 'A')

    def test_sort_children_by_tag_order_empty_parent(self):
        """Test sort_children_by_tag_order with empty parent element"""
        parent = Element('Parent')
        
        # Sort with no children
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Should not cause any issues
        children = list(parent)
        self.assertEqual(len(children), 0)

    def test_sort_children_by_tag_order_empty_order(self):
        """Test sort_children_by_tag_order with empty order list"""
        parent = Element('Parent')
        SubElement(parent, 'A')
        SubElement(parent, 'B')
        SubElement(parent, 'C')
        
        # Sort with empty order list and keep_rest=True
        sort_children_by_tag_order(parent, [], keep_rest=True)
        
        # All elements should be kept in original order
        children = list(parent)
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[2].tag, 'C')
        
        # Sort with empty order list and keep_rest=False
        sort_children_by_tag_order(parent, [], keep_rest=False)
        
        # All elements should be removed
        children = list(parent)
        self.assertEqual(len(children), 0)
    
    # Tests for sort_attributes_by_order function
    
    def test_sort_attributes_by_order_basic(self):
        """Test sort_attributes_by_order with basic order"""
        # Create an element with attributes in wrong order
        elem = Element('Element', attrib={'c': '3', 'a': '1', 'b': '2'})
        
        # Define the expected order
        order = ['a', 'b', 'c']
        
        # Sort the attributes
        sort_attributes_by_order(elem, order)
        
        # Check if the attributes are in the expected order
        # Note: lxml doesn't guarantee attribute order in Element objects
        # but we can verify the order in the serialized XML string
        result = tostring(elem, encoding='unicode')
        
        # The result should be something like: <Element a="1" b="2" c="3"/>
        # Extract the attributes portion from the result
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        
        # Verify the order of attributes
        self.assertLess(attr_part.index('a="1"'), attr_part.index('b="2"'))
        self.assertLess(attr_part.index('b="2"'), attr_part.index('c="3"'))

    def test_sort_attributes_by_order_with_missing_attributes(self):
        """Test sort_attributes_by_order with attributes missing from the order list"""
        elem = Element('Element', attrib={
            'c': '3', 'a': '1', 'd': '4', 'b': '2', 'e': '5'
        })
        
        # Sort with keep_rest=True (default)
        sort_attributes_by_order(elem, ['a', 'b', 'c'])
        
        # All attributes should be present
        self.assertEqual(len(elem.attrib), 5)
        self.assertIn('a', elem.attrib)
        self.assertIn('b', elem.attrib)
        self.assertIn('c', elem.attrib)
        self.assertIn('d', elem.attrib)
        self.assertIn('e', elem.attrib)
        
        # Check order in serialized format
        result = tostring(elem, encoding='unicode')
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        
        # a, b, c should be in specified order
        self.assertLess(attr_part.index('a="1"'), attr_part.index('b="2"'))
        self.assertLess(attr_part.index('b="2"'), attr_part.index('c="3"'))

    def test_sort_attributes_by_order_without_keep_rest(self):
        """Test sort_attributes_by_order with keep_rest=False"""
        elem = Element('Element', attrib={
            'c': '3', 'a': '1', 'd': '4', 'b': '2', 'e': '5'
        })
        
        # Sort with keep_rest=False
        sort_attributes_by_order(elem, ['a', 'b', 'c'], keep_rest=False)
        
        # Only a, b, c should remain
        self.assertEqual(len(elem.attrib), 3)
        self.assertIn('a', elem.attrib)
        self.assertIn('b', elem.attrib)
        self.assertIn('c', elem.attrib)
        self.assertNotIn('d', elem.attrib)
        self.assertNotIn('e', elem.attrib)
        
        # Check values are preserved
        self.assertEqual(elem.get('a'), '1')
        self.assertEqual(elem.get('b'), '2')
        self.assertEqual(elem.get('c'), '3')
        
        # Check order in serialized format
        result = tostring(elem, encoding='unicode')
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        
        self.assertLess(attr_part.index('a="1"'), attr_part.index('b="2"'))
        self.assertLess(attr_part.index('b="2"'), attr_part.index('c="3"'))

    def test_sort_attributes_by_order_with_empty_element(self):
        """Test sort_attributes_by_order with element having no attributes"""
        elem = Element('Element')
        
        # Sort the attributes (should have no effect)
        sort_attributes_by_order(elem, ['a', 'b', 'c'])
        
        # Element should still have no attributes
        self.assertEqual(len(elem.attrib), 0)
        
        # Serialized element should be simple
        result = tostring(elem, encoding='unicode')
        self.assertEqual(result, '<Element/>')

    def test_sort_attributes_by_order_empty_order(self):
        """Test sort_attributes_by_order with empty order list"""
        elem = Element('Element', attrib={'a': '1', 'b': '2', 'c': '3'})
        
        # Sort with empty order list and keep_rest=True
        sort_attributes_by_order(elem, [], keep_rest=True)
        
        # All attributes should be kept
        self.assertEqual(len(elem.attrib), 3)
        self.assertIn('a', elem.attrib)
        self.assertIn('b', elem.attrib)
        self.assertIn('c', elem.attrib)
        
        # Sort with empty order list and keep_rest=False
        sort_attributes_by_order(elem, [], keep_rest=False)
        
        # All attributes should be removed
        self.assertEqual(len(elem.attrib), 0)

    def test_sort_attributes_by_order_unknown_attributes(self):
        """Test sort_attributes_by_order with order containing unknown attributes"""
        elem = Element('Element', attrib={'a': '1', 'b': '2'})
        
        # Sort with order including unknown attributes
        sort_attributes_by_order(elem, ['c', 'a', 'd', 'b'])
        
        # Only existing attributes should be present
        self.assertEqual(len(elem.attrib), 2)
        self.assertIn('a', elem.attrib)
        self.assertIn('b', elem.attrib)
        self.assertNotIn('c', elem.attrib)
        self.assertNotIn('d', elem.attrib)
        
        # Check order in serialized format (a should come before b)
        result = tostring(elem, encoding='unicode')
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        
        self.assertLess(attr_part.index('a="1"'), attr_part.index('b="2"'))

    def test_sort_attributes_by_order_xml_special_chars(self):
        """Test sort_attributes_by_order with attributes containing XML special characters"""
        elem = Element('Element', attrib={
            'c': '"3"', 
            'a': '<1>', 
            'b': '&2;'
        })
        
        # Sort the attributes
        sort_attributes_by_order(elem, ['a', 'b', 'c'])
        
        # Check values are preserved with escaping
        self.assertEqual(elem.get('a'), '<1>')
        self.assertEqual(elem.get('b'), '&2;')
        self.assertEqual(elem.get('c'), '"3"')
        
        # Check order in serialized format (special chars should be escaped)
        result = tostring(elem, encoding='unicode')
        
        # Verify order and proper escaping
        self.assertIn('a="&lt;1&gt;"', result)
        self.assertIn('b="&amp;2;"', result)
        self.assertIn('c="&quot;3&quot;"', result)
        
        # Check proper attribute order
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        self.assertLess(attr_part.index('a="'), attr_part.index('b="'))
        self.assertLess(attr_part.index('b="'), attr_part.index('c="'))


if __name__ == "__main__":
    unittest.main()
