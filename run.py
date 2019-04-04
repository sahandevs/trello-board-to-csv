import click
from trello import Board, TrelloClient
from data_provider import DataProvider
from database import DataBase
from runner import Runner
from data_extractors.card_data_extractor.__index__ import __extractors__ as card_extractors_all
from filters.__index__ import __filters__ as filters
from parameter_parser import Parameter

CARD_EXTRACTORS = ', '.join([x.__name__ for x in card_extractors_all])
FILTERS = ', '.join([x.__name__ for x in filters])


@click.command()
@click.option('--trello_key', help='Trello key. generate here : https://trello.com/1/appKey/generate')
@click.option('--trello_secret', help='Trello Secret. generate here : https://trello.com/1/appKey/generate')
@click.option('--board_id',
              help='id of board to extract data from. obtain here : https://trello.com/1/members/me?boards=all')
@click.option('--out', default='~/', help='export folder. default: ~/')
@click.option('--delimiter', default='\t', help='export delimiter. default: TAB')
@click.option('--card_extractors', default=CARD_EXTRACTORS,
              help=('extractors : {0}.\nextractor with parameter example\n--card'
                    '_extractors="TimeInList(\'list_id_one\' '
                    '\'list_id_two\')"\n default :"{0}"').format(CARD_EXTRACTORS))
@click.option('--filters', help='filters. available filters:\n{0}'.format(FILTERS))
def setup(trello_key, trello_secret, board_id, out, delimiter, card_extractors, filters):
    # validate inputs

    if not trello_key or not trello_secret:
        raise click.BadParameter('trello_secret and trello_key are required')

    if not board_id:
        raise click.BadParameter('board_id is required')

    trello_client = TrelloClient(
        api_key=trello_key,
        api_secret=trello_secret,
    )
    data_provider = DataProvider(
        Board(
            trello_client,
            board_id=board_id,
        )
    )
    database = DataBase(delimiter=delimiter)
    runner = Runner(data_provider, database,
                    card_extractors_parameter=[Parameter(x.strip()) for x in card_extractors.split(',')],
                    filters=[Parameter(x.strip()) for x in filters.split(',')] if filters else [])
    runner.run()
    database.export(out)


if __name__ == "__main__":
    setup()
