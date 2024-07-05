import click
from datetime import datetime
import os
from pathlib import Path
import yaml
from fpdf import FPDF
import ttf_opensans


@click.command()
@click.argument('yaml_path', type=click.Path(exists=True))
def parse_yaml(yaml_path):
    """easyletter makes writing letters easy!"""
    try:
        with open(yaml_path, 'r') as file:
            document = yaml.safe_load(file)

            pdf = FPDF(format='A4')
            pdf.add_page()
            
            font_size = 12
            line_height = font_size / 2
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
            pdf.set_font(font_name, size=8)
            pdf.set_y(45)        
            pdf.cell(
                text=formatted_sender,
                w=85
            )
            
            recipient = document.get('address').get('recipient')
            pdf.set_font(font_name, size=font_size)
            pdf.set_y(50)
            pdf.multi_cell(
                text=recipient,
                w=85,
                h=line_height
            )
            
            location = document.get('location')
            formatted_date = datetime.now().strftime("%d.%m.%Y")
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
                w=0
            )
            
            ending_defined = document.get('ending')
            ending = ending_defined if ending_defined is None else "Beste Grüße"
            pdf.set_y(pdf.get_y() + 15)
            pdf.cell(text=ending)
            
            signature_name = sender_fragments[0]
            pdf.set_y(pdf.get_y() + 30)
            pdf.cell(text=signature_name)
            
            contact_email = document.get('contact').get('email')
            contact_phone = document.get('contact').get('phone')
            contact = f"E-Mail: {contact_email} • Telefon: {contact_phone}"
            pdf.set_y(-25)
            pdf.set_font(font_name, size=10)
            pdf.cell(
                text=contact,
                align='C',
                w=0
            )
            
            pdf_base_file_name=Path(yaml_path).stem
            pdf_dir="out"
            Path(pdf_dir).mkdir(parents=True, exist_ok=True)
            pdf_path = f"{pdf_dir}/{pdf_base_file_name}.pdf"
            pdf.output(pdf_path)

            print(f"Created letter at file://{os.getcwd()}/{pdf_path}")
            
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

if __name__ == '__main__':
    parse_yaml()
