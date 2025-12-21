from pydoc import html
import sys
from ppg_runtime.application_context.PySide6 import ApplicationContext
from ppg_runtime.application_context import PPGLifeCycle, Pydux, init_lifecycle
from ppg_runtime.application_context.devtools.reloader import hot_reloading
from ppg_runtime.application_context.utils import app_is_frozen
from PySide6.QtWidgets import QMainWindow, QLabel
from pyfrontkit import HtmlDoc, css, div, a, header, footer, img

# --------------------------------------------------------------------------------------
# Important! Production Considerations for Hot Reloading
# --------------------------------------------------------------------------------------
# Hot reloading is a development tool that allows you to instantly see UI changes
# when you save a file. It's extremely useful for rapid prototyping and designing
# interfaces.
#
# However, this functionality is not designed for use in production environments.
# For the final version of your application, it is highly recommended to remove
# the code related to hot reloading, such as the `@hot_reloading` decorator
# and the `window._init_hot_reload_system(__file__)` call.
#
# Keeping hot reloading active in production can negatively impact the application's
# performance, stability, and security.
# --------------------------------------------------------------------------------------
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


@init_lifecycle
@hot_reloading
class PpgIntegration(QMainWindow, PPGLifeCycle, Pydux):

    def generate_ui(self):
        self.doc = HtmlDoc(title="test page")
        self.doc = HtmlDoc(title="test page")
        header(id="top").form(height="60px", color="grey", background="black").border(
            "1px", "solid", "grey").align("row", "250px", pad_left="30px")
        top(
            div(id="left").align("column", pad_top="16px"),
            div(id="center").align("row", "30px", fsize="16px",
                                   text_align="center").form("600px"),
            div(id="right").align("row", '50px', padding="15px",
                                  pad_left="20px").form("240px", "40px")
        )

        left(
            img(src="https://framerusercontent.com/images/PBIA94m8cLTqDKOMY36HE98A4U.svg",
                width="107px", height="27px")
        )

        center(
            a(class_="home", ctn_p="Home").form(
                color="#a5e12d").align('column', pad_top="22px"),
            a(class_="button", ctn_p="Problems").form("80px", "40px").hover(
                "#a5e12d").align('column', pad_top="22px"),
            a(class_="button", ctn_p="Solution"),
            a(class_="button", ctn_p='Pricing'),
            a(class_="button", ctn_p="Blog"),
            a(class_="button", ctn_p="Affiliate")
        )

        right(
            a(ctn_p="Login", class_="begin", id="log").form(
                color="black", background="#a5e12d").hover('white', "rgb(47,47,50)"),
            a(ctn_p="Sign up", class_="begin").align("column", pad_top="6px", text_align="center").form(
                "80px", "26px", "20px", "rgb(47,47,50)", "white").hover("#a5e12d")
        )

        div(id="content").form("1532px", "630px", background="url(back.jpg)",
                               color="grey").align("column", "30px", pad_top="100px")
        content(
            div(ctn_strong="Unlock the Power of Linear\nOne Board, One URL").form(
                color="white").align("column", text_align="center", fsize="60px"),
            div(ctn_p='''Convert Linear's data into a Public/Private board - share with \n stakeholders via a single, easy-to-use URL. Achieve ultimate
                efficiency and transparency today!''').align("column", text_align="center", fsize="21px").form(color="rgb(207, 207, 207)"),
            a(ctn_p="Login").hover('white', "rgb(47,47,50)").margin(left="700px").form(
                "88px", "28px", "25px", "#a5e12d", "black").align('column', pad_top="10px", text_align="center")
        )
        footer(ctn_p="""© 2025 PyFrontKit. All rights reserved.  
                   Proudly built with PyFrontKit.""").form("1532px", "80px", color="#a5e12d", background="rgba(40, 40, 40, 0.35)").position("710px")

        self.document = self.doc.bundle_document(
            output="raw"
        )

    def component_will_mount(self):
        self.subscribe_to_store(self)
        self.generate_ui()

    def render_(self):
        self.engine = QWebEngineView(self)
        self.engine.setHtml(self.document, QUrl(""))

        self.setCentralWidget(self.engine)

    def responsive_UI(self):
        self.setMinimumSize(640, 480)


if __name__ == '__main__':
    appctxt = ApplicationContext()
    window = PpgIntegration()
    if not app_is_frozen():
        window._init_hot_reload_system(__file__)
    window.show()
    exec_func = getattr(appctxt.app, 'exec', appctxt.app.exec_)
    sys.exit(exec_func())
