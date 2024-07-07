import click
from datetime import datetime
import os
from pathlib import Path
import yaml
from fpdf import FPDF
import ttf_opensans
import locale


DEFAULT_FONT_SIZE = 12

@click.command()
@click.argument('yaml_path', type=click.Path(exists=True))
def write_letter(yaml_path):
    """Convert the provided YAML file to a PDF letter"""
    try:
        with open(yaml_path, 'r') as file:
            document = yaml.safe_load(file)
            pdf = create_pdf(document)
            pdf_path = output_path(yaml_path)
            pdf.output(pdf_path)
            print(f"Created letter at file://{os.getcwd()}/{pdf_path}")
            
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")    

def create_pdf(document) -> FPDF:
    pdf = FPDF(format='A4')
    pdf.add_page()
    
    line_height = DEFAULT_FONT_SIZE / 2
    font_name = 'open-sans'
    pdf.add_font(
        family=font_name,
        style="",
        fname=ttf_opensans.OPENSANS_REGULAR.path
    )
    pdf.add_font(
        family=font_name,
        style="b",
        fname=ttf_opensans.OPENSANS_BOLD.path
    )
    pdf.add_font(
        family=font_name,
        style="i",
        fname=ttf_opensans.OPENSANS_ITALIC.path
    )
    
    sender_block = f"{document.get('address').get('sender')}"
    sender_fragments = sender_block.splitlines()
    formatted_sender = " • ".join(sender_fragments)
    pdf.set_font(font_name, size=6)
    pdf.set_y(45)        
    pdf.cell(
        text=formatted_sender,
        w=85
    )
    
    recipient = document.get('address').get('recipient')
    pdf.set_font(font_name, size=DEFAULT_FONT_SIZE)
    pdf.set_y(50)
    pdf.multi_cell(
        text=recipient,
        w=85,
        h=line_height
    )
    
    location = document.get('location')
    configure_locale(document)
    formatted_date = datetime.now().strftime('%x')
    pdf.set_y(100)
    pdf.cell(
        text=f"__{location}, den {formatted_date}__",
        align='R',
        markdown=True,
        w=0
    )
    
    subject = document.get('subject')            
    pdf.set_y(120)
    pdf.cell(
        text=f"**{subject}**",
        markdown=True
    )
    
    content = document.get('content')
    pdf.set_y(140)
    pdf.multi_cell(
        text=content,
        markdown=True,
        w=0,
        h=line_height
    )
    
    ending = document.get('ending')
    if ending is not None:
        pdf.set_y(pdf.get_y() + 15)
        pdf.cell(text=ending)
        
        signature_name = sender_fragments[0]
        pdf.set_y(pdf.get_y() + 30)
        pdf.cell(text=signature_name)
    
    contact = document.get('contact')
    contact_items = []
    for key, value in contact.items():
        contact_items.append(f"{key}: {value}")
    formatted_contact="\n".join(contact_items)
    
    contact = f"""
    {sender_block}
    
    {formatted_contact}
    """
    pdf.set_xy(-100, 25)
    pdf.set_font(font_name, size=10)
    pdf.multi_cell(
        text=contact,
        align='R',
        w=90,
        h=5
    )
    
    # for folding
    pdf.set_xy(5, 105)
    pdf.cell(text="-")
    pdf.set_xy(5, 210)
    pdf.cell(text="-")
    
    return pdf

def configure_locale(document):
    defined_locale = document.get('locale')
    if defined_locale is None:
        locale.setlocale(locale.LC_TIME, '')
    else:
        locale.setlocale(locale.LC_TIME, locale=f"{defined_locale}.UTF-8")

def output_path(input_path) -> str:
    pdf_base_file_name=Path(input_path).stem
    pdf_dir="out"
    Path(pdf_dir).mkdir(parents=True, exist_ok=True)
    return f"{pdf_dir}/{pdf_base_file_name}.pdf"

if __name__ == '__main__':
    write_letter()
