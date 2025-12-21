# Copyright (c) 2025 Eduardo Antonio Ferrera Rodríguez
# SPDX-License-Identifier: MIT
# pyfrontkit/void_element.py

from .block import Block  # Registro global

# =============================================================
# VALID ATTRIBUTE CONSTANTS FOR VOID ELEMENTS
# =============================================================

BASE_VOID_ATTRS = {"id",  "class", "style", "title", "data-", "aria-"}

VOID_TAG_SPECIFIC_ATTRS = {
    "img": BASE_VOID_ATTRS | {"src", "alt", "width", "height", "loading", "srcset", "sizes","class_"},
    "input": BASE_VOID_ATTRS | {"type", "name", "value", "placeholder", "checked", "disabled", "readonly", "size", "maxlength", "min", "max", "step"},
    "link": BASE_VOID_ATTRS | {"href", "rel", "type", "media", "crossorigin"},
    "meta": BASE_VOID_ATTRS | {"name", "content", "charset", "http-equiv"},
    "br": set(),
    "hr": BASE_VOID_ATTRS,
    "area": BASE_VOID_ATTRS | {"alt", "coords", "href", "shape", "target"},
    "base": BASE_VOID_ATTRS | {"href", "target"},
    "col": BASE_VOID_ATTRS | {"span"},
    "source": BASE_VOID_ATTRS | {"src", "type", "srcset"},
    "embed": BASE_VOID_ATTRS | {"src", "type", "width", "height"},
    "param": BASE_VOID_ATTRS | {"name", "value"},
    "track": BASE_VOID_ATTRS | {"kind", "src", "srclang", "label", "default"},
    "wbr": set(),
}

# =============================================================
# VOID ELEMENT BASE
# =============================================================

class VoidElement:
    def __init__(self, tag: str, **attrs):
        self.tag = tag
        self.attrs = self._validate_attributes(tag, attrs)
        self._parent = None
        Block._registry.append(self)

    def _validate_attributes(self, tag: str, kwargs: dict) -> dict:
        allowed_attrs = VOID_TAG_SPECIFIC_ATTRS.get(tag, BASE_VOID_ATTRS)
        validated_attrs = {}

        for key, value in kwargs.items():
            normalized_key = "class" if key == "class_" else key

            
            if normalized_key.startswith("data-") or normalized_key.startswith("aria-"):
                pass
            
            elif normalized_key not in allowed_attrs :
                print(f"⚠️ Warning: '{key}' is not valid for <{tag}>. Allowed: {allowed_attrs}")
                continue

            if value is True:
                validated_attrs[normalized_key] = None
            elif value not in (None, False):
                validated_attrs[normalized_key] = value

        return validated_attrs

    def render(self, indent: int = 0) -> str:
        space = " " * indent
        attr_text = "".join(
            f' {k}' if v is None else f' {k}="{v}"'
            for k, v in self.attrs.items()
        )
        return f"{space}<{self.tag}{attr_text} />\n"

    def add_child(self, *children):
        raise RuntimeError(f"The <{self.tag}> element is a void element and cannot contain children.")

    def __str__(self):
        return self.render(0)

# =============================================================
# ELEMENTOS CONCRETOS
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
# ALIAS PARA LLAMADAS SIMPLES
# =============================================================

img = Img
Input_ = Input
hr = Hr
link = Link
source = Source
embed = Embed
param = Param
track = Track
wbr = Wbr
area = Area
base = Base
col = Col
