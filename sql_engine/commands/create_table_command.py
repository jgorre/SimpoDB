from .sql_command import SqlCommand
from ..constants import DATA_PATH
from ..data_serialization.schema import create_schema

class CreateTableCommand(SqlCommand):
    def __init__(self, table_name, columns):
        self.type = 'CREATE_TABLE'
        self.table_name = table_name
        self.columns = columns


    def execute(self):
        create_schema(self.table_name, self._schema())


    def _schema(self):
        return {
            "table_name": self.table_name,
            "columns": [{
                "name": column_name,
                "type": column_type.upper()
            } for column_name, column_type in self.columns]
        }