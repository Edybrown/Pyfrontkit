from pyfrontkit import HtmlDoc, Div, Section, Header, Nav, Ul, Li, Footer

doc = HtmlDoc(title="Modern Landing Page")

# ------------------------------
# Header
# ------------------------------
Header(
    id="header",
    ctn_p="Welcome to Our Modern Site",
    style=(
        "background:#f39c12; color:white; padding:40px 20px; "
        "text-align:center; font-size:2em; font-weight:600; font-family:Helvetica, sans-serif;"
    )
)

# ------------------------------
# Navigation
# ------------------------------
Nav(
    id="nav",
    style=(
        "display:flex; justify-content:center; gap:25px; "
        "padding:15px 0; background:#f1c40f; border-bottom:2px solid #e67e22;"
    )
)
nav(
    Div(ctn_p="Home", style="color:#2c3e50; padding:10px 15px; font-weight:bold; cursor:pointer; transition:0.3s;"),
    Div(ctn_p="About", style="color:#2c3e50; padding:10px 15px; font-weight:bold; cursor:pointer; transition:0.3s;"),
    Div(ctn_p="Services", style="color:#2c3e50; padding:10px 15px; font-weight:bold; cursor:pointer; transition:0.3s;"),
    Div(ctn_p="Contact", style="color:#2c3e50; padding:10px 15px; font-weight:bold; cursor:pointer; transition:0.3s;")
)

# ------------------------------
# Hero Section
# ------------------------------
Section(
    id="hero",
    style=(
        "padding:80px 20px; text-align:center; "
        "background:#ecf0f1;"
    )
)
hero(
    Div(
        ctn_p="Modern, elegant, and responsive design for your next project.",
        style="font-size:1.5em; max-width:800px; margin:auto; line-height:1.6; color:#2c3e50;"
    )
)

# ------------------------------
# Features Section
# ------------------------------
Section(
    id="features",
    style=(
        "padding:60px 20px; max-width:1000px; margin:auto; "
        "display:grid; grid-template-columns:repeat(auto-fit, minmax(250px,1fr)); gap:20px;"
    )
)
features(
    Div(ctn_p="🚀 Fast Performance", style="background:#f39c12; color:white; padding:20px; border-radius:10px; text-align:center;"),
    Div(ctn_p="🎨 Modern Design", style="background:#3498db; color:white; padding:20px; border-radius:10px; text-align:center;"),
    Div(ctn_p="🔒 Secure", style="background:#2ecc71; color:white; padding:20px; border-radius:10px; text-align:center;"),
    Div(ctn_p="⚡ Easy to Use", style="background:#e74c3c; color:white; padding:20px; border-radius:10px; text-align:center;")
)

# ------------------------------
# Footer
# ------------------------------
Footer(
    id="footer",
    style=(
        "background:#34495e; color:white; text-align:center; "
        "padding:25px 20px; font-size:0.9em;"
    )
)
footer(
    Div(ctn_p="© 2025 Modern Site. All rights reserved.")
)

# ------------------------------
# Create document
# ------------------------------
doc.create_document()
