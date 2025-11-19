from pyfrontkit import HtmlDoc, Div, Section, Header, Nav, Ul, Li, Footer, A

doc = HtmlDoc(title="Professional Landing Page")

# ------------------------------
# Header con imagen de fondo y degradado
# ------------------------------
Header(
    id="header",
    style=(
        "background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), "
        "url('https://picsum.photos/1920/1080') center/cover no-repeat;"
        "color:white; padding:100px 20px; text-align:center; font-family:'Arial', sans-serif;"
    )
)
header(
    Div(id="header_text", ctn_p="Welcome to Our Professional Site",
        style="font-size:2.5em; font-weight:bold;")
)

# ------------------------------
# Navigation
# ------------------------------
Nav(
    id="nav",
    style=(
        "display:flex; justify-content:center; gap:30px; padding:20px 0; "
        "background:#222; font-weight:bold; text-transform:uppercase;"
    )
)
nav(
    A(id="nav_home", ctn_p="Home", href="#header", style="color:white; text-decoration:none; transition:0.3s;"),
    A(id="nav_portfolio", ctn_p="Portfolio", href="#portfolio", style="color:white; text-decoration:none; transition:0.3s;"),
    A(id="nav_about", ctn_p="About", href="#about", style="color:white; text-decoration:none; transition:0.3s;"),
    A(id="nav_contact", ctn_p="Contact", href="#contact", style="color:white; text-decoration:none; transition:0.3s;")
)

# ------------------------------
# About Section
# ------------------------------
Section(
    id="about",
    style=(
        "padding:80px 20px; text-align:center; background:#f8f9fa; font-family:'Arial', sans-serif;"
    )
)
about(
    Div(id="about_text", ctn_p=(
        "We are a creative team building modern web experiences. "
        "Our mission is to craft engaging and beautiful designs for our clients."
    ), style="max-width:800px; margin:auto; font-size:1.2em; line-height:1.6; color:#333;")
)

# ------------------------------
# Portfolio / Featured images Section
# ------------------------------
Section(
    id="portfolio",
    style=(
        "padding:60px 20px; max-width:1200px; margin:auto; display:grid; "
        "grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px;"
    )
)
portfolio(
    Div(
        id="project1",
        ctn_p="Project 1",
        style=(
            "background:url('https://picsum.photos/400/250?random=1') center/cover no-repeat; "
            "height:250px; border-radius:10px; color:white; display:flex; align-items:flex-end; padding:10px; "
            "font-weight:bold; margin-top:10px;"
        )
    ),
    Div(
        id="project2",
        ctn_p="Project 2",
        style=(
            "background:url('https://picsum.photos/400/250?random=2') center/cover no-repeat; "
            "height:250px; border-radius:10px; color:white; display:flex; align-items:flex-end; padding:10px; "
            "font-weight:bold; margin-top:10px;"
        )
    ),
    Div(
        id="project3",
        ctn_p="Project 3",
        style=(
            "background:url('https://picsum.photos/400/250?random=3') center/cover no-repeat; "
            "height:250px; border-radius:10px; color:white; display:flex; align-items:flex-end; padding:10px; "
            "font-weight:bold; margin-top:10px;"
        )
    )
)

# ------------------------------
# Contact Section
# ------------------------------
Section(
    id="contact",
    style="padding:60px 20px; text-align:center; background:#222; color:white;"
)
contact(
    Div(id="contact_text", ctn_p="Get in touch with us: contact@example.com",
        style="font-size:1.2em;")
)

# ------------------------------
# Footer
# ------------------------------
Footer(
    id="footer",
    style="padding:25px 20px; background:#111; color:white; text-align:center;"
)
footer(
    Div(id="footer_text", ctn_p="© 2025 Professional Site. All rights reserved.")
)

# ------------------------------
# Generate document
# ------------------------------
doc.create_document()
