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
        
        # Consider making this function return on a more generator-y basis
        if self._should_use_index():
            primary_key_condition = [c for c in self.where_statement if c[0] == self.primary_key_column][0]
            search_value = primary_key_condition[2]
            result = [self.table_storage.read_entity_from_index(self.table, search_value)]
        else:
            result = list(self.table_storage.read_all(self.table))
        
        result = [e.data for e in result]

        if self.where_statement is not None:
            return_vals = []
            for val in result:
                if self._does_entity_pass_search_condition(val):
                    return_vals.append(val)

            result = return_vals

        result = self._format_result(result)

        for val in result:
            print(val)

        return result


    def _should_use_index(self):
        if self.where_statement is None:
            return False

        index_conditions = [c for c in self.conditions if c[0] == self.primary_key_column and c[1] == '=']
        is_single_index_condition = len(index_conditions) == 1
        or_and_operators = [op.upper() for op in self.where_statement if not isinstance(op, tuple) and op.upper() in ['OR', 'AND']]
        is_only_and_operators = len(or_and_operators) == 0 or all(op == 'AND' for op in or_and_operators)

        return is_single_index_condition and is_only_and_operators

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

        
