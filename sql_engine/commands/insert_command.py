from pathlib import Path
import json

from .sql_command import SqlCommand
from ..constants import DATA_PATH
from ..sql_types.sql_type_mapping import sql_type_mapping
from ..encoding.writer import Writer

class InsertCommand(SqlCommand):
    def __init__(self, table, columns, values):
        self.type = 'INSERT'
        self.table = table
        self.columns = columns
        self.values = values


    def execute(self):
        folder_path = DATA_PATH / self.table

        if not folder_path.exists():
            print(f"Table '{self.table}' does not exist")
            return
        
        schema = self._read_schema(folder_path)
        column_names = [c['name'] for c in schema['columns']]
        for column in self.columns:
            if column not in column_names:
                print(f"Column '{column}' does not exist in table '{self.table}'.")
                return
            
        column_list_index_dict = {
            self.columns.index(column): column_names.index(column) for column in self.columns
        }

        insert_values = []
        for value_list in self.values:
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
                    if column_type == 'STRING':
                        if not value.startswith("'") or not value.endswith("'"):
                            raise ValueError(f"{value} is not a valid string")
                        value = value[1:-1]
                    
                    sorted_values_list[index] = python_type(value)
                except ValueError:
                    print(f"Value {value} does not match type '{column_type}'.")
                    return

                
            insert_values.append(sorted_values_list)

        data_file_path = folder_path / "data"
        writer = Writer()
        writer.write(insert_values, data_file_path)

    def _read_schema(self, folder_path: Path):
        schema_file_path = folder_path / "schema.json"
        with open(schema_file_path, "r") as schema_file:
            schema = json.load(schema_file)
        return schema