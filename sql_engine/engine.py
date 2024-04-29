from pathlib import Path
import json

from .sql_parser.parse import parser
from .sql_parser.sql_commands import SelectCommand, CreateTableCommand, InsertCommand
from .sql_types.sql_type_mapping import sql_type_mapping

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


def handle_insert(insert_command: InsertCommand):
    table = insert_command.table
    folder_path = DATA_FOLDER_PATH / table

    if not folder_path.exists():
        print(f"Table '{table}' does not exist")
        return
    
    schema = read_schema(folder_path)
    column_names = [c['name'] for c in schema['columns']]
    for column in insert_command.columns:
        if column not in column_names:
            print(f"Column '{column}' does not exist in table '{table}'.")
            return
        
    # Put column values in correct order
    # We have the correct order of column names from the schema
    # Map index of insert_command.columns to index of column_names
    # Eventually handle nulls
    column_list_index_dict = {
        insert_command.columns.index(column): column_names.index(column) for column in insert_command.columns
    }

    insert_values = []
    for value_list in insert_command.values:
        sorted_values_list = [None] * (len(value_list))

        for i, value in enumerate(value_list):
            # Get column_spec
            index = column_list_index_dict.get(i)
            column_spec = schema['columns'][index]

            # Get column_type and python_type
            column_spec = schema['columns'][index]
            column_type = column_spec['type']
            python_type = sql_type_mapping.get(column_type)

            if python_type is None:
                print(f"Unknown type: '{column_type}'")
                print(column_spec)
                print(f'Column type "{column_type}" and python type {python_type}')
                return

            try:
                if column_type == 'STRING' and (not value.startswith("'") or not value.endswith("'")):
                    raise ValueError()
                else:
                    python_type(value)
            except ValueError:
                print(f"Value {value} does not match type '{column_type}'.")
                return

            sorted_values_list[index] = value
        
        insert_values.append(sorted_values_list)

    # insert into testtable (intval, strval) values (1, '2'), (3, 4)
    # insert into persons (lastname, age, firstname) values (gorrell, 29, jordan)
    # insert into mytable (v1, v2, v3) values (1, 2, 3), (4, 5, 6), (7, 8, 9)
    # insert into persons (lastname, age, firstname) values (gorrell, 29, jordan), (jakobsson, 28, louise), (gorrell, 26, cameron), (jakobsson, 66, agneta)
    data_file_path = folder_path / "data"
    with open(data_file_path, "a") as f:
        for line in insert_values:
            joined_line = ','.join(line)
            f.write(f'{joined_line}\n')


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
        handle_insert(sql)
    else:
        print(f"Unknown command: {sql}")

def run():
    while True:
        try:
            s = input('sql_command > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        handle_sql_command(result)

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