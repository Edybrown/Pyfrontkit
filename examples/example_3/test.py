from pyfrontkit  import HtmlDoc, div, a, header, footer,img, CreateFont

doc=HtmlDoc(title="test page")

header(id="top" ).form(height="60px",color="grey",background="black").border("1px","solid","grey").align("row","250px",pad_left="30px")
top(div(id="left").align("column",pad_top="16px"),
    div(id="center").align("row","30px",fsize="16px",text_align="center").form("600px"),
    div(id="right").align("row",'50px',padding="15px",pad_left="20px").form("240px","40px")
    )

left(img(src="https://framerusercontent.com/images/PBIA94m8cLTqDKOMY36HE98A4U.svg",width="107px",height="27px"))

center(a(class_="home", ctn_p="Home").form(color="#a5e12d").align('column', pad_top="22px"),
       a(class_="button", ctn_p="Problems").form("80px","40px").hover("#a5e12d").align('column', pad_top="22px"),
       a(class_="button",ctn_p="Solution"),
       a(class_="button", ctn_p='Pricing'),
       a(class_="button", ctn_p="Blog"),
       a(class_="button",ctn_p="Affiliate"))

right(a(ctn_p="Login",class_="begin",id="log").form(color="black",background="#a5e12d").hover('white',"rgb(47,47,50)"),
      a(ctn_p="Sign up",class_="begin").align("column",pad_top="6px",text_align="center").form("80px","26px","20px","rgb(47,47,50)","white").hover("#a5e12d")
        )


div(id="content").form("1532px","630px",background="url(back.jpg)",color="grey").align("column","30px",pad_top= "100px")
content(div(ctn_strong="Unlock the Power of Linear\nOne Board, One URL").form(color="white").align("column",text_align="center",fsize="60px"),
        div(ctn_p='''Convert Linear's data into a Public/Private board - share with \n stakeholders via a single, easy-to-use URL. Achieve ultimate
                        efficiency and transparency today!''').align("column",text_align="center",fsize="21px").form(color="rgb(207, 207, 207)"),
        a(ctn_p="Login").hover('white',"rgb(47,47,50)").margin(left="700px").form("88px","28px","25px","#a5e12d","black").align('column',pad_top="10px",text_align="center")
)
footer(ctn_p="""© 2025 PyFrontKit. All rights reserved.  
                   Proudly built with PyFrontKit.""").form("1532px","80px",color="#a5e12d",background="rgba(40, 40, 40, 0.35)").position("710px")
doc.create_document()
CreateFont("Ebrima")
