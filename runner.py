from trello import Card

from data_provider import DataProvider
from database import DataBase
from data_extractors.card_data_extractor.__index__ import __extractors__ as card_extractors
from typing import List

from parameter_parser import Parameter


class Runner:
    provider: DataProvider
    database: DataBase
    card_extractors: List[Parameter]
    filters: List[Parameter]

    def __init__(self, provider: DataProvider, database: DataBase, card_extractors_parameter: List[Parameter],
                 filters: List[Parameter]):
        self.provider = provider
        self.database = database
        self.card_extractors = card_extractors_parameter
        self.filters = filters

    def run(self):
        self.run_card_extractors()

    def get_cards(self) -> List[Card]:
        cards = self.provider.board.all_cards()
        for _filter in self.filters:
            if _filter.name == 'Member' and len(_filter.arguments) > 0:
                cards = [x for x in cards if all([member in x.idMembers for member in _filter.arguments])]
            if _filter.name == 'List' and len(_filter.arguments) > 0:
                cards = [x for x in cards if all([idList == x.list_id for idList in _filter.arguments])]
        return cards

    def run_card_extractors(self):
        for card in self.get_cards():
            data = {}
            for extractor in [x for x in card_extractors if
                              x.__name__ in [parameter.name for parameter in self.card_extractors]]:
                extractor_instance = extractor(card)
                parameter = [par for par in self.card_extractors if par.name == extractor.__name__][0]
                extractor_instance.arguments = parameter.arguments
                if not data.get(extractor_instance.category):
                    data[extractor_instance.category] = {}
                data[extractor_instance.category].update(extractor_instance.extract())
            for item in data:
                self.database.add_data(data[item], item)
