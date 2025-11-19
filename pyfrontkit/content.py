
# Copyright (C) [2025] Eduardo Antonio Ferrera Rodríguez
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; see the COPYING file for more details.


# pyfrontkit/content.py

class ContentItem:
    """
    Represents a simple content element:
    <tag>text</tag>
    
    Supports Python newline (\n) conversion into <br /> automatically.
    """

    def __init__(self, tag: str, text: str):
        self.tag = tag
        self.lines = text.split("\n")  # split text by newline

    def render(self, indent: int = 0):
        space = " " * indent
        html = f"{space}<{self.tag}>"
        for i, line in enumerate(self.lines):
            html += line
            if i < len(self.lines) - 1:
                html += "<br />"
        html += f"</{self.tag}>\n"
        return html


class ContentFactory:
    """
    Responsible for creating ContentItem objects from keys like 'ctn_p', 'ctn_h1', etc.
    """

    # Official list of supported tags
    SUPPORTED_TAGS = {
        "p", "span",
        "b", "strong", "i", "u", "em", "small", "mark", "code",
        "h1", "h2", "h3", "h4", "h5", "h6"
    }

    @classmethod
    def is_ctn_key(cls, key: str) -> bool:
        """Checks if the key follows the 'ctn_tag' pattern."""
        return key.startswith("ctn_") and key[4:] in cls.SUPPORTED_TAGS

    @classmethod
    def create_from_kwargs(cls, **kwargs):
        """
        Processes kwargs and returns a list of ContentItem.
        Example: ctn_p="hello" → ContentItem("p", "hello")
        """
        items = []

        for key, value in kwargs.items():
            if cls.is_ctn_key(key):
                tag = key[4:]  # remove 'ctn_'
                items.append(ContentItem(tag, value))

        return items
