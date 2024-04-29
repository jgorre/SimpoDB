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