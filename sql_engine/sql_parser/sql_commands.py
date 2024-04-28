class SelectCommand:
    def __init__(self, columns, table):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table


class CreateTableCommand:
    def __init__(self, table_name, columns):
        self.type = 'CREATE_TABLE'
        self.table_name = table_name
        self.columns = columns

    def schema(self):
        return {
            "table_name": self.table_name,
            "columns": [{
                "name": column_name,
                "type": column_type.upper()
            } for column_name, column_type in self.columns]
        }

class InsertCommand:
    def __init__(self, table, columns, values):
        self.type = 'INSERT'
        self.table = table
        self.columns = columns
        self.values = values

