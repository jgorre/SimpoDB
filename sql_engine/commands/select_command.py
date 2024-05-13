from .sql_command import SqlCommand
from ..data_serialization.reader import ByteReader
from ..storage.storage import TableStorage

class SelectCommand(SqlCommand):
    def __init__(self, columns, table):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table

    def execute(self):
        storage = TableStorage()
        print(storage.get_memtable('persons').keys())
