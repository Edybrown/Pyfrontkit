# pyfront/void_element.py

# Copyright (C) [2025] Eduardo Antonio Ferrera Rodríguez
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; see the COPYING file for more details.

class VoidElement:
    """
    Base class for void/self-closing HTML elements.
    Acts as a "printer": generates <tag attr1="..." attr2="..." />.
    """

    def __init__(self, tag: str, **attrs):
        self.tag = tag
        self.attrs = {}
        for key, value in attrs.items():
            # Normalize class_ to class
            if key == "class_":
                key = "class"
            if value is True:
                self.attrs[key] = None
            elif value not in (None, False):
                self.attrs[key] = value

    def render(self, indent: int = 0) -> str:
        space = " " * indent
        attr_text = ""
        for key, value in self.attrs.items():
            if value is None:
                attr_text += f" {key}"
            else:
                attr_text += f' {key}="{value}"'
        return f"{space}<{self.tag}{attr_text} />\n"


# =============================================================
# Concrete void elements
# =============================================================

class Img(VoidElement):
    def __init__(self, **attrs):
        super().__init__("img", **attrs)

class Input(VoidElement):
    def __init__(self, **attrs):
        super().__init__("input", **attrs)

class Hr(VoidElement):
    def __init__(self, **attrs):
        super().__init__("hr", **attrs)

class Meta(VoidElement):
    def __init__(self, **attrs):
        super().__init__("meta", **attrs)

class Link(VoidElement):
    def __init__(self, **attrs):
        super().__init__("link", **attrs)

class Source(VoidElement):
    def __init__(self, **attrs):
        super().__init__("source", **attrs)

class Embed(VoidElement):
    def __init__(self, **attrs):
        super().__init__("embed", **attrs)

class Param(VoidElement):
    def __init__(self, **attrs):
        super().__init__("param", **attrs)

class Track(VoidElement):
    def __init__(self, **attrs):
        super().__init__("track", **attrs)

class Wbr(VoidElement):
    def __init__(self, **attrs):
        super().__init__("wbr", **attrs)

class Area(VoidElement):
    def __init__(self, **attrs):
        super().__init__("area", **attrs)

class Base(VoidElement):
    def __init__(self, **attrs):
        super().__init__("base", **attrs)

class Col(VoidElement):
    def __init__(self, **attrs):
        super().__init__("col", **attrs)


# =============================================================
# Aliases for simple lowercase calls
# =============================================================

img = Img
input = Input
hr = Hr
meta = Meta
link = Link
source = Source
embed = Embed
param = Param
track = Track
wbr = Wbr
area = Area
base = Base
col = Col
