# PYFRONTKIT  
### A Pythonic DSL for Programmatic HTML & CSS Generation

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

**PyFrontKit** is a Python-based DSL designed to generate **HTML and CSS programmatically**, providing a clean, elegant, and highly readable syntax inspired by modern component-driven development.

It allows developers to build complete web pages using **pure Python**, without writing raw HTML manually.  
Ideal for:

- rapid prototyping  
- teaching HTML structure  
- generating static sites  
- automating documentation pages  
- template-driven UI generation  

---

# 🚀 Features

### ✔ Pythonic HTML Syntax  
Create elements using class constructors or ID-based global functions:

```python
Div(id="container")
container(Section(ctn_p="Hello World"))
```

### ✔ Accumulative DOM  
Any element with an `id="..."` automatically generates a global callable:

```python
header(Div(ctn_h1="Welcome"))
```

### ✔ Automatic CSS File Generation  
All selectors (`id`, `class`, and tag names) are scanned and exported into `style.css`.

### ✔ Inline Style Support  
Every tag accepts a native HTML5 `style="..."` attribute.

### ✔ Clean Separation Between Content & Structure  
`ctn_p`, `ctn_h1`, `ctn_div`, etc. allow pythonic, newline-based content — internally converted to `<p>`, `<br>`, `<h1>`, etc.

### ✔ Ready-to-open Output  
The library produces:

```
index.html
style.css
```

---

# 📦 Installation

### From PyPI (recommended)

```bash
pip install pyfrontkit
```

### From GitHub

```bash
pip install git+https://github.com/Edybrown/pyfrontkit.git
```

---

# 💡 Basic Usage Example

```python
from pyfrontkit import HtmlDoc, Div, Section, Header, Nav, Ul, Li, Footer

doc = HtmlDoc(title="My Professional Page")

# Header
Header(id="header", ctn_p="Welcome to My Professional Site",
       style="background-color:#2c3e50; color:white; padding:20px 0;")

# Navigation
Nav(id="nav", style="background-color:#34495e; display:flex; justify-content:center;")
nav(
    Div(ctn_p="Home", style="color:white; padding:15px 25px;"),
    Div(ctn_p="Services", style="color:white; padding:15px 25px;")
)

# Introduction
Section(id="intro", style="padding:40px 20px; max-width:1000px; margin:auto;")
intro(
    Div(ctn_p="This is the introduction section, generated entirely in Python.")
)

# Footer
Footer(id="footer", style="background-color:#2c3e50; color:white; text-align:center; padding:20px 0;")
footer(
    Div(ctn_p="© 2025 My Professional Site. All rights reserved.")
)

# Build files
doc.create_document()
```

Output generated:

```
index.html
style.css
```

---

# 🎨 CSS Usage Guide

PyFrontKit automatically generates a `style.css` file containing **all selectors found in the HTML**:

Example auto-generated output:

```css
#header {}
#nav {}
#intro {}
#footer {}
div {}
section {}
```

You can now fill these selectors manually:

```css
#header {
    background:#2c3e50;
    color:white;
    padding:20px 0;
}
```

## Styling methods

### 1. Inline Styles (fast prototyping)

```python
Div(ctn_p="Hello", style="color:red; margin-top:10px;")
```

### 2. External CSS File (recommended)

Edit the generated `style.css`:

```css
div {
    font-family: Arial, sans-serif;
}
```

---

# 📁 Examples (with screenshots)

A full set of examples is included in the repository:

```
examples/
│
├── 01-basic/
│   ├── example.py
│   ├── index.html
│   ├── style.css
│   └── screenshot.png
│
├── 02-intermediate/
│   ├── example.py
│   ├── index.html
│   ├── style.css
│   └── screenshot.png
│
└── 03-professional/
    ├── example.py
    ├── index.html
    ├── style.css
    └── screenshot.png
```

Run any example:

```bash
python examples/03-professional/example.py
```

---

# 🛠 Roadmap

Planned features:

- ✔ **CSS Template Packs** (global themes)
- ✔ **Automatic external CSS compilation**
- ✔ **Reusable Python components**
- ✔ **Dynamic `<script>` builder**
- ✔ **Minified output mode**
- ✔ **Plugin system for custom tags**

---

# 📄 License

Released under the **GNU GPLv3** license.  
You are free to use, modify, and redistribute this project.  
Any derivative work must remain open-source under the same license.

---

# 👤 Author

Created by **Eduardo Antonio Ferrera Rodríguez**  
A project combining:

- advanced Python OOP practice  
- DSL design  
- frontend structure understanding  
- static web automation  

Contributions, suggestions, and pull requests are welcome!

