from trello import Board
from typing import Dict


class DataExtractor:
    board: Board

    @property
    def category(self):
        return "default_board_data"

    def __init__(self, board: Board):
        self.board = board

    def extract(self) -> Dict[str, str]:
        pass
