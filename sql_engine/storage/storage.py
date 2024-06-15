from sortedcontainers import SortedDict
from pybloom_live import ScalableBloomFilter
import time
import json
import yaml
import heapq
import shutil

from .data_for_insert import DataForInsert
from .path_manager import PathManager
from ..data_serialization.schema import SchemaManager
from ..data_serialization import writer
from ..data_serialization import reader
from ..data_serialization.entity import Entity
from ..config.config import Config

SSTABLE_SIZE = 28

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
            self.bloom_filters = {}
            self.initialized = True

        self.path_manager = PathManager()
        self.schema_manager = SchemaManager()
        self.tables = [f.name for f in self.path_manager.get_data_path().iterdir() if f.is_dir()]
        
        self.db_config = Config()
        self.sstable_size = self.db_config.sstable_size

    def do_startup_initialization(self):
        self._initialize_bloom_filters()
        self._initialize_memtables()
        self._initialize_sparse_indexes()


    def _initialize_bloom_filters(self):
        for table in self.tables:
            bloom_filter_path = self.path_manager.get_bloom_filter_path(table)

            if not bloom_filter_path.exists():
                self.bloom_filters[table] = self.create_bloom_filter(table)
                continue

            with open(bloom_filter_path, 'rb') as bloom_file:
                self.bloom_filters[table] = ScalableBloomFilter().fromfile(bloom_file)


    def _initialize_memtables(self):
        for table in self.tables:
            write_ahead_log = self.path_manager.get_data_path() / table / 'writeahead.log'
            if not write_ahead_log.exists():
                continue

            with open(write_ahead_log, 'r') as log:
                for line in log:
                    data = DataForInsert.from_dict(json.loads(line))
                    self._write_to_memtable(table, [data])

            if self._should_memtable_be_flushed(table):
                self._flush_memtable(table)

    
    def get_encoded_memtable_values(self, table: str):
        memtable = self._get_memtable(table)

        return [
            (
                key, 
                writer.encode(value['data'], value['__schema_version'])
            ) for key, value in memtable.items()]


    def _initialize_sparse_indexes(self):
        for table in self.tables:
            sstables_path = self.path_manager.get_sstables_path(table)

            if not sstables_path.exists():
                continue

            for path in sstables_path.iterdir():
                with open(path / 'offsets', 'r') as offset_file:
                    byte_offsets = yaml.safe_load(offset_file)
                    sstable_name = path.name
                    if table not in self.sparse_indexes:
                        self.sparse_indexes[table] = {}

                    self.sparse_indexes[table][sstable_name] = byte_offsets


    def _should_memtable_be_flushed(self, table: str):
        return len(self._get_memtable(table)) >= self.sstable_size


    def write_data_to_table(self, table: str, data: list[DataForInsert]):
        self._write_to_log(table, data)
        self._write_to_memtable(table, data)

        if self._should_memtable_be_flushed(table):
            self._flush_memtable(table)

    
    def _flush_memtable(self, table):
        encoded_values = self.get_encoded_memtable_values(table)
        self._write_uncommitted_sstable(table, encoded_values)
        self._commit_sstables(table)
        self._write_bloom_filter(table)
        self._remove_write_ahead_log(table)
        self._reset_memtable(table)


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
        bloom_filter = self._get_bloom_filter(table)

        for row in data:
            key = row.data[row.primary_key_index]
            memtable[key] = { 'data': row.data, '__schema_version': row.schema_version }
            bloom_filter.add(key)

        
    def _write_uncommitted_sstable(self, table: str, encoded_values):
        sstables_path = self.path_manager.get_sstables_path(table)
        sstables_path.mkdir(parents=False, exist_ok=True)

        sstable_name = str(time.time_ns())
        uncommitted_sstable_name = sstable_name + '__uncommitted'
        uncommitted_sstable_path = sstables_path / uncommitted_sstable_name

        uncommitted_sstable_path.mkdir(parents=False, exist_ok=True)

        self.___write_sstable(table, uncommitted_sstable_path, sstable_name, encoded_values)

    
    def _commit_sstables(self, table):
        sstable_path = self.path_manager.get_sstables_path(table)
        uncommitted_tables = [p for p in sstable_path.rglob('*__uncommitted') if p.is_dir()]

        for table in uncommitted_tables:
            committed_table_name = table.stem.replace("__uncommitted", '')
            table.rename(sstable_path / committed_table_name)

    def _remove_write_ahead_log(self, table):
        self.path_manager.get_write_ahead_log_path(table).unlink()

    
    def _write_bloom_filter(self, table):
        bloom_path = self.path_manager.get_bloom_filter_path(table)
        bloom_filter = self._get_bloom_filter(table)
        
        with open(bloom_path, 'wb') as bloom_file:
            bloom_filter.tofile(bloom_file)


    def ___write_sstable(self, table, uncommitted_sstable_path, sstable_name, encoded_values):
        new_sstable_data_path = uncommitted_sstable_path / 'data'
        new_sstable_offsets_path = uncommitted_sstable_path / 'offsets'

        byte_offsets = {}

        sparse_index_distance = self.sstable_size / 5

        with open(new_sstable_data_path, 'wb') as data_file:
            for index, (key, value) in enumerate(encoded_values):
                if index % sparse_index_distance == 0:
                    byte_offsets[key] = data_file.tell()
                data_file.write(value)

        with open(new_sstable_offsets_path, 'w') as offsets_file:
            yaml.dump(byte_offsets, offsets_file)

            if table not in self.sparse_indexes:
                self.sparse_indexes[table] = {}

            self.sparse_indexes[table][sstable_name] = byte_offsets


    def perform_compaction(self, table: str):
        sstables_path = self.path_manager.get_sstables_path(table)
        sstables_path.mkdir(parents=False, exist_ok=True)

        vals = self.read_all_sstable_data(table)

        chunk = []
        for val in vals:
            chunk.append(
                (
                    val.get_key_value(),
                    writer.encode(val.data.values(), val.schema_version)
                )
            )
            if len(chunk) >= self.sstable_size:
                self._write_uncommitted_sstable(table, chunk)
                chunk = []

        if len(chunk) > 0:
            self._write_uncommitted_sstable(table, chunk)
            chunk = []

        for item in sstables_path.iterdir():
            if item.is_dir() and not item.name.endswith('__uncommitted'):
                shutil.rmtree(item)

        self._commit_sstables(table)
                

    def read_all(self, table: str):
        keys = set()

        memtable = self._get_memtable(table)

        for key in memtable:
            keys.add(key)
            yield self._get_entity_from_memtable_record(table, key)
        
        yield from self.read_all_sstable_data(table, keys)

    def read_all_sstable_data(self, table: str, keys=set()):
        heap = []

        sstable_path = self.path_manager.get_sstables_path(table)
        
        def get_file_iterator(file_path):
            yield from reader.decode(table, file_path)

        sstable_iterators = [get_file_iterator(path / 'data') for path in sorted(list(sstable_path.iterdir()), reverse=True)]

        for iter_index, iterator in enumerate(sstable_iterators):
            value = next(iterator)
            key = value.get_key_value()
            heapq.heappush(heap, (key, iter_index, value))

        while heap:
            key, iter_index, value = heapq.heappop(heap)

            if key not in keys:
                keys.add(key)
                yield value

            next_value = next(sstable_iterators[iter_index], None)

            if next_value is not None:
                next_key = next_value.get_key_value()
                heapq.heappush(heap, (next_key, iter_index, next_value))
            

    def read_entity_from_index(self, table: str, search_key_value):
        primary_key_type = self.schema_manager.get_primary_key_type(table)
        cast_search_key_value = primary_key_type(search_key_value)

        is_val_in_bloom_filter = cast_search_key_value in self._get_bloom_filter(table)
        if not is_val_in_bloom_filter:
            return
        
        result_from_memtable = self._get_entity_from_memtable_record(table, cast_search_key_value)

        if result_from_memtable is not None:
            return result_from_memtable            
        
        sstables_path = self.path_manager.get_sstables_path(table)
        sorted_dirs = sorted(sstables_path.iterdir(), key=lambda p: int(p.name), reverse=True)
        for path in sorted_dirs:
            from_byte, until_byte = self._get_byte_range(table, path.name, cast_search_key_value)

            if from_byte is None:
                continue

            # print(f'searching path {path} for value {cast_search_key_value} between bytes {from_byte} and {until_byte}')
            for entity in reader.decode(table, path / 'data', from_byte, until_byte):
                if entity.get_key_value() == cast_search_key_value:
                    return entity


    def _get_entity_from_memtable_record(self, table: str, key):
        memtable = self._get_memtable(table)

        if len(memtable) == 0:
            return None
        
        if key not in memtable:
            return None
        
        memtable_record = memtable[key]
        schema_version = memtable_record['__schema_version']
        record_schema = self.schema_manager.get_schema_with_version(table, schema_version)
        data = {}
        for i, column in enumerate(record_schema['columns']):
            data[column['name']] = memtable_record['data'][i]

        return Entity(schema_version, record_schema['primary_key'], data)

    def _get_byte_range(self, table, sstable_name, search_key_value):
        sparse_index = self.sparse_indexes[table][sstable_name]
        keys = list(sparse_index.keys())
        from_byte = None
        to_byte = None

        for i in range(len(keys)):
            current_key = keys[i]
            next_key = keys[i + 1] if i + 1 < len(keys) else None
            
            if search_key_value >= current_key and (next_key is None or search_key_value < next_key):
                from_byte = sparse_index[current_key]
                to_byte = sparse_index[next_key] if next_key is not None else None
                break

        return from_byte, to_byte

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

    
    def _get_bloom_filter(self, table: str) -> ScalableBloomFilter:
        if table not in self.bloom_filters:
            return None
        
        return self.bloom_filters[table]
    
    def create_bloom_filter(self, table: str):
        self.bloom_filters[table] = ScalableBloomFilter(initial_capacity=1000, error_rate=0.005)