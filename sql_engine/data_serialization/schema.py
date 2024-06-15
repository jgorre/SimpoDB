import json

from sql_engine.storage.path_manager import PathManager
from ..sql_types.sql_type_mapping import sql_type_mapping

class SchemaManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SchemaManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self.initialized:
            return

        self.path_manager = PathManager()

        tables_path = self.path_manager.get_data_path()

        self.schemas = {}
        for table_path in tables_path.iterdir():
            schema_path = table_path / "schema.json"
            table_name = table_path.stem
            with open(schema_path, 'r') as schema_file:
                self.schemas[table_name] = json.load(schema_file)
        
        self.initialized = True

    def get_all_schemas(self, table_name: str):
        return self.schemas[table_name]

    def get_latest_schema(self, table_name: str):
        schema_version, schema = list(self.schemas[table_name].items())[-1]
        return schema_version, schema
        
    def get_schema_with_version(self, table_name: str, version: int):
        return self.schemas[table_name][str(version)]
        
    def get_schema_columns(self, table_name: str):
        _, schema = self.get_latest_schema(table_name)
        return schema['columns']
        
    def create_schema(self, table_name: str, schema: dict):
        schema_path = self.path_manager.get_data_path() / table_name
        if schema_path.exists():
            print(f"Table '{table_name}' already exists or path is corrupt.")
            return

        schema_path.mkdir(parents=True, exist_ok=False)

        schema_file_path = schema_path / "schema.json"
        with open(schema_file_path, "w") as schema_file:
            json.dump(schema, schema_file, indent=4)

        sstables_path = schema_path / 'sstables'
        sstables_path.mkdir(parents=True, exist_ok=False)

        self.schemas[table_name] = schema

    def get_primary_key_column_for_table(self, table_name: str):
        _, schema = self.get_latest_schema(table_name)
        return schema['primary_key']
    
    def get_primary_key_type(self, table_name: str):
        _, schema = self.get_latest_schema(table_name)
        primary_key = schema['primary_key']
        column_specs = [col_spec for col_spec in schema['columns'] if primary_key == col_spec['name']]

        if len(column_specs) != 1:
            raise ValueError(f"Table '{table_name}' has a corrupt schema. Expected to find one primary key column, got {len(column_specs)}")
        
        column_spec = column_specs[0]
        return sql_type_mapping[column_spec['type']]