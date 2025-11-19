from pyfrontkit import HtmlDoc, Div, Section, Header, Nav, Ul, Li, Footer

doc = HtmlDoc(title="My Professional Page")

# ------------------------------
# Header
# ------------------------------
Header(
    id="header",
    ctn_p="Welcome to My Professional Site",
    style=(
        "background:#2c3e50; color:white; padding:30px 20px; "
        "text-align:center; font-size:1.8em; font-weight:bold; letter-spacing:1px;"
    )
)

# ------------------------------
# Navigation
# ------------------------------
Nav(
    id="nav",
    style=(
        "background:#34495e; display:flex; justify-content:center; "
        "gap:20px; padding:10px 0;"
    )
)
nav(
    Div(ctn_p="Home", style="color:white; padding:10px 20px; cursor:pointer; border-radius:5px; transition:0.3s;"),
    Div(ctn_p="Services", style="color:white; padding:10px 20px; cursor:pointer; border-radius:5px; transition:0.3s;"),
    Div(ctn_p="Contact", style="color:white; padding:10px 20px; cursor:pointer; border-radius:5px; transition:0.3s;"),
)

# ------------------------------
# Introduction Section
# ------------------------------
Section(
    id="intro",
    style=(
        "padding:60px 20px; max-width:1000px; margin:auto; "
        "background:#ecf0f1; border-radius:10px; box-shadow:0 4px 10px rgba(0,0,0,0.1);"
    )
)
intro(
    Div(ctn_p="This is the introduction section. Learn about our mission, vision, and approach.",
        style="font-size:1.2em; line-height:1.6; color:#2c3e50;")
)

# ------------------------------
# Services Section
# ------------------------------
Section(
    id="services",
    style=(
        "padding:60px 20px; max-width:1000px; margin:auto; "
        "background:#fff; border-radius:10px; box-shadow:0 4px 10px rgba(0,0,0,0.05);"
    )
)
services(Ul(id="service_list", style="list-style-type:disc; padding-left:20px;"))
service_list(
    Li(ctn_p="Custom web development", style="margin-bottom:10px;"),
    Li(ctn_p="Technology consulting", style="margin-bottom:10px;"),
    Li(ctn_p="UX/UI design", style="margin-bottom:10px;")
)

# ------------------------------
# Footer
# ------------------------------
Footer(
    id="footer",
    style=(
        "background:#2c3e50; color:white; text-align:center; "
        "padding:30px 20px; font-size:0.9em;"
    )
)
footer(Div(ctn_p="© 2025 My Professional Site. All rights reserved."))

# ------------------------------
# Create document
# ------------------------------
doc.create_document()
