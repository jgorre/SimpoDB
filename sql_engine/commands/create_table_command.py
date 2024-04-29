import json

from .sql_command import SqlCommand
from ..constants import DATA_PATH

class CreateTableCommand(SqlCommand):
    def __init__(self, table_name, columns):
        self.type = 'CREATE_TABLE'
        self.table_name = table_name
        self.columns = columns


    def execute(self):
        new_folder_path = DATA_PATH / self.table_name

        if new_folder_path.exists():
            print(f"Table '{self.table_name}' already exists.")
            return

        new_folder_path.mkdir(parents=True, exist_ok=False)

        schema_file_path = new_folder_path / "schema.json"
        with open(schema_file_path, "w") as schema_file:
            json.dump(self._schema(), schema_file, indent=4)


    def _schema(self):
        return {
            "table_name": self.table_name,
            "columns": [{
                "name": column_name,
                "type": column_type.upper()
            } for column_name, column_type in self.columns]
        }