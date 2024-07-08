import ttf_opensans
import locale
from fpdf import FPDF
from datetime import datetime
from letter import Letter

DEFAULT_FONT_SIZE = 11
LINE_HEIGHT = DEFAULT_FONT_SIZE / 2
FONT_NAME = 'open-sans'

def create_pdf(letter: Letter) -> FPDF:
    pdf = init_pdf()
    add_address_window(pdf, letter)
    add_contact(pdf, letter)
    add_body(pdf, letter)
    return pdf

def init_pdf() -> FPDF:
    pdf = FPDF(format='A4')
    pdf.add_page()

    pdf.set_margin(20)
    
    pdf.add_font(
        family=FONT_NAME,
        style="",
        fname=ttf_opensans.OPENSANS_REGULAR.path
    )
    pdf.add_font(
        family=FONT_NAME,
        style="b",
        fname=ttf_opensans.OPENSANS_BOLD.path
    )
    pdf.add_font(
        family=FONT_NAME,
        style="i",
        fname=ttf_opensans.OPENSANS_ITALIC.path
    )
    pdf.set_font(FONT_NAME)

    add_folding_marks(pdf)
    return pdf

def add_folding_marks(pdf: FPDF):
    pdf.line(5, 95, 7, 95)
    pdf.line(5, 200, 7, 200)

def add_address_window(pdf: FPDF, letter: Letter):
    formatted_sender = " • ".join(letter.sender_lines())
    pdf.set_font_size(6)
    pdf.set_y(45)
    pdf.cell(
        text=formatted_sender,
        w=85
    )
    
    pdf.set_font_size(DEFAULT_FONT_SIZE)
    pdf.set_y(50)
    pdf.multi_cell(
        text=letter.recipient,
        w=85,
        h=LINE_HEIGHT
    )

def add_contact(pdf: FPDF, letter: Letter):
    contact_items = [f"{key}: {value}" for key, value in letter.contact.items()]
    formatted_contact="\n".join(contact_items)

    contact = f"""
    {letter.sender}

    {formatted_contact}
    """
    pdf.set_xy(-110, 35)
    pdf.set_font_size(9)
    pdf.multi_cell(
        text=contact,
        align='R',
        w=90,
        h=4.5
    )

def add_body(pdf: FPDF, letter: Letter):
    pdf.set_font_size(DEFAULT_FONT_SIZE)

    configure_locale(letter.locale)
    formatted_date = datetime.now().strftime('%x')
    pdf.set_y(100)
    pdf.cell(
        text=f"__{letter.location}, {formatted_date}__",
        align='R',
        markdown=True,
        w=0
    )
    
    pdf.set_y(120)
    pdf.cell(
        text=f"**{letter.subject}**",
        markdown=True
    )
    
    pdf.set_y(140)
    pdf.multi_cell(
        text=letter.content,
        markdown=True,
        w=0,
        h=LINE_HEIGHT
    )
    
    if letter.ending is not None:
        pdf.set_y(pdf.get_y() + 15)
        pdf.cell(text=letter.ending)
        
        pdf.set_y(pdf.get_y() + 30)
        pdf.cell(text=letter.sender_name())

def configure_locale(defined_locale: str):
    if defined_locale is None:
        locale.setlocale(locale.LC_TIME, '')
    else:
        locale.setlocale(locale.LC_TIME, locale=f"{defined_locale}.UTF-8")
