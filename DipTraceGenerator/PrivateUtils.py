#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2021-... Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

"""
Private utility functions for working with XML elements in DipTrace library files.

This module provides helper functions for:
- Sorting XML element attributes
- Sorting XML element children
"""

from typing import List
from lxml.etree import Element


def sort_attributes_by_order(element: Element, order: List[str], keep_rest: bool = True) -> None:
    """
    Sort the attributes of an XML element based on a specified order.
    Any attributes not specified in the order list will be placed at the end
    in their original order.
    
    Args:
        element (Element): The XML element whose attributes are to be sorted
        order (List[str]): A list of attribute names defining the desired order
        keep_rest (bool): If True, attributes not in the order list are kept at the end;
                          if False, they are removed.

    Returns:
        None: The function modifies the element in place
        
    Examples:
        >>> from lxml.etree import Element, tostring
        >>> elem = Element('Element', attrib={'b': '2', 'a': '1', 'c': '3'})
        >>> sort_attributes_by_order(elem, ['a', 'b', 'c'])
        >>> tostring(elem)
        b'<Element a="1" b="2" c="3"/>'
    """
    attrib = element.attrib
    sorted_attrib = {key: attrib[key] for key in order if key in attrib}
    if keep_rest:
        for key in attrib:
            if key not in sorted_attrib:
                sorted_attrib[key] = attrib[key]
    element.attrib.clear()
    element.attrib.update(sorted_attrib)


def sort_children_by_tag_order(element: Element, order: List[str], keep_rest: bool = True) -> None:
    """
    Sort the child elements of an XML element based on a specified tag order.
    
    This function rearranges the child elements of the given XML element
    so that they appear in the order defined by the provided list of tags.
    Any child elements not specified in the order list will be placed at the end
    in their original order.
    
    Args:
        element (Element): The XML element whose children are to be sorted
        order (List[str]): A list of tag names defining the desired order of child elements
        keep_rest (bool): If True, child elements not in the order list are kept at the end;
                          if False, they are removed.

    Returns:
        None: The function modifies the element in place
        
    Examples:
        >>> from lxml.etree import Element, SubElement, tostring
        >>> parent = Element('Parent')
        >>> SubElement(parent, 'B')
        <Element B at 0x...>
        >>> SubElement(parent, 'A')
        <Element A at 0x...>
        >>> SubElement(parent, 'C')
        <Element C at 0x...>
        >>> sort_children_by_tag_order(parent, ['A', 'B', 'C'])
        >>> tostring(parent)
        b'<Parent><A/><B/><C/></Parent>'
    """
    children = list(element)
    element.clear()
    
    tag_to_elements = {tag: [] for tag in order}
    other_elements = []
    
    for child in children:
        if child.tag in tag_to_elements:
            tag_to_elements[child.tag].append(child)
        elif keep_rest:
            other_elements.append(child)
    
    for tag in order:
        for child in tag_to_elements[tag]:
            element.append(child)
    
    for child in other_elements:
        element.append(child)