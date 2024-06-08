import operator
from sympy.parsing.sympy_parser import parse_expr

from .sql_command import SqlCommand
from ..storage.storage import TableStorage
from ..data_serialization.schema import SchemaManager


class SelectCommand(SqlCommand):
    def __init__(self, columns, table, where_statement=None):
        self.table_storage = TableStorage()
        self.schema_manager = SchemaManager()

        self.type = 'SELECT'
        self.columns = columns
        self.table = table
        self.where_statement = where_statement
        self.conditions = None
        
        if where_statement is not None:
            self.conditions = [condition for condition in self.where_statement if isinstance(condition, tuple)]

        self.primary_key_column = self.schema_manager.get_primary_key_column_for_table(self.table)

    def execute(self):
        result = []
        if self.where_statement is None:
            result = list(self.table_storage.read_all(self.table))
            formatted_result = self._format_result(result)
            for entity in formatted_result:
                print(entity)
            return formatted_result
        
        # In what scenarios do we want to search on index?
            # indexed column condition plus ANDs
            # just indexed column
        
        if self._is_search_condition_on_index():
            primary_key_condition = [c for c in self.where_statement if c[0] == self.primary_key_column][0]
            indexed_column = primary_key_condition[0]
            search_value = primary_key_condition[2]
            result = [self.table_storage.read_entity_from_index(self.table, indexed_column, search_value)]
        else:
            result = self.table_storage.read_all(self.table)
            return_vals = []
            for entity in result:
                if self._does_entity_pass_search_condition(entity):
                    return_vals.append(entity)

            result = return_vals

        result = self._format_result(result)

        for entity in result:
            print(entity)

        return result

        # Bloom filter later

    def _is_search_condition_on_index(self):
        for condition in self.conditions:
            if condition[0] == self.primary_key_column:
                return True
            
        return False
    
    def _does_entity_pass_search_condition(self, entity):
        def evaluate_condition(condition):
            search_col, operation, search_value = condition
            try:
                entity_val = entity[search_col]
            except Exception:
                return False
            
            entity_val_type = type(entity_val)
            cast_search_val = entity_val_type(search_value)

            operations = {
                '=': operator.eq,
                '!=': operator.ne,
                '>': operator.gt,
                '>=': operator.ge,
                '<': operator.lt,
                '<=': operator.le,
            }

            entity_val = entity[search_col]
            if operation in operations:
                return operations[operation](entity_val, cast_search_val)
            
            raise ValueError(f'Unknown condition operator "{operator}"')

        result_tokens = []
        for token in self.where_statement:
            if not isinstance(token, tuple):
                result_tokens.append(token)
                continue
            condition = token
            result_tokens.append(evaluate_condition(condition))
        
        boolean_statement_tokens = [str(s).lower() for s in result_tokens]
        boolean_statement_string = " ".join(boolean_statement_tokens)
        return parse_expr(boolean_statement_string)
    

    def _format_result(self, result):
        if '*' in self.columns:
            return result
        
        formatted_result = []

        for res in result:
            entity = {}
            for col in self.columns:
                entity[col] = res[col]
            formatted_result.append(entity)

        return formatted_result

        
