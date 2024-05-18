from dataclasses import dataclass

@dataclass
class DataForInsert:
    data: list
    schema_version: int
    primary_key_index: int

    def to_dict(self):
        return {
            "data": self.data,
            "schema_version": self.schema_version,
            "primary_key_index": self.primary_key_index
        }
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            data=data_dict["data"],
            schema_version=data_dict["schema_version"],
            primary_key_index=data_dict["primary_key_index"]
        )