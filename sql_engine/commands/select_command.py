from .sql_command import SqlCommand
from ..data_serialization.reader import ByteReader

class SelectCommand(SqlCommand):
    def __init__(self, columns, table):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table

    def execute(self):
        reader = ByteReader()
        # where_condition = lambda row: row[1] == 'jakobsson'
        # values = reader.get_values(self.table, where_condition)
        values = reader.get_values(self.table)
        print(values)
