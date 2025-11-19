# PYFRONT: DSL for Programmatic Web Generation

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

**PYFRONT** is a Python library designed to programmatically generate **HTML and CSS** web structures. It acts as a **Domain-Specific Language (DSL)**, allowing developers to build complete web pages using only clean Python syntax.

Its main goal is **rapid prototyping** and the creation of simple frontends, ideal for Data Apps, documentation, or visualizing results in Machine Learning environments.

---

## Key Features

* **Fluent Block Syntax:** HTML tags are represented as Classes or Functions (`Div`, `div`), keeping all logic entirely in Python.
* **Accumulative DOM Manager:** A unique feature that converts any block’s `id` into a global function. This allows adding children (`Div(id="parent"); parent(Child1, Child2)`) without recursive nesting.
* **Automatic CSS Generation:** The system tracks all used `id`, `class`, and `tags` to automatically generate a `style.css` file with **all selectors ready** to be filled.
* **Native JS Support:** Allows inclusion of scripts via the `Script` class.
* **Final Rendering:** Produces `index.html` and `style.css` ready to serve.

---

## Installation

Install FRONTPY directly from the GitHub repository:

```bash
pip install git+https://github.com/Edybrown/FrontPy.git
```

---

## 💡 Usage Example (Professional Page)

The following Python code generates a semantic page structure and its associated stylesheet (`style.css`):

```python
from frontpy import HtmlDoc, Div, Section, Header, Nav, Ul, Li 
from frontpy import nav, intro, servicios, lista_servicios, footer

doc = HtmlDoc(title="My Professional Page")

Header(id="header", ctn_p="Welcome to My Professional Site",
       style="background-color:#2c3e50; color:white; padding:20px 0;")

Nav(id="nav", style="background-color:#34495e; display:flex; justify-content:center;")
# The id "nav" becomes the function nav()
nav(
    Div(ctn_p="Home", style="color:white; padding:15px 25px;"),
    Div(ctn_p="Services", style="color:white; padding:15px 25px;"),
)

Section(id="intro", style="padding:40px 20px; max-width:1000px; margin:auto;")
intro(
    Div(ctn_p="This is the introduction section, generated without HTML code."),
)

Section(id="servicios", style="padding:40px 20px; max-width:1000px; margin:auto;")
servicios(
    Ul(id="lista_servicios")
)
lista_servicios(
    Li(ctn_p="Custom web development"),
    Li(ctn_p="Technology consulting")
)

Footer(id="footer", style="background-color:#2c3e50; color:white; text-align:center; padding:20px 0;")
footer(Div(ctn_p="© 2025 My Professional Site. All rights reserved."))

doc.create_document()
```

---

## ⚖️ License

This project is released under the **GNU General Public License version 3.0 (GPLv3)**.

* Allows free use, modification, and redistribution.
* Requires that any software using FRONTPY or its derivatives also be free software (copyleft).

See the `COPYING` file for the full license text.

---

## 🙋 About the Author

This project was created by **Eduardo Antonio Ferrera Rodríguez** as part of an advanced learning journey in Python, *Object-Oriented Programming* (OOP), and library design.

If you have questions or want to contribute to FrontPy, you are welcome!

---

