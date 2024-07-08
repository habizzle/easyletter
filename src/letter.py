from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Letter:
    sender: str
    recipient: str
    contact: Dict[str, str]
    location: str
    subject: str
    content: str
    ending: str
    locale: str

    def sender_name(self) -> str:
        return self.sender_lines()[0]

    def sender_lines(self) -> List[str]:
        return self.sender.splitlines()
