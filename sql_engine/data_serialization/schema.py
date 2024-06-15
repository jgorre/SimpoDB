import json

from sql_engine.storage.path_manager import PathManager
from ..sql_types.sql_type_mapping import sql_type_mapping

class SchemaManager:
    def __init__(self) -> None:
        # make cache for recently accessed stuff. 
        # Or why not simply load all schemas into memory?
        # How many schemas could there realistically be?

        self.path_manager = PathManager()

    def get_schema_path(self, table_name: str):
        schema_path = self.path_manager.get_data_path() / table_name / 'schema.json'

        if not schema_path.exists():
            return None
        
        return schema_path

    def get_all_schemas(self, table_name: str):
        schema_path = self.get_schema_path(table_name)
        with open(schema_path, 'r') as schemas:
            return json.load(schemas)

    def get_latest_schema(self, table_name: str):
        schema_path = self.get_schema_path(table_name)
        with open(schema_path, 'r') as schema:
            schemas = json.load(schema)
            latest_version = max(schemas.keys(), key=int)
            return latest_version, schemas[latest_version]
        
    def get_schema_with_version(self, table_name: str, version: int):
        schema_path = self.get_schema_path(table_name)
        with open(schema_path, 'r') as schema:
            schemas = json.load(schema)

            try:
                return schemas[str(version)]
            except:
                print(f'Schema version {version} for table {table_name} does not exist.')
                return None
        
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