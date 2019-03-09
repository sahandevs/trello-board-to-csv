from typing import Dict
from ..base import DataExtractor


class CustomFields(DataExtractor):

    @property
    def category(self):
        return "base"

    def prepare(self):
        # cache custom field values
        if not CustomFields.valueId_to_value_map:
            for definition in self.card.board.get_custom_field_definitions():
                CustomFields.valueId_to_value_map.update(definition.list_options)

    def extract(self) -> Dict[str, str]:
        self.prepare()
        data = dict()
        for field in self.card.customFields:
            value = str(field._value).strip() if field._value is not None else ""
            data[field.name.strip()] = CustomFields.valueId_to_value_map.get(value) or value
        return data


CustomFields.valueId_to_value_map = {}
