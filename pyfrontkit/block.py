# Copyright (c) 2025 Eduardo Antonio Ferrera Rodríguez
# SPDX-License-Identifier: MIT

# pyfrontkit/block.py

from .content import ContentFactory
from .css_register import CSSRegistry # Ya está importado
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
    - Allows adding children only if an id is present
    - All blocks are registered globally to respect creation order
    """

    _registry = []
    _auto_id_counter = 0 
    _registry = [] 


    ALLOWED_CHILDREN = {
    "video": {"source", "track"},
    "audio": {"source", "track"},
    "picture": {"source", "img"},
    # object acepta todo (fallback)
}

    REQUIRES_LAST_CHILD = {
    "picture": "img"
}

 
    def __init__(self, tag: str, *children: Any, _parent=None, **kwargs):
        self.tag = tag
        self._parent = _parent

        # ----------------------------------------------------------------------
        # Auto-inject an ID or class when none is provided
        # ----------------------------------------------------------------------

        user_has_id = "id" in kwargs and kwargs.get("id")
        user_has_class = (
            ("class" in kwargs and kwargs.get("class")) or
            ("class_" in kwargs and kwargs.get("class_"))
        )

        if not user_has_id and not user_has_class:
            Block._auto_id_counter += 1
            kwargs["id"] = f"_pyfk_auto_{Block._auto_id_counter}"

        # Extract attributes (kwargs always contains an ID at this point)
        self.attrs = self._extract_attributes(kwargs)

        # Create content items based on content-related kwargs
        self.content_items = ContentFactory.create_from_kwargs(**kwargs)

        # Child assignment
        self.children = []
        for ch in children:
            self.add_child(ch)

        # Register in DOM (the ID always exists at this point)
        block_id = self.attrs.get("id")
        if block_id:
            from .dom import DOM
            DOM.register(block_id, self)

        # Register block in CSS registry
        from .css_register import CSSRegistry
        CSSRegistry.register_block(self)

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
            # Special handling for ID — must always exist
            if key == "id":
                # If user supplied None, False, empty "", regenerate a valid auto-id
                if not value:
                    Block._auto_id_counter += 1
                    value = f"_pyfk_auto_{Block._auto_id_counter}"
                attrs["id"] = value
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
        
        # 1. Handle elements capable of rendering (Block, VoidElement, etc.)
        if hasattr(child, "render"):
            
            # Set parent reference for the child object
            if hasattr(child, '_parent'):
                child._parent = self 
            
            # If it's a Block, set the parent reference explicitly
            if isinstance(child, Block):
                child._parent = self

            # --- Apply Tag-Specific Child Rules ---
            rules = self.ALLOWED_CHILDREN.get(self.tag)

            if rules and isinstance(child, Block):
                child_tag = getattr(child, "tag", None)
                if child_tag not in rules:
                    raise RuntimeError(
                        f"<{self.tag}> does not accept <{child_tag}> as a child."
                    )

            # 2. Append the child ONLY ONCE (Fixes duplication issue)
            self.children.append(child)

            # 3. Register child ID in DOM if applicable
            if isinstance(child, Block):
                child_id = child.attrs.get("id")
                if child_id:
                    from .dom import DOM
                    DOM.register(child_id, child)
            
            # --- Apply Last Child Validation (e.g., for <picture>) ---
            if self.tag in self.REQUIRES_LAST_CHILD:
                required = self.REQUIRES_LAST_CHILD[self.tag]
                if self.children:
                    last = self.children[-1]
                    last_tag = getattr(last, "tag", None)

                    if last_tag != required:
                        raise RuntimeError(
                            f"<{self.tag}> must end with <{required}>"
                        )   
        
        # 4. Handle non-renderable/raw string content
        else:
            from .content import ContentItem
            ci = ContentItem("p", str(child))
            self.content_items.append(ci)

    
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

    def _get_main_selector(self):
        """
        Returns the strongest selector. Debido a la inyección de ID en __init__, 
        la Prioridad 1 siempre se ejecutará para las instancias de Block.
        """
        
        
        if self.attrs.get("id"):
            return f"#{self.attrs['id']}", "id"

        
        elif self.attrs.get("class"):
            return f".{self.attrs['class']}", "class"
        
        
        else:
            return self.tag, "tag"
        

    def align(self, orientation=None, gap=None, padding=None, pad_top=None,pad_right=None, pad_bottom=None, pad_left=None, grid_column=None, fsize=None, text_align=None):
        """
        Controls the layout of this block and optionally text alignment and font-size.
        """

        if orientation is None:
            print("align(): 'orientation' parameter is required")
            return self

        if orientation not in ("column", "row", "grid"):
            print("align(): invalid orientation. Use 'column', 'row' or 'grid'")
            return self

        if orientation == "grid" and not grid_column:
            print("align(): 'grid_column' is required when orientation='grid'")
            return self

        # -------------------------
        # Text-align semantic map
        # -------------------------
        TEXT_ALIGN_MAP = {
            "start": "start",
            "left": "left",
            "center": "center",
            "end": "end",
            "right": "right",
            "expand": "justify",
        }

        if text_align and text_align not in TEXT_ALIGN_MAP:
            print(
                "align(): invalid text_align value. "
                "Use: start, left, center, end, right, expand"
            )
            return self

        selector, _ = self._get_main_selector()

        # -------------------------
        # CSS Templates
        # -------------------------
        templates = {
            "column": '''
        display: flex;
        flex-direction: column;
        {gap}
        {padding}
        {pad_top}
        {pad_right}
        {pad_bottom}
        {pad_left}
        {font_size}
        {text_align}
        ''',
            "row": '''
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        {gap}
        {padding}
        {pad_top}
        {pad_right}
        {pad_bottom}
        {pad_left}
        {font_size}
        {text_align}
        ''',
            "grid": '''
        display: grid;
        grid-template-columns: repeat({grid_column}, 1fr);
        {gap}
        {padding}
        {pad_top}
        {pad_right}
        {pad_bottom}
        {pad_left}
        {font_size}
        {text_align}
        '''
        }

        # -------------------------
        # Optional parameters
        # -------------------------
        gap_text = f"gap: {gap};" if gap else ""
        padding_text = f"padding: {padding};" if padding else ""

        pad_top_text = f"padding-top: {pad_top};" if pad_top else ""
        pad_right_text = f"padding-right: {pad_right};" if pad_right else ""
        pad_bottom_text = f"padding-bottom: {pad_bottom};" if pad_bottom else ""
        pad_left_text = f"padding-left: {pad_left};" if pad_left else ""

        font_size_text = f"font-size: {fsize};" if fsize else ""
        text_align_text = (
            f"text-align: {TEXT_ALIGN_MAP[text_align]};"
            if text_align else ""
        )

        # -------------------------
        # Build final CSS
        # -------------------------
        template = templates[orientation]
        css_text = template.format(
            gap=gap_text,
            padding=padding_text,
            pad_top=pad_top_text,
            pad_right=pad_right_text,
            pad_bottom=pad_bottom_text,
            pad_left=pad_left_text,
            font_size=font_size_text,
            text_align=text_align_text,
            grid_column=grid_column if grid_column else "1"
        )

        # -------------------------
        # Register rule
        # -------------------------
        from .style_manager import CSS_RULES_STYLE
        CSS_RULES_STYLE.append({selector: {"css": css_text}})

        return self

    # Assuming this method belongs to a class like BlockStyle or similar

    def form(self, width=None, height=None, border_radius=None, background=None, color=None):
        """
        Set the size, shape, background color, and text color of the Block container.
        
        Parameters:
            width (str): container width (e.g., '200px', '50%')
            height (str): container height (e.g., '100px', 'auto')
            border_radius (str): container shape (e.g., '0', '10px', '50%')
            background (str): Background color (e.g., '#FFF', 'blue', 'rgb(255, 255, 255)')
            color (str): Text color (e.g., '#000', 'white')
        """
        # ------------------------------
        # Get main selector
        # ------------------------------
        # Assuming _get_main_selector() returns the CSS selector for the block
        selector, _ = self._get_main_selector() 

        # ------------------------------
        # Build CSS lines
        # ------------------------------
        css_lines = []
        if width:
            css_lines.append(f"width: {width};")
        if height:
            css_lines.append(f"height: {height};")
        if border_radius:
            css_lines.append(f"border-radius: {border_radius};")
        
        # --- NEW COLOR CONTROLS ---
        if background:
            css_lines.append(f"background: {background};") # Controls background-color
        if color:
            css_lines.append(f"color: {color};")          # Controls text color (font-color)
        # --------------------------

        css_text = "\n".join(css_lines)

        # ------------------------------
        # Save to global style list
        # ------------------------------
        # Assuming the existence of a global style manager
        from .style_manager import CSS_RULES_STYLE
        
        # Prepare the dictionary for insertion
        if css_text:
            # Check if the selector already exists in the list to update/append
            updated = False
            for rule in CSS_RULES_STYLE:
                if selector in rule:
                    # Append new properties to the existing CSS block
                    rule[selector]["css"] += "\n" + css_text
                    updated = True
                    break
            
            if not updated:
                # Add new selector block
                CSS_RULES_STYLE.append({selector: {"css": css_text}})

        return self
    
    
    def position(self, top=None, left=None, right=None, bottom=None, z_index=None):
        """
        Absolute positioning template.
        """

        if all(v is None for v in (top, left, right, bottom)):
            print("position(): at least one position value is required")
            return self

        selector, _ = self._get_main_selector()

        css_lines = ["position: absolute;"]

        if top is not None:
            css_lines.append(f"top: {top};")
        if left is not None:
            css_lines.append(f"left: {left};")
        if right is not None:
            css_lines.append(f"right: {right};")
        if bottom is not None:
            css_lines.append(f"bottom: {bottom};")
        if z_index is not None:
            css_lines.append(f"z-index: {z_index};")

        css_text = "\n".join(css_lines)

        from .style_manager import CSS_RULES_STYLE

        for rule in CSS_RULES_STYLE:
            if selector in rule:
                rule[selector]["css"] += "\n" + css_text
                break
        else:
            CSS_RULES_STYLE.append({selector: {"css": css_text}})

        return self


    def border(self, size=None, style="solid", color=None):
    

        selector, _ = self._get_main_selector()

        valid_styles = {
            "solid", "dashed", "dotted", "double",
            "groove", "ridge", "inset", "outset",
            "none", "hidden"
        }

        css_lines = []

        # --- Size (no strict validation) ---
        if size:
            css_lines.append(f"border-width: {size};")

        # --- Style (validated) ---
        if style:
            if style not in valid_styles:
                print(f"border(): invalid style -> {style}")
            else:
                css_lines.append(f"border-style: {style};")

        # --- Color (free, no validation) ---
        if color:
            css_lines.append(f"border-color: {color};")

        css_text = "\n".join(css_lines)

        from .style_manager import CSS_RULES_STYLE

        if css_text:
            updated = False
            for rule in CSS_RULES_STYLE:
                if selector in rule:
                    rule[selector]["css"] += "\n" + css_text
                    updated = True
                    break

            if not updated:
                CSS_RULES_STYLE.append({selector: {"css": css_text}})

        return self


    def shadow(self, x=None, y=None, blur=None, spread=None, color=None, inset=False):
        

        selector, _ = self._get_main_selector()

        css_parts = []

        # Required minimal values
        if x:
            css_parts.append(x)
        else:
            css_parts.append("0px")

        if y:
            css_parts.append(y)
        else:
            css_parts.append("0px")

        # Optional extras
        if blur:
            css_parts.append(blur)

        if spread:
            css_parts.append(spread)

        if color:
            css_parts.append(color)

        # Inset shadow
        if inset:
            css_parts.insert(0, "inset")

        css_text = f"box-shadow: {' '.join(css_parts)};"

        from .style_manager import CSS_RULES_STYLE

        updated = False
        for rule in CSS_RULES_STYLE:
            if selector in rule:
                rule[selector]["css"] += "\n" + css_text
                updated = True
                break

        if not updated:
            CSS_RULES_STYLE.append({selector: {"css": css_text}})

        return self


    def margin(self, top=None, right=None, bottom=None, left=None):
        selector, _ = self._get_main_selector()

        css_lines = []

        if top:
            css_lines.append(f"margin-top: {top};")
        if right:
            css_lines.append(f"margin-right: {right};")
        if bottom:
            css_lines.append(f"margin-bottom: {bottom};")
        if left:
            css_lines.append(f"margin-left: {left};")

        if not css_lines:
            return self

        css_text = "\n".join(css_lines)

        from .style_manager import CSS_RULES_STYLE

        updated = False
        for rule in CSS_RULES_STYLE:
            if selector in rule:
                rule[selector]["css"] += "\n" + css_text
                updated = True
                break

        if not updated:
            CSS_RULES_STYLE.append({selector: {"css": css_text}})

        return self


    def hover(self, color=None, background=None, scale=None, transition="0.2s"):
        """
        Set hover effect for this block.

        Parameters:
            color (str): text color on hover
            background (str): background color on hover
            scale (float): scale factor on hover (e.g., 1.1 = 10% larger)
            transition (str): CSS transition duration for smooth effect
        """
        from .style_manager import CSS_RULES_STYLE

        # ------------------------------
        # Get main selector
        # ------------------------------
        selector, _ = self._get_main_selector()

        # ------------------------------
        # Add transition to base selector
        # ------------------------------
        updated = False
        for rule in CSS_RULES_STYLE:
            if selector in rule:
                # Añadir transition si no existe
                if "transition" not in rule[selector]["css"]:
                    rule[selector]["css"] += f"\ntransition: all {transition} ease;"
                updated = True
                break
        if not updated:
            CSS_RULES_STYLE.append({selector: {"css": f"transition: all {transition} ease;"}})

        # ------------------------------
        # Build hover CSS
        # ------------------------------
        css_lines = []
        if color:
            css_lines.append(f"color: {color};")
        if background:
            css_lines.append(f"background: {background};")
        if scale:
            css_lines.append(f"transform: scale({scale});")

        if css_lines:
            hover_selector = f"{selector}:hover"
            hover_css = "\n".join(css_lines)

            # Verificar si hover ya existe
            updated_hover = False
            for rule in CSS_RULES_STYLE:
                if hover_selector in rule:
                    # Reemplazar hover en vez de concatenar
                    rule[hover_selector]["css"] = hover_css
                    updated_hover = True
                    break
            if not updated_hover:
                CSS_RULES_STYLE.append({hover_selector: {"css": hover_css}})

        return self
