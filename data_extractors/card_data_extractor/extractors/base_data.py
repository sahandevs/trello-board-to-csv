from typing import Dict
import trello
from ..base import DataExtractor
from datetime import datetime, timezone


class BaseData(DataExtractor):

    @property
    def category(self):
        return "base"

    def prepare(self):
        # cache board lists
        if not BaseData.board_lists:
            BaseData.board_lists = self.card.board.all_lists()
            for list_item in BaseData.board_lists:
                BaseData.idList_to_List_map[list_item.id] = list_item
        # cache members
        if not BaseData.board_members:
            BaseData.board_members = self.card.board.all_members()
            for member in BaseData.board_members:
                BaseData.idMember_to_Member_map[member.id] = member

    def extract(self) -> Dict[str, str]:
        self.prepare()
        data = dict()
        data["card name"] = self.card.name
        data["labels"] = ', '.join([x.name for x in self.card.labels or []])
        data["members"] = ', '.join([BaseData.idMember_to_Member_map[x].username for x in self.card.idMembers])
        data["last activity"] = str(self.card.dateLastActivity)
        data["created date"] = str(self.card.created_date)
        data["due date"] = str(self.card.due_date)
        data['age'] = '~ {0} d'.format(
            str((datetime.now(tz=timezone.utc) - self.card.created_date).total_seconds() // (60 * 60 * 24)))
        # data["description"] = self.card.desc or ""
        data["current list"] = BaseData.idList_to_List_map[self.card.idList].name
        return data


BaseData.board_lists = None
BaseData.idList_to_List_map: Dict[str, trello.List] = {}
BaseData.board_members = None
BaseData.idMember_to_Member_map: Dict[str, trello.Member] = {}
