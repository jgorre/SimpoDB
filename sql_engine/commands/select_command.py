from .sql_command import SqlCommand
from ..storage.storage import TableStorage

class SelectCommand(SqlCommand):
    def __init__(self, columns, table, where_condition=None):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table
        self.table_storage = TableStorage()
        self.where_condition = where_condition

    def execute(self):
        if self.where_condition is None:
            self.table_storage.read_all(self.table)
        else:
            self.table_storage.read_entity(self.table, self.where_condition)

        # Need to implement sparse in memory hash table per sstable
        # Bloom filter later
        # SSTable should have sparse in-memory hashmap per index.