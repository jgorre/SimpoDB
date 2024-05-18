from sortedcontainers import SortedDict
from pathlib import Path
import json

from ..constants import DATA_PATH
from .data_for_insert import DataForInsert
from .path_manager import PathManager

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

        self.path_manager = PathManager()

    def initialize_memtables(self):
        tables = [f.name for f in DATA_PATH.iterdir() if f.is_dir()]
        for table in tables:
            write_ahead_log = DATA_PATH / table / 'writeahead.log'
            if not write_ahead_log.exists():
                continue

            with open(write_ahead_log, 'r') as log:
                for line in log:
                    data = DataForInsert.from_dict(json.loads(line))
                    self._write_to_memtable(table, [data])


    def write_data_to_table(self, table: str, data: list[DataForInsert]):
        self._write_to_log(table, data)
        self._write_to_memtable(table, data)

    def _write_to_log(self, table: str, data: list[DataForInsert]):
        json_data = [json.dumps(d.to_dict(), separators=(',', ':')) for d in data]

        write_ahead_log_path = self.path_manager.get_write_ahead_log_path(table)
        with open(write_ahead_log_path, 'a') as log:
            for line in json_data:
                log.write(line + '\n')

    def _write_to_memtable(self, table: str, data: list[DataForInsert]):
        if table not in self.memtables.keys():
            self._instantiate_memtable(table)

        memtable = self._get_memtable(table)
        for row in data:
            key = row.data[row.primary_key_index]
            memtable[key] = { 'entity': row.data, '__schema_version': row.schema_version }

            
    def read(self, table: str):
        memtable = self._get_memtable(table)
        print(memtable)

    def _get_memtable(self, table: str) -> SortedDict:
        try:
            return self.memtables[table]
        except KeyError:
            return SortedDict()
    
    
    def _instantiate_memtable(self, table: str):
        if table in self.memtables.keys():
            print(f'WARN - memtable "{table}" already exists')
            return

        self.memtables[table] = SortedDict()