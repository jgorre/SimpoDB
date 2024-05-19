from .sql_command import SqlCommand
from ..storage.storage import TableStorage

class SelectCommand(SqlCommand):
    def __init__(self, columns, table):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table

    def execute(self):
        storage = TableStorage()
        storage.read(self.table)