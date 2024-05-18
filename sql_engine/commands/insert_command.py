from .sql_command import SqlCommand
from ..sql_types.sql_type_mapping import sql_type_mapping
from ..data_serialization.writer import Writer
from ..data_serialization.schema import get_latest_schema
from ..storage.storage import TableStorage
from ..storage.data_for_insert import DataForInsert

class InsertCommand(SqlCommand):
    def __init__(self, table, columns, values):
        self.type = 'INSERT'
        self.table = table
        self.columns = columns
        self.values = values


    def execute(self):
        schema = get_latest_schema(self.table)

        if schema is None:
            print(f"Table '{self.table}' does not exist")
            return
        
        column_names = [c['name'] for c in schema['columns']]
        for column in self.columns:
            if column not in column_names:
                print(f"Column '{column}' does not exist in table '{self.table}'.")
                return
            
        column_list_index_dict = {
            self.columns.index(column): column_names.index(column) for column in self.columns
        }

        schema_version = schema['version']
        primary_key = schema['primary_key']
        columns = schema['columns']
        primary_key_index = next((index for index, item in enumerate(columns) if item['name'] == primary_key), None)

        if primary_key_index is None:
            raise ValueError("Explode")

        insertion_data = []
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

                
            insertion_data.append(DataForInsert(sorted_values_list, schema_version, primary_key_index))

        storage = TableStorage()
        storage.write_data_to_table(self.table, insertion_data)