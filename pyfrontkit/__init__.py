# ----------------------------------------------------------------------
# Package Configuration
# ----------------------------------------------------------------------
__version__ = "0.9.0"
__author__ = "Eduardo Antonio Ferrera Rodriguez"
__license__ = "GPLv3"

# ----------------------------------------------------------------------
# Export main classes and functions
# ----------------------------------------------------------------------

# Core modules
from .html_doc import HtmlDoc
from .css import CSSRegistry
from .block import Block

# Tags
from .tags import (
    Div, Section, Article, Header, Footer, Nav, Main, Aside, Button, Form, Ul, Li, A,
    div, section, article, header, footer, nav, main, aside, button, form, ul, li, a
)

# Void elements
from .void_element import (
    VoidElement, Img, Input, Hr, Meta, Link, Source, Embed, Param, Track, Wbr, Area, Base, Col,
    img, input, hr, meta, link, source, embed, param, track, wbr, area, base, col
)

# Special containers
from .special import Video, Audio, Picture, ObjectElement
from .special import video, audio, picture, object
