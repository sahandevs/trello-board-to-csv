
```sh
git clone https://github.com/SahandAkbarzadeh/trello-board-to-csv.git
cd trello-board-to-csv

Usage: run.py [OPTIONS]

Options:
  --trello_key TEXT       Trello key. generate here :
                          https://trello.com/1/appKey/generate
  --trello_secret TEXT    Trello Secret. generate here :
                          https://trello.com/1/appKey/generate
  --board_id TEXT         id of board to extract data from. obtain here :
                          https://trello.com/1/members/me?boards=all
  --out TEXT              export folder. default: ~/
  --delimiter TEXT        export delimiter. default: TAB
  --card_extractors TEXT  extractors : BaseData, CustomFields, TimeInList.
                          extractor with parameter example
                          --card_extractors="TimeInList('list_id_one'
                          'list_id_two')"
                           default :"BaseData, CustomFields,
                          TimeInList"
  --filters TEXT          filters. available filters:
                          Member('member_id' ...),
                          List('list_id' ...)
  --help                  Show this message and exit.



```

example

```sh
python run.py \ 
        --trello_key="<KEY>" \
        --trello_secret="<SECRET>" \
        --board_id="<ID>" \
        --out="~\export" \
        --card_extractors="BaseData, CustomFields, TimeInList('<LIST_ID>')" \
        --filters="Member('<MEMBER_ID>'), List('<LIST_ID>')"

```
