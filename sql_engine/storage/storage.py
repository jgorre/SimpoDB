from sortedcontainers import SortedDict
from pathlib import Path
import json

from ..constants import DATA_PATH

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

        # Do this first when you come back
        self.initialize_memtables()

    def write_data_to_table(self, table: str, schema: dict, data: list[list]):
        if table not in self.memtables.keys():
            self._instantiate_memtable(table)

        primary_key = schema['primary_key']
        schema_version = schema['version']
        
        memtable = self._get_memtable(table)
        primary_key = schema['primary_key']
        columns = schema['columns']
        primary_key_index = next((index for index, item in enumerate(columns) if item['name'] == primary_key), None)

        if primary_key_index is None:
            raise ValueError("Explode")
        
        for row in data:
            key = row[primary_key_index]
            memtable[key] = { 'entity': row, '__schema_version': schema_version }

        # If memtable chonky, do stuff
            
    def read(self, table: str):
        memtable = self._get_memtable(table)
        print(memtable)

    def _get_memtable(self, table: str) -> SortedDict:
        return self.memtables[table]
    
    def _instantiate_memtable(self, table: str):
        # Initially implement WAL with JSON encoding for simplicity

        if table in self.memtables.keys():
            print(f'WARN - memtable "{table}" already exists')
            return

        self.memtables[table] = SortedDict()

        def open_writeahead_log(table: str):
            writeahead_log_path = DATA_PATH / table / 'writeahead.log'
            if writeahead_log_path.exists():
                with open(writeahead_log_path, 'r') as file:
                    for row in file:
                        log_row = json.loads(row)
