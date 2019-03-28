from config import *
from trello import Board, TrelloClient
from data_provider import DataProvider
from database import DataBase
from runner import Runner


def main():
    trello_client = TrelloClient(
        api_key=TRELLO_KEY,
        api_secret=TRELLO_SECRET,
    )
    data_provider = DataProvider(
        Board(
            trello_client,
            board_id=BOARD_ID,
        )
    )
    database = DataBase()
    runner = Runner(data_provider, database)
    runner.run()
    database.export(OUT)


if __name__ == "__main__":
    main()
