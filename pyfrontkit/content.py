# Copyright (c) 2025 Eduardo Antonio Ferrera Rodríguez
# SPDX-License-Identifier: MIT

# pyfrontkit/content.py

class ContentItem:
    """
    Represents a content element:
    - If tag is 'none', it renders raw text.
    - Otherwise, renders <tag>text</tag>.
    """

    def __init__(self, tag: str, text: str, class_: str = None, style: str = None):
        self.tag = tag
        self.lines = text.split("\n") if text else []
        self.class_ = class_
        self.style = style

    def render(self, indent: int = 0):
        space = " " * indent
        
        # --- LOGIC FOR RAW TEXT (NO TAG) ---
        if self.tag == "none":
            html = ""
            for i, line in enumerate(self.lines):
                html += f"{space}{line}"
                if i < len(self.lines) - 1:
                    html += "<br />"
                html += "\n"
            return html

        # --- LOGIC FOR STANDARD TAGS ---
        attrs = ""
        if self.class_:
            attrs += f' class="{self.class_}"'
        if self.style:
            attrs += f' style="{self.style}"'

        html = f"{space}<{self.tag}{attrs}>"
        for i, line in enumerate(self.lines):
            html += line
            if i < len(self.lines) - 1:
                html += "<br />"
        html += f"</{self.tag}>\n"
        return html


class ContentFactory:
    """
    Creates ContentItem objects. 
    Supports 'ctn_none' for raw text without wrapping tags.
    """

    # Added 'none' to supported tags
    SUPPORTED_TAGS = {
        "none", "p", "span",
        "b", "strong", "i", "u", "em", "small", "mark", "code",
        "h1", "h2", "h3", "h4", "h5", "h6"
    }

    @classmethod
    def is_ctn_key(cls, key: str) -> bool:
        return key.startswith("ctn_") and key[4:] in cls.SUPPORTED_TAGS

    @classmethod
    def create_from_kwargs(cls, **kwargs):
        items = []
        for key, value in kwargs.items():
            if cls.is_ctn_key(key):
                tag = key[4:] 

                if isinstance(value, tuple):
                    text = value[0] if len(value) > 0 else ""
                    class_ = value[1] if len(value) > 1 else None
                    style = value[2] if len(value) > 2 else None
                    items.append(ContentItem(tag, text, class_, style))
                else:
                    items.append(ContentItem(tag, value))
        return items