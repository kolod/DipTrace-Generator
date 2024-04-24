#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <oleksandr.kolodkin@ukr.net>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from lxml.etree import Element, SubElement, tostring
from typing import Optional, List
from dataclasses import dataclass, field
from copy import deepcopy
from DipTraceGenerator.Enums import Units, Side, MountType, Boolean, Layer


@dataclass
class Order(object):
    tags: List[str] = field(default_factory=lambda: [])
    args: List[str] = field(default_factory=lambda: [])
    subs: List[str] = field(default_factory=lambda: [])


class RootMixin(object):
    _root: Element
    _order: Order = field(default_factory=lambda: Order())

    def __init__(self, root: Optional[Element] = None, *args, **kwargs):
        if root is None:
            root = Element(self.__class__.__name__)
        self._root = root

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def root(self) -> Element:
        return self._root

    def __str__(self) -> str:
        # Remove the unneeded whitespaces
        for element in self._root.iter():
            if not isinstance(element.text, type(None)):
                element.text = element.text.strip()
                if element.text == "":
                    element.text = "\n"

        return tostring(self._root, xml_declaration=False, pretty_print=True, encoding="utf-8").decode("utf-8")

    def sort(self) -> None:
        if hasattr(self, "_order") and isinstance(self._order, Order):
            temp = {}
            for key in self._order.args:
                if key in self._root.attrib:
                    temp[key] = self._root.attrib.pop(key)
            for key, value in temp.items():
                self._root.set(key, value)

            temp = {}
            for key in self._order.tags:
                temp[key] = deepcopy(self._root.find(f"./{key}"))
                for tag in self._root.findall(f"./{key}"):
                    self._root.remove(tag)

            for key, value in temp.items():
                if value is not None:
                    self._root.append(value)

            for key in self._order.subs:
                if hasattr(self, key):
                    obj = getattr(self, key)

                    if hasattr(obj, "reorder"):
                        if callable(obj.sort):
                            obj.sort()

                    elif hasattr(obj, "__iter__"):
                        for o in obj:
                            if callable(o.sort):
                                o.sort()


class NameMixin(RootMixin):
    @property
    def name(self) -> Optional[str]:
        return self._root.get("Name")

    @name.setter
    def name(self, value: Optional[str] = None) -> None:
        if value is not None:
            self._root.set("Name", value)
        elif "Name" in self._root.attrib:
            self._root.attrib.pop("Name")


class RefDesMixin(RootMixin):
    @property
    def ref_des(self) -> Optional[str]:
        return self._root.get("RefDes")

    @ref_des.setter
    def ref_des(self, value: Optional[str] = None) -> None:
        if value is not None:
            self._root.set("RefDes", value)
        elif "RefDes" in self._root.attrib:
            self._root.attrib.pop("RefDes")


class NameTagMixin(RootMixin):
    @property
    def name(self) -> Optional[str]:
        if (tag := self._root.find("Name")) is not None:
            return tag.text
        return None

    @name.setter
    def name(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./Name"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Name")
            tag.text = value


class NameDescriptionTagMixin(RootMixin):
    @property
    def name_description(self) -> Optional[str]:
        if (tag := self._root.find("Name_Description")) is not None:
            return tag.text
        return None

    @name_description.setter
    def name_description(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./Name_Description"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Name_Description")
            tag.text = value


class NameUniqueTagMixin(RootMixin):
    @property
    def name_unique(self) -> Optional[str]:
        if (tag := self._root.find("Name_Unique")) is not None:
            return tag.text
        return None

    @name_unique.setter
    def name_unique(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./Name_Unique"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Name_Unique")
            tag.text = value


class ValueTagMixin(RootMixin):
    @property
    def value(self) -> Optional[str]:
        if (tag := self._root.find("Value")) is not None:
            return tag.text
        return None

    @value.setter
    def value(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./Value"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Value")
            tag.text = value


class ManufacturerTagMixin(RootMixin):
    @property
    def manufacturer(self) -> Optional[str]:
        if (tag := self._root.find("Manufacturer")) is not None:
            return tag.text
        return None

    @manufacturer.setter
    def manufacturer(self, value: Optional[str] = None) -> None:
        if value is not None:
            tag = SubElement(self._root, "Manufacturer")
            tag.text = value
        else:
            self._root.remove(self._root.find("Manufacturer"))


