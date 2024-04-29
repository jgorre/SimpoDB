from .sql_command import SqlCommand

class SelectCommand(SqlCommand):
    def __init__(self, columns, table):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table

    def execute(self):
        print("You did a select!")