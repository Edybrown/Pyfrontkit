# create_color.py

# Copyright (c) 2025 Eduardo Antonio Ferrera Rodríguez
# SPDX-License-Identifier: MIT

from . import colors_templates
from . import palettes
from pathlib import Path
import re
from itertools import product
from colorsys import rgb_to_hls, hls_to_rgb  # Python's built-in HLS module


# ----------------------------------------------------------------------
# HSL UTILITY FUNCTIONS
# ----------------------------------------------------------------------

def _hex_to_hls(hex_color):
    """Converts a HEX color string to HLS (Hue: 0-360, Luminosity/Saturation: 0-100)."""
    # Remove # and convert to R, G, B in the range 0-1
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255

    # Convert RGB (0-1) to HLS (0-1)
    h, l, s = rgb_to_hls(r, g, b)

    # Scale H to 0-360, L and S to 0-100
    return h * 360, l * 100, s * 100


def _hls_to_hex(h, l, s):
    """Converts HLS (Hue: 0-360, Luminosity/Saturation: 0-100) to HEX color string."""
    # Scale H, L, S back to 0-1 range
    h_norm = h / 360
    l_norm = l / 100
    s_norm = s / 100

    # Convert HLS (0-1) to R, G, B (0-1)
    r, g, b = hls_to_rgb(h_norm, l_norm, s_norm)

    # Scale R, G, B to 0-255 and format as HEX
    r_hex = max(0, min(255, int(r * 255)))
    g_hex = max(0, min(255, int(g * 255)))
    b_hex = max(0, min(255, int(b * 255)))

    return f"#{r_hex:02X}{g_hex:02X}{b_hex:02X}"

# ----------------------------------------------------------------------
# TAG DEFINITIONS
# ----------------------------------------------------------------------


family_tags = {
    "block_tags": [
        "body", "div", "section", "article", "header", "footer",
        "nav", "main", "aside", "button", "form", "ul", "li", "a"
    ],

    "text_tags": ["p", "span"],

    "text_htags": ["h1", "h2", "h3", "h4", "h5", "h6"],

    "void_tags": ["img", "input", "hr"],

    "special_conteiners": ["video", "audio", "object"],

    "simple_tags": [
        "body", "div", "section", "article", "header", "footer",
        "nav", "main", "aside", "button", "form", "ul", "li", "a",
        "p", "span",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "img", "input", "hr",
        "video", "audio", "object"
    ]
}

# ----------------------------------------------------------------------
# CREATECOLOR CLASS
# ----------------------------------------------------------------------


