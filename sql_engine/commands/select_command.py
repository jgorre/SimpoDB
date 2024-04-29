class SelectCommand:
    def __init__(self, columns, table):
        self.type = 'SELECT'
        self.columns = columns
        self.table = table