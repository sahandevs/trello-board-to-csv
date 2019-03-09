from trello import Card
from typing import Dict


class DataExtractor:
    card: Card

    @property
    def category(self):
        return "default_card_data"

    def __init__(self, card: Card):
        self.card = card

    def extract(self) -> Dict[str, str]:
        pass
