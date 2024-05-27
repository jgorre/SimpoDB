from .sql_command import SqlCommand
from ..data_serialization.schema import SchemaManager

class CreateTableCommand(SqlCommand):
    def __init__(self, table_name, columns, primary_key):
        self.type = 'CREATE_TABLE'
        self.table_name = table_name
        self.columns = columns
        self.primary_key = primary_key
        
        self.schema_manager = SchemaManager()


    def execute(self):
        self.schema_manager.create_schema(self.table_name, self._schema())


    def _schema(self):
        return {
            0: {
                "columns": [{
                    "name": column_name,
                    "type": column_type.upper(),
                    "attributes": attributes
                } for column_name, column_type, attributes in self.columns],
                "primary_key": self.primary_key
            }
        }