class DatasheetTagMixin(RootMixin):
    @property
    def datasheet(self) -> Optional[str]:
        if (tag := self._root.find("Datasheet")) is not None:
            return tag.text
        return None

    @datasheet.setter
    def datasheet(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./Datasheet"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Datasheet")
            tag.text = value


class NumberMixin(RootMixin):
    @property
    def number(self) -> Optional[int]:
        try:
            return int(self._root.get("Number"))
        except (ValueError, TypeError, AttributeError):
            return None

    @number.setter
    def number(self, value: Optional[int] = None) -> None:
        if value is not None:
            self._root.set("Number", str(value))
        elif "Number" in self._root.attrib:
            self._root.attrib.pop("Number")


class NumberTagMixin(RootMixin):
    @property
    def number(self) -> Optional[str]:
        if (tag := self._root.find("Number")) is not None:
            return tag.text
        return None

    @number.setter
    def number(self, value: Optional[str] = None) -> None:
        for tag in self._root.findall("./Number"):
            self._root.remove(tag)
        if value is not None:
            tag = SubElement(self._root, "Number")
            tag.text = value


class IdMixin(RootMixin):
    @property
    def id(self) -> Optional[int]:
        try:
            return int(self._root.get("Id"))
        except (ValueError, TypeError):
            return None

    @id.setter
    def id(self, value: Optional[int] = None) -> None:
        if value is not None:
            self._root.set("Id", str(value))
        elif "Id" in self._root.attrib:
            self._root.attrib.pop("Id")


class GroupMixin(RootMixin):
    @property
    def group(self) -> Optional[int]:
        try:
            return int(self._root.get("Group"))
        except (AttributeError, ValueError, TypeError):
            return None

    @group.setter
    def group(self, value: Optional[int]) -> None:
        if value is not None:
            self._root.set("Group", str(value))
        elif "Group" in self._root.attrib:
            self._root.attrib.pop("Group")


class HintMixin(RootMixin):
    @property
    def hint(self) -> Optional[str]:
        return self._root.get("Hint")

    @hint.setter
    def hint(self, value: Optional[str] = None) -> None:
        if value is not None:
            self._root.set("Hint", value)
        elif "Hint" in self._root.attrib:
            self._root.attrib.pop("Hint")


