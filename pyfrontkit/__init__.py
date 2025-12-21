# ----------------------------------------------------------------------
# Package Configuration
# ----------------------------------------------------------------------
__version__ = "1.1.6"
__author__ = "Eduardo Antonio Ferrera Rodriguez"
__license__ = "MIT"

# ----------------------------------------------------------------------
# Expose CSS submodule
# ----------------------------------------------------------------------
from . import css

# Expose CreateColor directly
from .css import CreateColor
from .css import CreateWithColor
from .css.fonts import CreateFont
from .css.fonts import FooterFont
from .css.fonts import HeaderFont
from .css.fonts import MainFont
# ----------------------------------------------------------------------
# Core modules
# ----------------------------------------------------------------------
from .html_doc import HtmlDoc
from .css_register import CSSRegistry
from .block import Block

# ----------------------------------------------------------------------
# Tags
# ----------------------------------------------------------------------
from .tags import (
    Div, Section, Article, Header, Footer, Nav, Main, Aside, Button, Form, Ul, Li, A,Picture,Video,Audio,Object,T ,
    div, section, article, header, footer, nav, main, aside,
    button, form, ul, li, a,picture,video, audio, object, t
)

# ----------------------------------------------------------------------
# Void elements
# ----------------------------------------------------------------------
from .void_element import (
    VoidElement, Img, Input, Hr,  Link, Source, Embed, Param, Track,
    Wbr, Area, Base, Col,
    img, Input, hr,  link, source, embed, param, track,
    wbr, area, base, col
)


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
__all__ = [
    # CSS
    "css",
    "CreateColor",
    "CreateWithColor",
    "CreateFont", 
    "FooterFont",
    "HeaderFont",
    "MainFont",
    
    # Core
    "HtmlDoc",
    "CSSRegistry",
    "Block",

    # Tags
    "Div", "Section", "Article", "Header", "Footer", "Nav", "Main", "Aside",
    "Button", "Form", "Ul", "Li", "A","T"
    "div", "section", "article", "header", "footer", "nav", "main", "aside",
    "button", "form", "ul", "li", "a", "t"

    # Void elements
    "VoidElement", "Img", "Input", "Hr", "Meta", "Link", "Source",
    "Embed", "Param", "Track", "Wbr", "Area", "Base", "Col",
    "img", "hr",  "link", "source", "embed",
    "param", "track", "wbr", "area", "base", "col",

    # Special containers
    "Video", "Audio", "Picture", "ObjectElement",
    "video", "audio", "picture", "Object",
]   
