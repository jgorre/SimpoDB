from .sql_command import SqlCommand
from ..storage.storage import TableStorage
from ..data_serialization.schema import SchemaManager

class SelectCommand(SqlCommand):
    def __init__(self, columns, table, where_condition=None):
        self.table_storage = TableStorage()
        self.schema_manager = SchemaManager()

        self.type = 'SELECT'
        self.columns = columns
        self.table = table
        self.where_condition = where_condition
        self.primary_key_column = self.schema_manager.get_primary_key_column_for_table(self.table)

    def execute(self):
        if self.where_condition is None:
            result = list(self.table_storage.read_all(self.table))
            for entity in result:
                print(entity)
            return result
        elif self._is_search_condition_on_index():
            primary_key_condition = [c for c in self.where_condition if c[0] == self.primary_key_column][0]
            indexed_column = primary_key_condition[0]
            search_value = primary_key_condition[1]
            result = self.table_storage.read_entity_from_index(self.table, indexed_column, search_value)
            # need to still perform pass search condition check
            print(result)
            return result
        else:
            result = self.table_storage.read_all(self.table)
            return_vals = []
            for entity in result:
                if self._does_entity_pass_search_condition(entity):
                    return_vals.append(entity)

            for entity in return_vals:
                print(entity)

            return return_vals

        # Bloom filter later

    def _is_search_condition_on_index(self):
        for condition in self.where_condition:
            if isinstance(condition, tuple) and condition[0] == self.primary_key_column:
                return True
            
        return False
    
    def _does_entity_pass_search_condition(self, entity):
        # Helper function to evaluate a single condition
        def evaluate_condition(entity, condition):
            search_col, search_value = condition
            try:
                # Simple logic now. Might want to adjust later.
                entity_val = entity[search_col]
            except Exception:
                return False
            
            entity_val_type = type(entity_val)
            cast_search_val = entity_val_type(search_value)

            return entity[search_col] == cast_search_val

        # Initialize the result with the first condition
        result = evaluate_condition(entity, self.where_condition[0])
        
        # Iterate over the conditions and the logical operators
        for i in range(1, len(self.where_condition), 2):
            logical_operator = self.where_condition[i].upper()
            next_condition = self.where_condition[i + 1]
            
            if logical_operator == 'AND':
                result = result and evaluate_condition(entity, next_condition)
            elif logical_operator == 'OR':
                result = result or evaluate_condition(entity, next_condition)
            else:
                raise ValueError(f"Unknown logical operator: {logical_operator}")
        
        return result