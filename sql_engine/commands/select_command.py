from .sql_command import SqlCommand
from ..storage.storage import TableStorage
from ..data_serialization.schema import SchemaManager

class SelectCommand(SqlCommand):
    def __init__(self, columns, table, where_condition=None):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table
        self.table_storage = TableStorage()
        self.where_condition = where_condition

        self.schema_manager = SchemaManager()

    def execute(self):
        if self.where_condition is None:
            self.table_storage.read_all(self.table)
        elif self._is_search_condition_on_index():
            indexed_column = self.where_condition[0]
            search_value = self.where_condition[1]
            self.table_storage.read_entity_from_index(self.table, indexed_column, search_value)
        else:
            raise NotImplementedError('Search criteria did not match known pattern.')

        # Bloom filter later

    def _is_search_condition_on_index(self):
        return self.where_condition[0] == self.schema_manager.get_primary_key_column_for_table(self.table)