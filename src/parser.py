import yaml
from letter import *

def parse_letter(yaml_path) -> Letter:
    with open(yaml_path, 'r') as file:
        document = yaml.safe_load(file)

        return Letter(
            sender=document.get('sender'),
            recipient=document.get('recipient'),
            contact=document.get('contact', {}),
            location=document.get('location'),
            subject=document.get('subject'),
            content=document.get('content'),
            ending=document.get('ending'),
            locale=document.get('locale')
        )
