# Copyright (c) 2025 Eduardo Antonio Ferrera Rodríguez
# SPDX-License-Identifier: MIT

# fonts.py
from typing import Optional
from pathlib import Path
import re

class CreateFont:
    
    
    def __init__(self, family: str, color: str = None, p: str = None, h1: str = None, h2: str = None, h3: str = None):
        """
        Applies font styles globally via the 'body' selector and specifically to <p>, <h1>, etc.

        :param family: The font family for the <body> selector.
        :param color: The text color for the <body> selector.
        :param p: Font size for <p> tags.
        :param h1, h2, h3: Font sizes for header tags.
        """
        self.css_path = Path("style.css")
        self.styles_to_insert = {}
        
        # Set font family and color for body
        self.styles_to_insert['body'] = {'font-family': family}
        if color:
            self.styles_to_insert['body']['color'] = color
        
        # Set font sizes
        tag_map = {'p': p, 'h1': h1, 'h2': h2, 'h3': h3}
        for tag, size in tag_map.items():
            if size:
                if tag not in self.styles_to_insert:
                    self.styles_to_insert[tag] = {}
                self.styles_to_insert[tag]['font-size'] = size
                
        self.write()


    def _update_content(self, css_content: str, selector: str, properties: dict) -> str:
        """Helper to find or create a CSS selector block and insert properties."""
        
        # This regex handles cases where the selector exists and captures the content inside the braces.
        pattern = re.compile(rf'({re.escape(selector)}\s*\{{)([^}}]*?)(\}})', re.DOTALL)
        
        # Format the properties to be inserted (e.g., "\n    font-size: 16px;")
        new_properties_css = "".join([f"\n    {prop}: {value};" for prop, value in properties.items()])
        
        match = pattern.search(css_content)

        if match:
            # Selector found: replace the entire block with updated content
            start_block = match.group(1)
            inner_content = match.group(2).strip()
            end_block = match.group(3)
            
            # Append new properties to existing content, ensuring proper formatting
            if inner_content:
                # Append to existing styles
                new_inner_content = inner_content + new_properties_css + "\n"
            else:
                # Insert directly if the block was empty
                new_inner_content = new_properties_css.lstrip() 
            
            new_block = f"{start_block}{new_inner_content}{end_block}"
            
            # Replace the first occurrence of the selector block
            return css_content.replace(match.group(0), new_block, 1)

        else:
            # Selector not found: append a new block to the end of the content
            new_block = f"\n\n{selector} {{" + new_properties_css + "\n}"
            return css_content + new_block
            
    
    def write(self):
        """Reads style.css, applies all stored styles, and writes the updated content back."""
        
        try:
            if self.css_path.exists():
                with open(self.css_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = ""
                
        except Exception as e:
            print(f"Error reading/accessing CSS file: {e}")
            return
            
        modified_content = content
        
        # Iterate through all configured selectors to update the content
        for selector, properties in self.styles_to_insert.items():
            modified_content = self._update_content(modified_content, selector, properties)
            
        # Write the modified content back to the file
        try:
            with open(self.css_path, 'w', encoding='utf-8') as f:
                f.write(modified_content.strip())
            print(f"Font styles applied successfully to {self.css_path}.")
        except Exception as e:
            print(f"Error writing to CSS file: {e}")


class HeaderFont(CreateFont):
    def __init__(self, family: Optional[str] = None, color: Optional[str] = None,
                 p: Optional[str] = None, h1: Optional[str] = None, h2: Optional[str] = None, h3: Optional[str] = None):
        """Applies font styles specifically within the <header> element."""

        # Ensure at least one argument is provided
        if not any([family, color, p, h1, h2, h3]):
            raise TypeError("HeaderFont requires at least one argument: family, color, p, h1, h2, or h3.")

        # Initialize parent attributes (dummy family, as we override self.styles_to_insert)
        super().__init__(family="Arial")

        # Build actual selectors
        self.styles_to_insert = {}
        
        # Apply family and color to the main container ('header')
        container_styles = {}
        if family:
            container_styles["font-family"] = family
        if color:
            container_styles["color"] = color # New property added
            
        if container_styles:
            self.styles_to_insert["header"] = container_styles

        # Apply font size to child elements ('header > p', etc.)
        tag_map = {"p": p, "h1": h1, "h2": h2, "h3": h3}
        for tag, size in tag_map.items():
            if size:
                # Uses child selector for specificity
                self.styles_to_insert[f"header > {tag}"] = {"font-size": size}

        # Write styles using parent's method
        self.write()


class MainFont(CreateFont):
    def __init__(self, family: Optional[str] = None, color: Optional[str] = None,
                 p: Optional[str] = None, h1: Optional[str] = None, h2: Optional[str] = None, h3: Optional[str] = None):
        """Applies font styles specifically within the <main> element."""

        if not any([family, color, p, h1, h2, h3]):
            raise TypeError("MainFont requires at least one argument: family, color, p, h1, h2, or h3.")

        # Initialize parent attributes (dummy value)
        super().__init__(family="Arial")

        # Build actual selectors
        self.styles_to_insert = {}
        
        # Apply family and color to the main container ('main')
        container_styles = {}
        if family:
            container_styles["font-family"] = family
        if color:
            container_styles["color"] = color # New property added
            
        if container_styles:
            self.styles_to_insert["main"] = container_styles

        # Apply font size to child elements ('main > p', etc.)
        tag_map = {"p": p, "h1": h1, "h2": h2, "h3": h3}
        for tag, size in tag_map.items():
            if size:
                self.styles_to_insert[f"main > {tag}"] = {"font-size": size}

        self.write()


class FooterFont(CreateFont):
    def __init__(self, family: Optional[str] = None, color: Optional[str] = None,
                 p: Optional[str] = None, h1: Optional[str] = None, h2: Optional[str] = None, h3: Optional[str] = None):
        """Applies font styles specifically within the <footer> element."""

        if not any([family, color, p, h1, h2, h3]):
            raise TypeError("FooterFont requires at least one argument: family, color, p, h1, h2, or h3.")

        # Initialize parent attributes (dummy value)
        super().__init__(family="Arial")

        # Build actual selectors
        self.styles_to_insert = {}
        
        # Apply family and color to the main container ('footer')
        container_styles = {}
        if family:
            container_styles["font-family"] = family
        if color:
            container_styles["color"] = color # New property added
            
        if container_styles:
            self.styles_to_insert["footer"] = container_styles

        # Apply font size to child elements ('footer > p', etc.)
        tag_map = {"p": p, "h1": h1, "h2": h2, "h3": h3}
        for tag, size in tag_map.items():
            if size:
                self.styles_to_insert[f"footer > {tag}"] = {"font-size": size}

        self.write()