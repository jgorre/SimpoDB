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

    # To do the find a value magic
    # Need to set up where clause functionality
        # for now, assume search is on the index
        # where indentifier = string or num
    # Select command should have a clever data object
    # specifying what the constraints are. key indentifier pairs
        # Again, assume identifier is the index for now.
        # Also assume we are not doing a range query,
        # rather we are looking only for a single entity.
    # Then we check the memtable for the key. If exists, return entity.
    # If not exists, check the latest sstable
        # But maybe we should have the sparse in memory hash table per sstable
        # Bloom filter later
        # SSTable should have sparse in-memory hashmap per index.