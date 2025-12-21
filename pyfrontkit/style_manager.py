# SPDX-License-Identifier: MIT
# style_manager.py
import re
import os
from pathlib import Path

CSS_RULES_STYLE = []

class StyleManager:
    def __init__(self, css_file="style.css"):
        self.css_file = Path(css_file)
        if not os.path.exists(css_file):
            raise FileNotFoundError(f"{css_file} not found in the current directory.")

    def apply_styles(self):
        with open(self.css_file, "r", encoding="utf-8") as f:
            css_text = f.read()

        for rule in CSS_RULES_STYLE:
            for selector, data in rule.items():
                new_css = data.get("css", "").strip()
                if not new_css:
                    continue

               
                is_hover = ":hover" in selector
                css_selector = selector  

               
                new_lines = [line if line.endswith(";") else line + ";" for line in new_css.splitlines() if line.strip()]

                pattern = re.compile(rf"({re.escape(css_selector)}\s*\{{)([^}}]*)(\}})", re.MULTILINE)
                match = pattern.search(css_text)

                if match:
                    existing_css = match.group(2).strip()
                    existing_lines = [line.strip() for line in existing_css.splitlines() if line.strip()]
                    combined_lines = existing_lines + new_lines
                    css_text = css_text[:match.start(2)] + "\n    " + "\n    ".join(combined_lines) + "\n" + css_text[match.end(2):]
                else:
                   
                    css_text += f"\n{css_selector} {{\n    " + "\n    ".join(new_lines) + "\n}}\n"
        css_text = css_text.replace("}}", "}")   
        with open(self.css_file, "w", encoding="utf-8") as f:
            f.write(css_text)

        print(f"✅ Styles updated in {self.css_file}")
