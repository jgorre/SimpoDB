from dataclasses import dataclass

@dataclass
class Entity:
    schema_version: int
    key_name: object
    data: dict

    def get_key_value(self):
        return self.data[self.key_name]


