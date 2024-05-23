from sortedcontainers import SortedDict
from pympler.asizeof import asizeof
import time
import json

from ..constants import DATA_PATH
from .data_for_insert import DataForInsert
from .path_manager import PathManager
from ..data_serialization import writer
from ..data_serialization import reader

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
            self.sparse_indexes = {}
            self.initialized = True

        self.path_manager = PathManager()

    def do_startup_initialization(self):
        self._initialize_memtables()
        self._initialize_sparse_indexes()

    def _initialize_memtables(self):
        tables = [f.name for f in DATA_PATH.iterdir() if f.is_dir()]
        for table in tables:
            write_ahead_log = DATA_PATH / table / 'writeahead.log'
            if not write_ahead_log.exists():
                continue

            with open(write_ahead_log, 'r') as log:
                for line in log:
                    data = DataForInsert.from_dict(json.loads(line))
                    self._write_to_memtable(table, [data])

            if self._should_memtable_be_flushed(table):
                self._write_sstable(table)


    def _initialize_sparse_indexes(self):
        tables = [f.name for f in DATA_PATH.iterdir() if f.is_dir()]
        for table in tables:
            sstables_path = self.path_manager.get_sstables_path(table)
            for path in sstables_path.iterdir():
                with open(path / 'offsets', 'r') as offset_file:
                    byte_offsets = json.load(offset_file)
                    sstable_name = path.name
                    if table not in self.sparse_indexes:
                        self.sparse_indexes[table] = {}

                    self.sparse_indexes[table][sstable_name] = byte_offsets

    def _should_memtable_be_flushed(self, table: str):
        # return asizeof(memtable) > 5_000
        # return len(self._get_memtable(table)) > 5
        return len(self._get_memtable(table)) > 28


    def write_data_to_table(self, table: str, data: list[DataForInsert]):
        self._write_to_log(table, data)
        self._write_to_memtable(table, data)

        if self._should_memtable_be_flushed(table):
            self._write_sstable(table)


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
            memtable[key] = { 'data': row.data, '__schema_version': row.schema_version }

        
    def _write_sstable(self, table: str):
        memtable = self._get_memtable(table)

        encoded_values = [
            (
                key, 
                writer.encode(value['data'], value['__schema_version'])
            ) for key, value in memtable.items()]

        nanotime_str = str(time.time_ns())
        sstables_path = self.path_manager.get_sstables_path(table)
        sstables_path.mkdir(parents=False, exist_ok=True)

        new_sstable_name = nanotime_str + '__uncommitted'
        new_sstable_path = sstables_path / new_sstable_name
        new_sstable_data_path = new_sstable_path / 'data'
        new_sstable_offsets_path = new_sstable_path / 'offsets'

        new_sstable_path.mkdir(parents=False, exist_ok=True)

        byte_offsets = {}

        with open(new_sstable_data_path, 'wb') as data_file:
            for index, (key, value) in enumerate(encoded_values):
                if index % 5 == 0:
                    byte_offsets[key] = data_file.tell()
                data_file.write(value)

        with open(new_sstable_offsets_path, 'w') as offsets_file:
            json.dump(byte_offsets, offsets_file, separators=(',', ':'))

            if table not in self.sparse_indexes:
                self.sparse_indexes[table] = {}

            self.sparse_indexes[table][nanotime_str] = byte_offsets

        new_sstable_path.rename(sstables_path / nanotime_str)
        self.path_manager.get_write_ahead_log_path(table).unlink()
        self._reset_memtable(table)

            
    def read_all(self, table: str):
        sstable_path = self.path_manager.get_sstables_path(table)
        vals = []
        for path in sstable_path.iterdir():
            for entity in reader.decode(table, path / 'data'):
                vals.append(entity)

        print(vals)

    def read_entity(self, table: str, condition):
        search_column, search_key_value = condition

        memtable = self._get_memtable(table)
        if search_key_value in memtable is not None:
            print(memtable[search_key_value])
            return
        
        sstables_path = self.path_manager.get_sstables_path(table)
        sorted_dirs = sorted(sstables_path.iterdir(), key=lambda p: int(p.name), reverse=True)
        for path in sorted_dirs:
            print(f'searching path {path} for value {search_key_value}')
            for entity in reader.decode(table, path / 'data'):
                if entity[search_column] == search_key_value:
                    print(entity)
                    return


    def _get_memtable(self, table: str) -> SortedDict:
        try:
            return self.memtables[table]
        except KeyError:
            # Do not keep this this way
            return SortedDict()
        
    def _reset_memtable(self, table: str):
        self.memtables[table] = SortedDict()
    
    
    def _instantiate_memtable(self, table: str):
        if table in self.memtables.keys():
            print(f'WARN - memtable "{table}" already exists')
            return

        self.memtables[table] = SortedDict()