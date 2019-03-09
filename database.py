from typing import List, Dict
from pprint import pprint
import csv
import os
from datetime import datetime


class CategoryData:
    name: str

    data: List[Dict[str, str]]

    def __init__(self, name):
        self.name = name
        self.data = []

    def add_data(self, data: Dict[str, str]):
        self.data.append(data)

    def to_sheet(self) -> Dict[str, List[str]]:
        sheet: Dict[str, List[str]] = dict()

        for item in self.data:
            # add each data to each col
            for key in item:
                if not sheet.get(key):
                    sheet[key] = []
                sheet[key].append(item[key])
            # add padding for empty cells
            max_col_size = max(len(sheet[col]) for col in sheet)
            for col in sheet:
                for _ in range(max(0, max_col_size - len(sheet[col]))):
                    sheet[col].append("")  # padding

        return sheet


class DataBase:
    categories: List[CategoryData]

    def __init__(self):
        self.categories = []

    def add_category(self, name) -> CategoryData:
        category = CategoryData(name)
        self.categories.append(category)
        return category

    def add_data(self, data: Dict[str, str], category: str):
        for cat in self.categories:
            if cat.name == category:
                cat.add_data(data)
                return
        self.add_category(category).add_data(data)

    def pprint(self):
        data = []
        for category in self.categories:
            data.append(category.to_sheet())
        pprint(data)

    def export(self, folder):
        for category in self.categories:
            with open(
                    os.path.join(folder, '{0}-{1}.csv'.format(category.name, datetime.now().timestamp())),
                    'w',
                    newline='',
                    encoding='utf-8'
            ) as file:
                headers = []
                for data in category.data:
                    headers += [x for x in data]
                writer = csv.DictWriter(
                    file,
                    delimiter="\t",
                    fieldnames=list(set(headers)),
                    quoting=csv.QUOTE_ALL,
                )
                writer.writeheader()
                writer.writerows(category.data)
