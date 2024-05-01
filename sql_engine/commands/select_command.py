from .sql_command import SqlCommand
from ..constants import DATA_PATH
from ..encoding.reader import ByteReader

class SelectCommand(SqlCommand):
    def __init__(self, columns, table):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table

    def execute(self):
        reader = ByteReader()
        table_data_path = DATA_PATH / self.table / 'data'
        values = reader.get_values(table_data_path)
        print(values)
