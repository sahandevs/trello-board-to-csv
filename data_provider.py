import trello as t


class DataProvider:
    board: t.Board

    def __init__(self, board: t.Board):
        self.board = board
        self.board.fetch()
