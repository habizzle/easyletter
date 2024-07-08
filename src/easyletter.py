import click
import os
from pathlib import Path
from parser import parse_letter
from pdf_creator import create_pdf

@click.command()
@click.argument('yaml_path', type=click.Path(exists=True))
def write_letter(yaml_path):
    """Convert the provided YAML file to a PDF letter"""

    letter = parse_letter(yaml_path)

    pdf = create_pdf(letter)
    pdf_path = output_path(yaml_path)
    pdf.output(pdf_path)

    print(f"Created letter at file://{os.getcwd()}/{pdf_path}")

def output_path(input_path) -> str:
    pdf_base_file_name=Path(input_path).stem
    pdf_dir="out"
    Path(pdf_dir).mkdir(parents=True, exist_ok=True)
    return f"{pdf_dir}/{pdf_base_file_name}.pdf"

if __name__ == '__main__':
    write_letter()
