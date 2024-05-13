from sortedcontainers import SortedDict

class TableStorage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TableStorage, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if not self.initialized:
            self.memtables = {}
            self.initialized = True

    def write_data_to_table(self, table: str, data: list[list]):
        if table not in self.memtables.keys():
            self._add_memtable(table)

        memtable = self._get_memtable(table)
        # memtable.

    # Memtable shouldn't need to be exposed now.
    def _add_memtable(self, table: str):
        if table in self.memtables.keys():
            print(f'WARN - memtable "{table}" already exists')
            return

        self.memtables[table] = SortedDict()

    def _get_memtable(self, table: str) -> SortedDict:
        return self.memtables[table]