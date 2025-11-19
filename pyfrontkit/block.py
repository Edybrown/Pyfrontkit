
# Copyright (C) [2025] Eduardo Antonio Ferrera Rodríguez
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY. See the COPYING file for more details.


# pyfrontkit/block.py

# pyfrontkit/block.py

from .content import ContentFactory
from .dom import DOM
from .css import CSSRegistry
from typing import Any

# Global whitelist of valid HTML attributes
VALID_HTML_ATTRS = {
    "id", "class", "class_", "style", "title", "alt", "src", "href", "target",
    "type", "name", "value", "disabled", "checked", "readonly", "placeholder",
}

# Optional tag-specific whitelist
TAG_SPECIFIC_ATTRS = {
    "a": {"href", "target", "rel", "title"},
    "img": {"src", "alt", "title"},
    "input": {"type", "name", "value", "placeholder", "checked", "disabled", "readonly"},
    "button": {"type", "name", "value", "disabled"},
}

class Block:
    """
    Base element for container tags (div, section, article, etc.)
    - Processes and validates HTML attributes (id, class_, style, etc.)
    - Processes ctn_* into ContentItem (via ContentFactory)
    - Registers in DOM if an id is present
    - Registers selectors in CSS (tag, id, classes and cascades)
    - Allows adding children only if an id is present
    - All blocks are registered globally to respect creation order
    """

    _registry = []

    def __init__(self, tag: str, *children: Any, _parent=None, **kwargs):
        self.tag = tag
        self._parent = _parent

        # Extract and validate attributes
        self.attrs = self._extract_attributes(kwargs)

        # CTN content items
        self.content_items = ContentFactory.create_from_kwargs(**kwargs)

        # Initial children
        self.children = []
        for ch in children:
            self.add_child(ch)

        # Register in DOM if id exists
        block_id = self.attrs.get("id")
        if block_id:
            DOM.register(block_id, self)

        # Register in CSS
        CSSRegistry.register_block(self)

        # Registrar en lista global para mantener orden de creación
        Block._registry.append(self)

    # ------------------------------
    # Attribute extraction and validation
    # ------------------------------
    def _extract_attributes(self, kwargs: dict) -> dict:
        attrs = {}
        for key, value in kwargs.items():
            if ContentFactory.is_ctn_key(key):
                continue

            # Normalize class_
            if key == "class_":
                key = "class"

            # Always allow 'style'
            if key == "style":
                if value not in (None, False):
                    attrs[key] = value
                continue

            # Validate against global list
            if key not in VALID_HTML_ATTRS:
                print(f"⚠️ Warning: '{key}' is not a valid HTML attribute for <{self.tag}>")
                continue

            # Validate against tag-specific list
            allowed_tag_attrs = TAG_SPECIFIC_ATTRS.get(self.tag, set())
            if allowed_tag_attrs and key not in allowed_tag_attrs and key not in ("id", "class"):
                print(f"⚠️ Warning: '{key}' is not valid for <{self.tag}>")
                continue

            # Boolean attributes
            if value is True:
                attrs[key] = None
            elif value not in (None, False):
                attrs[key] = value
        return attrs

    # ------------------------------
    # Adding children
    # ------------------------------
    def add_child(self, *children):
        if not self.attrs.get("id"):
            raise RuntimeError(f"The <{self.tag}> block does not have an id; it cannot contain children.")

        for ch in children:
            if isinstance(ch, (list, tuple)):
                for sub in ch:
                    self._attach_child(sub)
            else:
                self._attach_child(ch)

    def _attach_child(self, child):
        if isinstance(child, Block):
            child._parent = self

        if hasattr(child, "render"):
            if isinstance(child, Block):
                CSSRegistry.register_block(child)
                child_id = child.attrs.get("id")
                if child_id:
                    DOM.register(child_id, child)
            self.children.append(child)
        else:
            from .content import ContentItem
            ci = ContentItem("p", str(child))
            self.content_items.append(ci)

    # ------------------------------
    # Rendering
    # ------------------------------
    def _render_opening_tag(self, indent: int) -> str:
        space = " " * indent
        attr_text = ""
        for key, value in self.attrs.items():
            if value is None:
                attr_text += f" {key}"
            else:
                attr_text += f' {key}="{value}"'
        return f"{space}<{self.tag}{attr_text}>\n"

    def _render_closing_tag(self, indent: int) -> str:
        space = " " * indent
        return f"{space}</{self.tag}>\n"

    def _render_content(self, indent: int) -> str:
        html = ""
        for item in self.content_items:
            html += item.render(indent + 2)
        for child in self.children:
            html += child.render(indent + 2)
        return html

    def render(self, indent: int = 0) -> str:
        html = self._render_opening_tag(indent)
        html += self._render_content(indent)
        html += self._render_closing_tag(indent)
        return html

    def __str__(self):
        return self.render(0)
