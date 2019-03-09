import trello
from typing import Dict


class DataExtractor:
    list: trello.List

    @property
    def category(self):
        return "default_list_data"

    def __init__(self, trello_list: trello.List):
        self.list = trello_list

    def extract(self) -> Dict[str, str]:
        pass
