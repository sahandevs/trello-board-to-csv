from trello import Card
from typing import Dict, List


class DataExtractor:
    card: Card
    arguments: List[str]

    @property
    def category(self):
        return "default_card_data"

    def __init__(self, card: Card):
        self.card = card

    def extract(self) -> Dict[str, str]:
        pass

    @classmethod
    def __name__(cls):
        return cls.__class__.__name__
