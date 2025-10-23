#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from unittest import TestCase, main
from pathlib import Path
from unittest.mock import patch
from DipTraceGenerator import format_xml, get_correct_filename, load_from_xml_file, compare
from DipTraceGenerator.ComponentLibrary import ComponentLibrary
from DipTraceGenerator.PatternLibrary import PatternLibrary


class Test(TestCase):

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
        lib_file = path.joinpath("samples/test_component.libxml")
        
        # This file is a ComponentLibrary
        result = load_from_xml_file(lib_file)
        self.assertIsInstance(result, ComponentLibrary)

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

    def test_compare_two_files(self):
        """Test compare function with two files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        
        # Mock the necessary functions
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
                with patch('DipTraceGenerator.Utils.Popen') as mock_popen:
                    compare(file1, file2)
                    mock_popen.assert_called_once()

    def test_compare_three_files(self):
        """Test compare function with three files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        file3 = path.joinpath("samples/test_load.libxml")
        
        # Mock the necessary functions
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
                with patch('DipTraceGenerator.Utils.Popen') as mock_popen:
                    compare(file1, file2, file3)
                    mock_popen.assert_called_once()

    def test_compare_too_few_files(self):
        """Test compare raises error with too few files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
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
        
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
                with self.assertRaises(ValueError) as cm:
                    compare(file1, file2, file3, file4)
                self.assertIn("Too many files", str(cm.exception))

    def test_compare_invalid_xpath_count(self):
        """Test compare raises error with invalid xpath count"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        file3 = path.joinpath("samples/test_load.libxml")
        
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
                with self.assertRaises(ValueError) as cm:
                    compare(file1, file2, file3, "./Parts", "./Components")
                self.assertIn("Number of xpath", str(cm.exception))

    def test_compare_with_single_xpath(self):
        """Test compare function with single xpath for all files"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/test_load.libxml")
        file2 = path.joinpath("samples/test_categories.libxml")
        
        # Mock to avoid GitHub Actions skip and WinMerge launch
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
                with patch('DipTraceGenerator.Utils.Popen') as mock_popen:
                    # Mock the process wait method
                    mock_popen.return_value.wait.return_value = None
                    
                    # Use a valid XPath that exists in both files
                    compare(file1, file2, "./PadStyles")
                    mock_popen.assert_called_once()
                    # Verify wait was called on the process
                    mock_popen.return_value.wait.assert_called_once()

    def test_compare_with_multiple_xpaths(self):
        """Test compare function with different xpath for each file"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/test_load.libxml")
        file2 = path.joinpath("samples/test_categories.libxml")
        
        # Mock to avoid GitHub Actions skip and WinMerge launch
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
                with patch('DipTraceGenerator.Utils.Popen') as mock_popen:
                    # Mock the process wait method
                    mock_popen.return_value.wait.return_value = None
                    
                    # Use valid xpaths for each file
                    compare(file1, file2, "./Patterns", "./Categories")
                    mock_popen.assert_called_once()
                    # Verify wait was called on the process
                    mock_popen.return_value.wait.assert_called_once()

    def test_compare_skips_in_github_actions(self):
        """Test that compare skips execution in GitHub Actions"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        
        # Mock GitHub Actions environment
        with patch('DipTraceGenerator.Utils.getenv', return_value='true'):
            with patch('DipTraceGenerator.Utils.Popen') as mock_popen:
                compare(file1, file2)
                # Popen should not be called when in GitHub Actions
                mock_popen.assert_not_called()

    def test_compare_skips_when_winmerge_not_found(self):
        """Test that compare skips when WinMerge is not found"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        
        # Mock WinMerge not found
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value=None):
                with patch('DipTraceGenerator.Utils.Path.exists', return_value=False):
                    with patch('DipTraceGenerator.Utils.Popen') as mock_popen:
                        compare(file1, file2)
                        # Popen should not be called when WinMerge not found
                        mock_popen.assert_not_called()

    def test_compare_uses_default_winmerge_path(self):
        """Test that compare uses default WinMerge path when which returns None"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/part_test.sample.xml")
        file2 = path.joinpath("samples/format_test.sample.xml")
        
        # Mock which returning None, but default path exists
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value=None):
                with patch('DipTraceGenerator.Utils.Path.exists', return_value=True):
                    with patch('DipTraceGenerator.Utils.Popen') as mock_popen:
                        compare(file1, file2)
                        # Popen should be called with default path
                        mock_popen.assert_called_once()

    def test_compare_xpath_not_found(self):
        """Test that compare raises error when XPath is not found"""
        path = Path(__file__).parent
        file1 = path.joinpath("samples/test_load.libxml")
        file2 = path.joinpath("samples/test_categories.libxml")
        
        # Use an invalid XPath that doesn't exist
        with patch('DipTraceGenerator.Utils.getenv', return_value=None):
            with patch('DipTraceGenerator.Utils.which', return_value='winmerge'):
                with self.assertRaises(ValueError) as cm:
                    compare(file1, file2, "./NonExistentElement")
                self.assertIn("XPath", str(cm.exception))
                self.assertIn("not found", str(cm.exception))

    def test_load_from_xml_file_invalid_library_type(self):
        """Test load_from_xml_file with invalid library type"""
        path = Path(__file__).parent
        # Create a temporary XML file with invalid Type attribute
        test_file = path.joinpath("samples/part_test.sample.xml")
        
        # This file doesn't have Type="DipTrace-PatternLibrary" or "DipTrace-ComponentLibrary"
        result = load_from_xml_file(test_file)
        # Should return None for invalid types
        self.assertIsNone(result)

    # Test that PrivateUtils can be imported and has proper main block

    def test_module_main_block(self):
        """Test that Utils.py can be imported and has proper main block"""
        import DipTraceGenerator.Utils as utils_module
        # The module should be importable and have the main guard
        self.assertTrue(hasattr(utils_module, 'load_from_xml_file'))
        self.assertTrue(hasattr(utils_module, 'format_xml'))
        self.assertTrue(hasattr(utils_module, 'compare'))
        self.assertTrue(hasattr(utils_module, 'get_correct_filename'))


if __name__ == "__main__":
    main()
