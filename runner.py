from data_provider import DataProvider
from database import DataBase
from data_extractors.card_data_extractor.__index__ import __extractors__ as card_extractors


class Runner:
    provider: DataProvider
    database: DataBase

    def __init__(self, provider: DataProvider, database: DataBase):
        self.provider = provider
        self.database = database

    def run(self):
        self.run_card_extractors()

    def run_card_extractors(self):
        for card in self.provider.board.all_cards():
            data = {}
            for extractor in card_extractors:
                extractor_instance = extractor(card)
                if not data.get(extractor_instance.category):
                    data[extractor_instance.category] = {}
                data[extractor_instance.category].update(extractor_instance.extract())
            for item in data:
                self.database.add_data(data[item], item)
