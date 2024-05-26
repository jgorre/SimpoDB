import json

from ..constants import DATA_PATH

def get_schema_path(table_name: str):
    schema_path = DATA_PATH / table_name / 'schema.json'

    if not schema_path.exists():
        return None
    
    return schema_path

def get_all_schemas(table_name: str):
    schema_path = get_schema_path(table_name)
    with open(schema_path, 'r') as schemas:
        return json.load(schemas)

def get_latest_schema(table_name: str):
    schema_path = get_schema_path(table_name)
    with open(schema_path, 'r') as schema:
        schemas = json.load(schema)
        latest_version = max(schemas.keys(), key=int)
        return latest_version, schemas[latest_version]
    
def get_schema_with_version(table_name: str, version: int):
    schema_path = get_schema_path(table_name)
    with open(schema_path, 'r') as schema:
        schemas = json.load(schema)

        try:
            return schemas[str(version)]
        except:
            print(f'Schema version {version} for table {table_name} does not exist.')
            return None
    
def get_schema_columns(table_name: str):
    _, schema = get_latest_schema(table_name)
    return schema['columns']
    
def create_schema(table_name: str, schema: dict):
    schema_path = DATA_PATH / table_name
    if schema_path.exists():
        print(f"Table '{table_name}' already exists or path is corrupt.")
        return

    schema_path.mkdir(parents=True, exist_ok=False)

    schema_file_path = schema_path / "schema.json"
    with open(schema_file_path, "w") as schema_file:
        json.dump(schema, schema_file, indent=4)

    sstables_path = schema_path / 'sstables'
    sstables_path.mkdir(parents=True, exist_ok=False)

def get_primary_key_column_for_table(table_name: str):
    _, schema = get_latest_schema(table_name)
    return schema['primary_key']