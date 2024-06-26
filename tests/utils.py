#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from lxml.etree import Element, fromstring


def xml(text: str) -> Element:
    return fromstring(text)


if __name__ == "__main__":
    pass
