# SPDX-License-Identifier: MIT
# style_manager.py

"""
style_manager.py

CSS rule processor and file adapter.

Design principles:
- DRY (Don't Repeat Yourself): CSS merge logic exists in ONE place only.
- SRP (Single Responsibility Principle):
    - CSSProcessor: pure, in-memory CSS transformation logic.
    - StyleManager: filesystem adapter (read → process → write).
- Easily reusable for bundlers, HTML exporters, previews, or tests.
"""

from pathlib import Path
import re
from typing import List, Dict, Optional

CSS_RULES_STYLE: List[Dict[str, Dict[str, str]]] = []

class CSSProcessor:
    """
    Pure CSS transformation engine.

    This class contains NO filesystem access and NO side effects.
    It can safely be reused in:
    - HTML bundlers
    - CSS exporters
    - Email templates
    - Unit tests
    """

    @staticmethod
    def apply_rules(
        css_text: str,
        rules: Optional[List[Dict[str, Dict[str, str]]]] = None,
    ) -> str:
        """
        Merge CSS rules into an existing CSS string.

        This function follows DRY: it is the ONLY place where
        CSS merge logic is implemented.

        Args:
            css_text: Original CSS content.
            rules: Optional list of CSS rules. Defaults to CSS_RULES_STYLE.

        Returns:
            The merged CSS as a string.
        """
        if rules is None:
            rules = CSS_RULES_STYLE

        for rule in rules:
            for selector, data in rule.items():
                new_css = data.get("css", "").strip()
                if not new_css:
                    continue

                # Normalize new CSS lines
                new_lines = [
                    line if line.endswith(";") else line + ";"
                    for line in new_css.splitlines()
                    if line.strip()
                ]

                pattern = re.compile(
                    rf"({re.escape(selector)}\s*\{{)([^}}]*)(\}})",
                    re.MULTILINE,
                )

                match = pattern.search(css_text)

                if match:
                    # Selector exists → merge rules
                    existing_css = match.group(2).strip()
                    existing_lines = [
                        line.strip()
                        for line in existing_css.splitlines()
                        if line.strip()
                    ]

                    combined_lines = existing_lines + new_lines

                    css_text = (
                        css_text[:match.start(2)]
                        + "\n    "
                        + "\n    ".join(combined_lines)
                        + "\n"
                        + css_text[match.end(2):]
                    )
                else:
                    # Selector does not exist → append block
                    css_text += (
                        f"\n{selector} {{\n    "
                        + "\n    ".join(new_lines)
                        + "\n}\n"
                    )

        # Safety cleanup
        return css_text.replace("}}", "}")

class StyleManager:
    """
    Filesystem adapter for CSSProcessor.

    Responsibilities:
    - Read CSS from disk
    - Delegate processing to CSSProcessor
    - Write the result back to disk

    It does NOT implement CSS logic (DRY enforced).
    """

    def __init__(self, css_file: str | Path = "style.css"):
        self.css_file = Path(css_file)

        if not self.css_file.exists():
            raise FileNotFoundError(
                f"{self.css_file} not found in the current directory."
            )

    def apply_styles(self) -> None:
        """
        Apply registered CSS rules to the CSS file.

        This method is intentionally thin:
        read → process → write.
        """
        css_text = self.css_file.read_text(encoding="utf-8")

        css_text = CSSProcessor.apply_rules(css_text)

        self.css_file.write_text(css_text, encoding="utf-8")

        print(f"✅ Styles updated in {self.css_file}")
