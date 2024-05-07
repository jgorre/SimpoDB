import json

from ..constants import DATA_PATH

def get_latest_schema(table_name: str):
    schema_path = DATA_PATH / table_name / 'schema.json'

    if not schema_path.exists():
        return None

    with open(schema_path, 'r') as schema:
        schemas = json.load(schema)
        num_schemas = len(schemas)
        latest_schema_index = num_schemas - 1
        return schemas[latest_schema_index]
    
def get_schema_columns(table_name: str):
    schema = get_latest_schema(table_name)
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