class LockedMixin(RootMixin):
    @property
    def locked(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("Locked"))
        except (ValueError, TypeError):
            return None

    @locked.setter
    def locked(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("Locked", value.value)
        elif "Locked" in self._root.attrib:
            self._root.attrib.pop("Locked")


class AllLayersMixin(RootMixin):
    @property
    def all_layers(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("AllLayers"))
        except (ValueError, TypeError):
            return None

    @all_layers.setter
    def all_layers(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("AllLayers", value.value)
        elif "AllLayers" in self._root.attrib:
            self._root.attrib.pop("AllLayers")


class FontVectorMixin(RootMixin):
    @property
    def font_vector(self) -> Optional[Boolean]:
        try:
            return Boolean(self._root.get("FontVector"))
        except (ValueError, TypeError):
            return None

    @font_vector.setter
    def font_vector(self, value: Optional[Boolean]) -> None:
        if value is not None:
            self._root.set("FontVector", value.value)
        elif "FontVector" in self._root.attrib:
            self._root.attrib.pop("FontVector")


class StyleMixin(RootMixin):
    @property
    def style(self) -> Optional[str]:
        return self._root.get("Style")

    @style.setter
    def style(self, value: Optional[str]) -> None:
        if value is not None:
            self._root.set("Style", value)
        elif "Style" in self._root.attrib:
            self._root.attrib.pop("Style")


class VersionMixin(RootMixin):
    @property
    def version(self) -> Optional[str]:
        return self._root.get("Version")

    @version.setter
    def version(self, value: Optional[str] = None) -> None:
        if value is not None:
            self._root.set("Version", value)
        elif "Version" in self._root.attrib:
            self._root.attrib.pop("Version")


class UnitsMixin(RootMixin):
    @property
    def units(self) -> Optional[Units]:
        try:
            return Units(self._root.get("Units"))
        except (ValueError, TypeError):
            return None

    @units.setter
    def units(self, value: Optional[Units] = None) -> None:
        if value is not None:
            self._root.set("Units", value.value)
        elif "Units" in self._root.attrib:
            self._root.attrib.pop("Units")


class SideMixin(RootMixin):
    @property
    def side(self) -> Optional[Side]:
        try:
            return Side(self._root.get("Side"))
        except (ValueError, TypeError):
            return None

    @side.setter
    def side(self, value: Optional[Side] = None) -> None:
        if value is not None:
            self._root.set("Side", value.value)
        elif "Side" in self._root.attrib:
            self._root.attrib.pop("Side")


class LayerMixin(RootMixin):
    @property
    def layer(self) -> Optional[Layer]:
        try:
            return Layer(self._root.get("Layer"))
        except (ValueError, TypeError):
            return None

    @layer.setter
    def layer(self, value: Optional[Layer] = None) -> None:
        if value is not None:
            self._root.set("Layer", value.value)
        elif "Layer" in self._root.attrib:
            self._root.attrib.pop("Layer")


class PadTypeMixin(RootMixin):
    @property
    def type(self) -> Optional[MountType]:
        try:
            return MountType(self._root.get("Type"))
        except (ValueError, TypeError):
            return None

    @type.setter
    def type(self, value: Optional[MountType]) -> None:
        if value is not None:
            self._root.set("Type", value.value)
        elif "Type" in self._root.attrib:
            self._root.attrib.pop("Type")


class WidthMixin(RootMixin):
    @property
    def width(self) -> Optional[float]:
        try:
            return float(self._root.get("Width"))
        except (ValueError, TypeError):
            return None

    @width.setter
    def width(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Width", f"{value:.5g}")
        elif "Width" in self._root.attrib:
            self._root.attrib.pop("Width")


class HeightMixin(RootMixin):
    @property
    def height(self) -> Optional[float]:
        try:
            return float(self._root.get("Height"))
        except (ValueError, TypeError):
            return None

    @height.setter
    def height(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Height", f"{value:.5g}")
        elif "Height" in self._root.attrib:
            self._root.attrib.pop("Height")


class CornerMixin(RootMixin):
    @property
    def corner(self) -> Optional[float]:
        try:
            return float(self._root.get("Corner"))
        except (ValueError, TypeError):
            return None

    @corner.setter
    def corner(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Corner", f"{value:.6g}")
        elif "Corner" in self._root.attrib:
            self._root.attrib.pop("Corner")


class XMixin(RootMixin):
    @property
    def x(self) -> Optional[float]:
        try:
            return float(self._root.get("X"))
        except (ValueError, TypeError):
            return None

    @x.setter
    def x(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("X", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "X" in self._root.attrib:
            self._root.attrib.pop("X")


class YMixin(RootMixin):
    @property
    def y(self) -> Optional[float]:
        try:
            return float(self._root.get("Y"))
        except (ValueError, TypeError):
            return None

    @y.setter
    def y(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Y", f"{value:.4f}".rstrip("0").rstrip("."))
        elif "Y" in self._root.attrib:
            self._root.attrib.pop("Y")


class DiameterMixin(RootMixin):
    @property
    def diameter(self) -> Optional[float]:
        try:
            return float(self._root.get("Diam"))
        except (ValueError, TypeError):
            return None

    @diameter.setter
    def diameter(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Diam", f"{value:.6g}")
        elif "Diam" in self._root.attrib:
            self._root.attrib.pop("Diam")


class HoleDiameterMixin(RootMixin):
    @property
    def hole_diameter(self) -> Optional[float]:
        try:
            return float(self._root.get("HoleDiam"))
        except (ValueError, TypeError):
            return None

    @hole_diameter.setter
    def hole_diameter(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("HoleDiam", f"{value:.6g}")
        elif "HoleDiam" in self._root.attrib:
            self._root.attrib.pop("HoleDiam")


class ZMixin(RootMixin):
    @property
    def z(self) -> Optional[float]:
        try:
            return float(self._root.get("Z"))
        except (ValueError, TypeError):
            return None

    @z.setter
    def z(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Z", f"{value:.6g}")
        elif "Z" in self._root.attrib:
            self._root.attrib.pop("Z")


class XOffsetMixin(RootMixin):
    @property
    def x_offset(self) -> Optional[float]:
        try:
            return float(self._root.get("XOff"))
        except (ValueError, TypeError):
            return None

    @x_offset.setter
    def x_offset(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("XOff", f"{value:.6g}")
        elif "XOff" in self._root.attrib:
            self._root.attrib.pop("XOff")


class YOffsetMixin(RootMixin):
    @property
    def y_offset(self) -> Optional[float]:
        try:
            return float(self._root.get("YOff"))
        except (ValueError, TypeError):
            return None

    @y_offset.setter
    def y_offset(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("YOff", f"{value:.6g}")
        elif "YOff" in self._root.attrib:
            self._root.attrib.pop("YOff")


class AngleMixin(RootMixin):
    @property
    def angle(self) -> Optional[float]:
        try:
            return float(self._root.get("Angle"))
        except (ValueError, TypeError):
            return None

    @angle.setter
    def angle(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Angle", f"{value:.6g}")
        elif "Angle" in self._root.attrib:
            self._root.attrib.pop("Angle")


class OrientationMixin(RootMixin):
    @property
    def orientation(self) -> Optional[float]:
        try:
            return float(self._root.get("Orientation"))
        except (ValueError, TypeError):
            return None

    @orientation.setter
    def orientation(self, value: Optional[float] = None) -> None:
        if value is not None:
            self._root.set("Orientation", f"{value:.6g}")
        elif "Orientation" in self._root.attrib:
            self._root.attrib.pop("Orientation")


class FontNameMixin(RootMixin):
    @property
    def font_name(self) -> Optional[str]:
        try:
            return self._root.get("FontName")
        except (ValueError, TypeError):
            return None

    @font_name.setter
    def font_name(self, value: Optional[str]) -> None:
        if value is not None:
            self._root.set("Orientation", value)
        elif "FontName" in self._root.attrib:
            self._root.attrib.pop("FontName")


class FontMixin(RootMixin):
    @property
    def font_name(self) -> Optional[str]:
        try:
            return self._root.get("FontName")
        except (ValueError, TypeError):
            return None

    @font_name.setter
    def font_name(self, value: Optional[str]) -> None:
        if value is not None:
            self._root.set("FontName", value)
        elif "FontName" in self._root.attrib:
            self._root.attrib.pop("FontName")

    @property
    def font_size(self) -> Optional[int]:
        try:
            return int(self._root.get("FontSize"))
        except (ValueError, TypeError):
            return None

    @font_size.setter
    def font_size(self, value: Optional[int]) -> None:
        if value is not None:
            self._root.set("FontSize", str(value))
        elif "FontSize" in self._root.attrib:
            self._root.attrib.pop("FontSize")

    @property
    def font_scale(self) -> Optional[float]:
        try:
            return float(self._root.get("FontScale"))
        except (ValueError, TypeError):
            return None

    @font_scale.setter
    def font_scale(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("FontScale", f"{value:.5g}")
        elif "FontScale" in self._root.attrib:
            self._root.attrib.pop("FontScale")

    @property
    def font_width(self) -> Optional[float]:
        try:
            return float(self._root.get("FontWidth"))
        except (ValueError, TypeError):
            return None

    @font_width.setter
    def font_width(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("FontWidth", f"{value:.5g}")
        elif "FontWidth" in self._root.attrib:
            self._root.attrib.pop("FontWidth")


class LineWidthMixin(RootMixin):
    @property
    def line_width(self) -> Optional[float]:
        try:
            return float(self._root.get("LineWidth"))
        except (AttributeError, ValueError, TypeError):
            return None

    @line_width.setter
    def line_width(self, value: Optional[float]) -> None:
        if value is not None:
            self._root.set("LineWidth", f"{value:.5g}")
        elif "LineWidth" in self._root.attrib:
            self._root.attrib.pop("LineWidth")


if __name__ == "__main__":
    pass