class CreateColor:
    """
    Manages color paletter generation and application to CSS based on 
    a color name, family (monochromatic, triadic, etc.), and template.
    """

    def __init__(self, color_name, family, template):
        self.css_path = Path("style.css")
        self.color_name = color_name.lower()
        self.family = family.lower()
        self.template = template.lower()
        self.template_rule = self.import_template()
        self.specific_palette = self.import_colors()

        self.tags = self.decode_template()
        self.write_and_color()

    # -------------------------
    # IMPORTS
    # -------------------------

    def import_template(self):
        """Loads the CSS template definition."""
        try:
            return getattr(colors_templates, self.template)
        except AttributeError:
            raise ValueError(
                f"Template '{self.template}' does not exist in colors_templates.")

    def import_colors(self):
        """Loads the specific color palette dictionary."""
        try:
            family_color = getattr(palettes, self.family)
            return family_color[self.color_name]
        except AttributeError:
            raise ValueError(f"Color family '{self.family}' does not exist.")
        except KeyError:
            raise ValueError(
                f"Color '{self.color_name}' does not exist for family '{self.family}'.")

    # -------------------------
    # DECODING TEMPLATE
    # -------------------------

    def decode_template(self):
        """
        Parses the color template rules, expanding tag groups into 
        specific CSS selectors (simple, double, and triple selectors).
        """
        list_selector_name = []

        # SIMPLE SELECTOR
        for group_name, type_selectors in self.template_rule.items():
            if group_name != "simple_selector":
                continue

            for tags, color_rule in type_selectors.items():
                tags = tags.lower()

                if tags in family_tags["simple_tags"]:
                    list_selector_name.append({tags: color_rule})
                elif tags in family_tags:
                    for new_tag in family_tags[tags]:
                        list_selector_name.append({new_tag: color_rule})

        # DOUBLE and TRIPLE SELECTORS (Combined Logic)
        for group_key in ["doble_selector", "triple_selector"]:
            for selector, color_rule in self.template_rule.get(group_key, {}).items():
                parts = selector.lower().split(">")
                expanded = []

                for tag in parts:
                    tag = tag.lower()
                    if tag in family_tags["simple_tags"]:
                        expanded.append([tag])
                    elif tag in family_tags:
                        expanded.append(family_tags[tag])
                    else:
                        expanded.append([tag])

                # Use itertools.product to get all combinations
                for combo in product(*expanded):
                    list_selector_name.append({">".join(combo): color_rule})

        return list_selector_name

    # -------------------------
    # HSL ADJUSTMENT LOGIC
    # -------------------------

    def _adjust_palette_hsl(self, palette, family):
        """
        Dynamically adjusts 'triadic' and 'tetradic' palettes using HSL to ensure 
        visual harmony and better web usability by varying Lightness and Saturation.
        Returns the potentially modified palette dictionary.
        """

        if family not in ("triadic", "tetradic"):
            # Return the static palette for monochromatic, homologous, etc.
            return palette

        principal_hex = palette["principal"]
        H, S, L = _hex_to_hls(principal_hex)

        new_palette = {"principal": principal_hex}
        color_roles = ["secondary", "tertiary", "quaternary"]

        # Define HUE deltas for the specified family
        if family == "triadic":
            deltas = [120, 240]
        elif family == "tetradic":
            # Using the standard rectangular tetradic: 90, 180, 270 degrees
            deltas = [90, 180, 270]

        # Define the visual adjustments for Lightness (L) and Saturation (S)
        adjustments = {
            # Secondary: Less saturated, slightly brighter for key accents
            "secondary": {"L_offset": 15, "S_reduction": 20, "L_max": 80, "S_min": 40},
            # Tertiary: Much less saturated, brighter for backgrounds/subtle elements
            "tertiary":  {"L_offset": 30, "S_reduction": 40, "L_max": 90, "S_min": 20},
            # Quaternary: Minimal saturation, very bright (useful for light borders/shadows)
            "quaternary": {"L_offset": 40, "S_reduction": 50, "L_max": 95, "S_min": 10},
        }

        for i, delta in enumerate(deltas):
            if i >= len(color_roles):
                break

            role = color_roles[i]
            adj = adjustments.get(role, {})

            # 1. Calculate new Hue
            H_new = (H + delta) % 360

            # 2. Apply Saturation and Lightness adjustments
            S_new = max(S - adj.get("S_reduction", 0), adj.get("S_min", 0))
            L_new = min(L + adj.get("L_offset", 0), adj.get("L_max", 100))

            # 3. Convert back to HEX
            new_hex = _hls_to_hex(H_new, L_new, S_new)
            new_palette[role] = new_hex

        return new_palette

    # -------------------------
    # APPLY COLORS
    # -------------------------

    def write_and_color(self):
        """
        Applies HSL adjustments (if necessary), replaces color roles 
        with specific HEX values, and injects the resulting CSS into style.css.
        """

        def decode_color_final():

            # Apply HSL adjustment logic before mapping colors
            self.specific_palette = self._adjust_palette_hsl(
                self.specific_palette, self.family)

            for name_selector in self.tags:
                for selector_name, style_color in name_selector.items():
                    for color, style in style_color.items():

                        if style in ["principal", "secondary", "tertiary", "quaternary"]:
                            try:
                                # Replace the color role string (e.g., "principal") with the HEX value
                                style_color[color] = self.specific_palette[style]

                            except KeyError:
                                # Fallback case: if 'quaternary' is requested but missing in the palette
                                if style == "quaternary" and "tertiary" in self.specific_palette:
                                    style_color[color] = self.specific_palette["tertiary"]
                                else:
                                    continue
                        else:
                            continue

            return self.tags

        decode_color_final()

        # ------------------------------
        # READ style.css
        # ------------------------------

        with open(self.css_path, "r", encoding="utf-8") as f:
            css_text = f.read()

        # ------------------------------
        # INSERT STYLES
        # ------------------------------
        for selector_dict in self.tags:
            for selector_name, style_color in selector_dict.items():

                # --- Flexible Selector Matching ---
                escaped_selector = re.escape(selector_name)

                # Replace combinators with flexible regex to handle arbitrary whitespace
                flexible_selector = escaped_selector.replace(
                    r'\>', r'\s*>\s*').replace('>', r'\s*>\s*')
                flexible_selector = flexible_selector.replace(
                    r'\+', r'\s*\+\s*').replace('+', r'\s*\+\s*')
                flexible_selector = flexible_selector.replace(
                    r'\~', r'\s*~\s*').replace('~', r'\s*~\s*')
                flexible_selector = flexible_selector.replace(
                    r'\ ', r'\s+').replace(' ', r'\s+')

                pattern = rf"{flexible_selector}\s*\{{"
                match = re.search(pattern, css_text)

                if not match:
                    continue

                insert_pos = match.end()

                insert_block = ""
                for prop, value in style_color.items():
                    # Use standard four spaces for indentation
                    insert_block += f"\n    {prop}: {value};"

                css_text = css_text[:insert_pos] + \
                    insert_block + css_text[insert_pos:]

        # ------------------------------
        # SAVE style.css
        # ------------------------------
        with open(self.css_path, "w", encoding="utf-8") as f:
            f.write(css_text)
        print("[PyFrontKit] Colors applied. style.css updated successfully.")

# ----------------------------------------------------------------------
# CREATEWITHCOLOR CLASS
# ----------------------------------------------------------------------


class CreateWithColor(CreateColor):
    """
    Allows users to manually provide primary, secondary, and tertiary colors 
    instead of relying on predefined palettes, reusing the styling logic.
    """

    def __init__(self, primary, secondary, tertiary, template, quaternary=None):

        # 1. Initialize core properties needed by inherited methods
        self.css_path = Path("style.css")
        self.template = template.lower()

        # Note: self.family is not needed for HSL logic exclusion, as it's not triadic/tetradic.
        self.family = "custom"

        # 2. Import the template rule (Reusing the inherited method)
        self.template_rule = self.import_template()

        # 3. Manually assign the user's colors to self.specific_palette
        self.specific_palette = {}

        # REQUIRED COLORS (3 minimum)
        self.specific_palette["principal"] = primary
        self.specific_palette["secondary"] = secondary
        self.specific_palette["tertiary"] = tertiary

        # OPTIONAL COLOR
        if quaternary:
            self.specific_palette["quaternary"] = quaternary

        # 4. Decode the template to generate the selector list (Reusing the inherited method)
        self.tags = self.decode_template()

        # 5. Apply colors and write to CSS (Reusing the inherited method)
        # Note: write_and_color will use self.family="custom" which skips the HSL adjustment.
        self.write_and_color()
