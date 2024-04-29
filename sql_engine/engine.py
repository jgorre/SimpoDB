from pathlib import Path
import json

from .sql_parser.parse import parser
from .sql_types.sql_type_mapping import sql_type_mapping
from .commands.select_command import SelectCommand
from .commands.insert_command import InsertCommand
from .commands.create_table_command import CreateTableCommand

DATA_FOLDER_PATH = Path("./data")

def read_schema(folder_path: Path):
    schema_file_path = folder_path / "schema.json"
    with open(schema_file_path, "r") as schema_file:
        schema = json.load(schema_file)
    return schema

# create table persons (firstname string, lastname string, age int)
def handle_create_table(create_table_command: CreateTableCommand):
    table_name = create_table_command.table_name
    new_folder_path = DATA_FOLDER_PATH / table_name

    if new_folder_path.exists():
        print(f"Table '{table_name}' already exists.")
        return

    new_folder_path.mkdir(parents=True, exist_ok=False)

    # Create schema.json file in the new folder
    schema_file_path = new_folder_path / "schema.json"
    with open(schema_file_path, "w") as schema_file:
        schema = create_table_command.schema()
        json.dump(schema, schema_file, indent=4)  # You can provide your desired JSON content here


def handle_select(query: SelectCommand):
    table = query.table
    table_path = DATA_FOLDER_PATH / table

    data_file_path = table_path / 'data'
    with open(data_file_path, "r") as f:
        for line in f:
            print(line)


def handle_sql_command(sql):
    if isinstance(sql, SelectCommand):
        handle_select(sql)
    elif isinstance(sql, CreateTableCommand):
        handle_create_table(sql)
    elif isinstance(sql, InsertCommand):
        sql.execute()
        # handle_insert(sql)
    else:
        print(f"Unknown command: {sql}")

def run():
    while True:
        try:
            s = input('sql_command > ')
        except EOFError:
            break
        if not s: continue
        parsed_sql_command = parser.parse(s)
        handle_sql_command(parsed_sql_command)

# def manual_pack(integer, string):
#     # Ensure the string is exactly 4 characters (for simplicity)
#     string = string.ljust(4)[:4]  

#     # Convert integer to bytes
#     integer_bytes = bytes([
#         (integer >> 24) & 0xFF,  # Most significant byte
#         (integer >> 16) & 0xFF,
#         (integer >> 8) & 0xFF,
#         integer & 0xFF           # Least significant byte
#     ])

#     # Convert string to bytes
#     string_bytes = string.encode('utf-8')

#     # Concatenate byte data
#     return integer_bytes + string_bytes

# packed_data = manual_pack(1234, 'ABCD')
# print(f'Packed Data: {packed_data.hex()}')  # Using .hex() to show binary data in hex form