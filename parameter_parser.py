from typing import List
import re


class Parameter:
    name: str
    arguments: List[str]

    def __init__(self, parameter: str):
        # TODO: add real validation with regex
        if '(' in parameter:
            self.name = parameter.split('(')[0]
            self.arguments = [x.group().strip("\'") for x in re.finditer(r"'[\w\W]*?'", parameter)]
        else:
            self.name = parameter
            self.arguments = []
