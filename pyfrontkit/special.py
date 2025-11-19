# 

# Copyright (C) [2025] Eduardo Antonio Ferrera Rodríguez
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; see the COPYING file for more details.

# pyfrontkit/special.py

from .void_element import Source, Track, Img, Param
from .css import CSSRegistry

# ===============================
#      SPECIAL CONTAINERS
# ===============================

class Video:
    ALLOWED_CHILDREN = {"source": Source, "track": Track}

    def __init__(self, *, source=None, track=None, **attrs):
        self.tag = "video"
        self.attrs = attrs
        self.children = []

        # Generate allowed children from attributes
        for key, value in {"source": source, "track": track}.items():
            if value is not None:
                child_class = self.ALLOWED_CHILDREN[key]
                if isinstance(value, str):
                    child = child_class(src=value)
                elif isinstance(value, dict):
                    child = child_class(**value)
                else:
                    raise TypeError(f"Error: '{key}' attribute must be a string or dict")
                self.children.append(child)
                # Register child in CSS if it has class or style
                if getattr(child, "attrs", None) and ("class" in child.attrs or "class_" in child.attrs or "style" in child.attrs):
                    CSSRegistry.register_block(child)

        # Register self in CSS if class/style exists
        if "class" in attrs or "class_" in attrs or "style" in attrs:
            CSSRegistry.register_block(self)

    def render(self, indent=0):
        space = " " * indent
        attr_text = ""
        for k, v in self.attrs.items():
            if v is True:
                attr_text += f" {k}"
            else:
                attr_text += f' {k}="{v}"'
        html = f"{space}<{self.tag}{attr_text}>\n"
        for child in self.children:
            html += child.render(indent + 2)
        html += f"{space}</{self.tag}>\n"
        return html


class Audio:
    ALLOWED_CHILDREN = {"source": Source, "track": Track}

    def __init__(self, *, source=None, track=None, **attrs):
        self.tag = "audio"
        self.attrs = attrs
        self.children = []

        for key, value in {"source": source, "track": track}.items():
            if value is not None:
                child_class = self.ALLOWED_CHILDREN[key]
                if isinstance(value, str):
                    child = child_class(src=value)
                elif isinstance(value, dict):
                    child = child_class(**value)
                else:
                    raise TypeError(f"Error: '{key}' attribute must be a string or dict")
                self.children.append(child)
                if getattr(child, "attrs", None) and ("class" in child.attrs or "class_" in child.attrs or "style" in child.attrs):
                    CSSRegistry.register_block(child)

        if "class" in attrs or "class_" in attrs or "style" in attrs:
            CSSRegistry.register_block(self)

    def render(self, indent=0):
        space = " " * indent
        attr_text = ""
        for k, v in self.attrs.items():
            if v is True:
                attr_text += f" {k}"
            else:
                attr_text += f' {k}="{v}"'
        html = f"{space}<{self.tag}{attr_text}>\n"
        for child in self.children:
            html += child.render(indent + 2)
        html += f"{space}</{self.tag}>\n"
        return html


class Picture:
    ALLOWED_CHILDREN = {"source": Source, "img": Img}

    def __init__(self, *, source=None, img=None, **attrs):
        self.tag = "picture"
        self.attrs = attrs
        self.children = []

        for key, value in {"source": source, "img": img}.items():
            if value is not None:
                child_class = self.ALLOWED_CHILDREN[key]
                if isinstance(value, str):
                    child = child_class(src=value)
                elif isinstance(value, dict):
                    child = child_class(**value)
                else:
                    raise TypeError(f"Error: '{key}' attribute must be a string or dict")
                self.children.append(child)
                if getattr(child, "attrs", None) and ("class" in child.attrs or "class_" in child.attrs or "style" in child.attrs):
                    CSSRegistry.register_block(child)

        if "class" in attrs or "class_" in attrs or "style" in attrs:
            CSSRegistry.register_block(self)

    def render(self, indent=0):
        space = " " * indent
        attr_text = ""
        for k, v in self.attrs.items():
            if v is True:
                attr_text += f" {k}"
            else:
                attr_text += f' {k}="{v}"'
        html = f"{space}<{self.tag}{attr_text}>\n"
        for child in self.children:
            html += child.render(indent + 2)
        html += f"{space}</{self.tag}>\n"
        return html


class ObjectElement:
    ALLOWED_CHILDREN = {"param": Param}

    def __init__(self, *, param=None, **attrs):
        self.tag = "object"
        self.attrs = attrs
        self.children = []

        if param is not None:
            child_class = self.ALLOWED_CHILDREN["param"]
            if isinstance(param, str):
                child = child_class(name="value", value=param)
            elif isinstance(param, dict):
                child = child_class(**param)
            else:
                raise TypeError("Error: 'param' attribute must be a string or dict")
            self.children.append(child)
            if getattr(child, "attrs", None) and ("class" in child.attrs or "class_" in child.attrs or "style" in child.attrs):
                CSSRegistry.register_block(child)

        if "class" in attrs or "class_" in attrs or "style" in attrs:
            CSSRegistry.register_block(self)

    def render(self, indent=0):
        space = " " * indent
        attr_text = ""
        for k, v in self.attrs.items():
            if v is True:
                attr_text += f" {k}"
            else:
                attr_text += f' {k}="{v}"'
        html = f"{space}<{self.tag}{attr_text}>\n"
        for child in self.children:
            html += child.render(indent + 2)
        html += f"{space}</{self.tag}>\n"
        return html

# ===============================
#      FUNCTION ALIASES (lowercase)
# ===============================

def video(*args, **kwargs):
    return Video(*args, **kwargs)

def audio(*args, **kwargs):
    return Audio(*args, **kwargs)

def picture(*args, **kwargs):
    return Picture(*args, **kwargs)

def object(*args, **kwargs):
    return ObjectElement(*args, **kwargs)
