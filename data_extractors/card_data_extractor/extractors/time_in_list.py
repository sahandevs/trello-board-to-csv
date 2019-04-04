from typing import Dict, List
from ..base import DataExtractor
from .base_data import BaseData
import moment
from datetime import datetime
import trello
from time import sleep


class MoveActions:
    from_list_name: str
    to_list_name: str
    date: str

    def __init__(self, from_list, to_list, date):
        self.from_list_name = from_list
        self.to_list_name = to_list
        self.date = date


class TimeInList(DataExtractor):

    @property
    def category(self):
        return "base"

    def get_data(self):
        try:
            return self.card.fetch_actions(action_filter="createCard,updateCard")
        except:
            print("retry")
            sleep(5)
            return self.get_data()

    def extract(self) -> Dict[str, str]:
        raw_actions: List[Dict] = self.get_data()
        raw_actions.reverse()
        actions: List[MoveActions] = []
        # serialize move actions
        for action in raw_actions:
            if action["type"] == "createCard":
                actions.append(MoveActions(None, action["data"]["list"].get("id"),
                                           action["date"]))
            elif action["type"] == "updateCard" and action["data"].get("listBefore"):
                actions.append(MoveActions(action["data"]["listBefore"]["id"],
                                           action["data"]["listAfter"]["id"],
                                           action["date"]))
        if len(actions) == 0 or raw_actions[0]["type"] != "createCard":
            return {}
        # calculate time in each list ( in hours )
        calculated_time: Dict[str, int] = dict()
        for (index, action) in enumerate(actions):
            if index == 0:
                continue
            if not calculated_time.get(action.from_list_name):
                calculated_time[action.from_list_name] = 0
            from_date = moment.date(actions[index - 1].date).datetime
            to_date = moment.date(action.date).datetime
            total = to_date - from_date
            calculated_time[action.from_list_name] += total.total_seconds() / (60 * 60)
        # last list time
        action = actions[-1] if len(actions) > 1 else actions[0]
        if not calculated_time.get(action.to_list_name):
            calculated_time[action.to_list_name] = 0
        from_date = moment.date(action.date).datetime
        to_date = datetime.now().replace(tzinfo=from_date.tzinfo)
        total = to_date - from_date
        calculated_time[action.to_list_name] += total.total_seconds() / (60 * 60)
        data = dict()
        for item in calculated_time:
            if len(self.arguments) > 0 and item not in self.arguments:
                continue
            data["time in {0}".format(
                BaseData.idList_to_List_map.get(
                    item,
                    trello.List(
                        name=item,
                        list_id=item,
                        board=self.card.board)
                ).name)] = '{0} h'.format(calculated_time[item]) \
                if calculated_time[item] < 24 else \
                '{0} d'.format(calculated_time[item] // 24)
        return data
