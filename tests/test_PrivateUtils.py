#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from unittest import TestCase, main
from lxml.etree import Element, SubElement, tostring
from DipTraceGenerator.PrivateUtils import sort_children_by_tag_order, sort_attributes_by_order


class TestPrivateUtils(TestCase):

    def test_module_import(self):
        """Test that PrivateUtils.py can be imported"""
        import DipTraceGenerator.PrivateUtils as private_utils_module
        
        # The module should be importable and have the required functions
        self.assertTrue(hasattr(private_utils_module, 'sort_children_by_tag_order'))
        self.assertTrue(hasattr(private_utils_module, 'sort_attributes_by_order'))

    # Tests for sort_children_by_tag_order
  
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
        # Create a parent element with children having attributes
        parent = Element('Parent')
        c = SubElement(parent, 'C', attrib={'value': '3'})
        a = SubElement(parent, 'A', attrib={'value': '1'})
        b = SubElement(parent, 'B', attrib={'value': '2'})
        
        # Sort the children
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Check if the children are in the expected order with preserved attributes
        children = list(parent)
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[0].get('value'), '1')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[1].get('value'), '2')
        self.assertEqual(children[2].tag, 'C')
        self.assertEqual(children[2].get('value'), '3')

    def test_sort_children_by_tag_order_with_nested_elements(self):
        """Test sort_children_by_tag_order with nested elements"""
        # Create a parent element with nested children
        parent = Element('Parent')
        c = SubElement(parent, 'C')
        SubElement(c, 'C1')
        SubElement(c, 'C2')
        a = SubElement(parent, 'A')
        SubElement(a, 'A1')
        b = SubElement(parent, 'B')
        SubElement(b, 'B1')
        
        # Sort the children
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Check if the children are in the expected order with preserved nested elements
        children = list(parent)
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(list(children[0])[0].tag, 'A1')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(list(children[1])[0].tag, 'B1')
        self.assertEqual(children[2].tag, 'C')
        self.assertEqual(list(children[2])[0].tag, 'C1')
        self.assertEqual(list(children[2])[1].tag, 'C2')

    def test_sort_children_by_tag_order_with_missing_tags(self):
        """Test sort_children_by_tag_order with tags missing from order"""
        # Create a parent element with children
        parent = Element('Parent')
        SubElement(parent, 'C')
        SubElement(parent, 'A')
        SubElement(parent, 'B')
        SubElement(parent, 'D')  # Not in order list
        
        # Sort the children, with keep_rest=True (default)
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Check if the children are in the expected order, with D at the end
        children = list(parent)
        self.assertEqual(len(children), 4)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[2].tag, 'C')
        self.assertEqual(children[3].tag, 'D')  # D is preserved at the end

    def test_sort_children_by_tag_order_without_keep_rest(self):
        """Test sort_children_by_tag_order with keep_rest=False"""
        # Create a parent element with children
        parent = Element('Parent')
        SubElement(parent, 'C')
        SubElement(parent, 'A')
        SubElement(parent, 'B')
        SubElement(parent, 'D')  # Not in order list
        
        # Sort the children, with keep_rest=False
        sort_children_by_tag_order(parent, ['A', 'B', 'C'], keep_rest=False)
        
        # Check if the children are in the expected order, with D removed
        children = list(parent)
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[1].tag, 'B')
        self.assertEqual(children[2].tag, 'C')

    def test_sort_children_by_tag_order_with_duplicate_tags(self):
        """Test sort_children_by_tag_order with duplicate tags"""
        # Create a parent element with duplicate children tags
        parent = Element('Parent')
        SubElement(parent, 'A')
        SubElement(parent, 'B')
        SubElement(parent, 'A')  # Duplicate A
        
        # Sort the children
        sort_children_by_tag_order(parent, ['A', 'B'])
        
        # Check if the children are in the expected order, with both A elements at the beginning
        children = list(parent)
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].tag, 'A')
        self.assertEqual(children[1].tag, 'A')
        self.assertEqual(children[2].tag, 'B')

    def test_sort_children_by_tag_order_empty_parent(self):
        """Test sort_children_by_tag_order with an empty parent element"""
        # Create an empty parent element
        parent = Element('Parent')
        
        # Sort the children (shouldn't raise exceptions)
        sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        
        # Check if the parent is still empty
        children = list(parent)
        self.assertEqual(len(children), 0)

    def test_sort_children_by_tag_order_empty_order(self):
        """Test sort_children_by_tag_order with an empty order list"""
        # Create a parent element with children
        parent = Element('Parent')
        SubElement(parent, 'C')
        SubElement(parent, 'A')
        SubElement(parent, 'B')
        
        # Make a copy of the children list before sorting
        original_children = [(child.tag, dict(child.attrib)) for child in parent]
        
        # Sort with empty order list
        sort_children_by_tag_order(parent, [])
        
        # Check if the children are unchanged
        children = list(parent)
        self.assertEqual(len(children), 3)
        
        # Verify that children are in the same order as before
        for i, child in enumerate(children):
            self.assertEqual(child.tag, original_children[i][0])
            self.assertEqual(dict(child.attrib), original_children[i][1])

    # Tests for sort_attributes_by_order
    
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
        """Test sort_attributes_by_order with missing attributes"""
        # Create an element with attributes
        elem = Element('Element', attrib={'a': '1', 'c': '3', 'd': '4'})  # 'b' is missing
        
        # Sort the attributes
        sort_attributes_by_order(elem, ['a', 'b', 'c'])  # 'd' not in order
        
        # Check the serialized XML to verify order
        result = tostring(elem, encoding='unicode')
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        
        # 'a' should come before 'c'
        self.assertLess(attr_part.index('a="1"'), attr_part.index('c="3"'))
        
        # 'd' should come after 'c' since it's not in the order list but keep_rest=True
        self.assertLess(attr_part.index('c="3"'), attr_part.index('d="4"'))

    def test_sort_attributes_by_order_without_keep_rest(self):
        """Test sort_attributes_by_order with keep_rest=False"""
        # Create an element with attributes
        elem = Element('Element', attrib={'a': '1', 'b': '2', 'c': '3', 'd': '4'})
        
        # Sort the attributes with keep_rest=False
        sort_attributes_by_order(elem, ['a', 'c'], keep_rest=False)
        
        # Verify that only the specified attributes are retained
        self.assertEqual(len(elem.attrib), 2)
        self.assertEqual(elem.get('a'), '1')
        self.assertEqual(elem.get('c'), '3')
        self.assertIsNone(elem.get('b'))
        self.assertIsNone(elem.get('d'))
        
        # Check the serialized XML to verify order
        result = tostring(elem, encoding='unicode')
        
        # Result should have only 'a' and 'c' attributes
        self.assertIn('a="1"', result)
        self.assertIn('c="3"', result)
        self.assertNotIn('b="2"', result)
        self.assertNotIn('d="4"', result)
        
        # Verify order
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        self.assertLess(attr_part.index('a="1"'), attr_part.index('c="3"'))

    def test_sort_attributes_by_order_with_empty_element(self):
        """Test sort_attributes_by_order with an element that has no attributes"""
        # Create an element with no attributes
        elem = Element('Element')
        
        # Sort the attributes (shouldn't raise exceptions)
        sort_attributes_by_order(elem, ['a', 'b', 'c'])
        
        # Verify the element still has no attributes
        self.assertEqual(len(elem.attrib), 0)
        
        # Check that the serialized XML doesn't have attributes
        result = tostring(elem, encoding='unicode')
        self.assertEqual(result, '<Element/>')

    def test_sort_attributes_by_order_empty_order(self):
        """Test sort_attributes_by_order with an empty order list"""
        # Create an element with attributes
        elem = Element('Element', attrib={'a': '1', 'b': '2', 'c': '3'})
        
        # Copy original attributes for comparison
        original_attrib = dict(elem.attrib)
        
        # Sort with empty order list
        sort_attributes_by_order(elem, [])
        
        # Check that attributes are unchanged
        self.assertEqual(len(elem.attrib), 3)
        self.assertEqual(elem.get('a'), '1')
        self.assertEqual(elem.get('b'), '2')
        self.assertEqual(elem.get('c'), '3')
        
        # The attribute dict should be the same as the original
        self.assertEqual(dict(elem.attrib), original_attrib)

    def test_sort_attributes_by_order_unknown_attributes(self):
        """Test sort_attributes_by_order with attributes not in element"""
        # Create an element with attributes
        elem = Element('Element', attrib={'a': '1', 'c': '3'})
        
        # Sort with order list containing unknown attributes
        sort_attributes_by_order(elem, ['a', 'b', 'd', 'c'])
        
        # Check that existing attributes are in the expected order
        result = tostring(elem, encoding='unicode')
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        
        # 'a' should come before 'c' as per order list
        self.assertLess(attr_part.index('a="1"'), attr_part.index('c="3"'))
        
        # Element should not have the unknown attributes
        self.assertNotIn('b', elem.attrib)
        self.assertNotIn('d', elem.attrib)

    def test_sort_attributes_by_order_xml_special_chars(self):
        """Test sort_attributes_by_order with XML special characters"""
        # Create an element with attributes containing special XML characters
        elem = Element('Element', attrib={
            'c': '3 & special',
            'a': '1 < less',
            'b': '2 > greater'
        })
        
        # Sort the attributes
        sort_attributes_by_order(elem, ['a', 'b', 'c'])
        
        # Check that attributes with special chars are correctly preserved and ordered
        self.assertEqual(elem.get('a'), '1 < less')
        self.assertEqual(elem.get('b'), '2 > greater')
        self.assertEqual(elem.get('c'), '3 & special')
        
        # Check serialized output for order verification
        result = tostring(elem, encoding='unicode')
        
        # Special characters should be escaped in the output
        self.assertIn('a="1 &lt; less"', result)
        self.assertIn('b="2 &gt; greater"', result)
        self.assertIn('c="3 &amp; special"', result)
        
        # Verify order using the escaped attribute strings
        attr_part = result.split('<Element ')[1].split('/>')[0].strip()
        self.assertLess(attr_part.index('a="1 &lt; less"'), attr_part.index('b="2 &gt; greater"'))
        self.assertLess(attr_part.index('b="2 &gt; greater"'), attr_part.index('c="3 &amp; special"'))

    # Test that PrivateUtils can be imported and has proper main block

    def test_module_main_block(self):
        """Test that Utils.py can be imported and has proper main block"""
        import DipTraceGenerator.PrivateUtils as utils_module
        # The module should be importable and have the main guard
        self.assertTrue(hasattr(utils_module, 'sort_children_by_tag_order'))
        self.assertTrue(hasattr(utils_module, 'sort_attributes_by_order'))

if __name__ == "__main__":
    main()