import ply.yacc as yacc

from ..commands.select_command import SelectCommand
from ..commands.insert_command import InsertCommand
from ..commands.create_table_command import CreateTableCommand


from .tokens import tokens

def p_sql_statement(p):
    '''sql_statement : query 
                     | create_schema
                     | create_table
                     | insert_statement
    '''
    p[0] = p[1]

def p_query(p):
    '''query : SELECT select_columns FROM IDENTIFIER
             | SELECT select_columns FROM IDENTIFIER WHERE where_clause'''    
    columns = p[2]
    table = p[4]
    where_statement = None

    if len(p) == 7:
        where_statement = p[6]

    p[0] = SelectCommand(columns, table, where_statement)

def p_where_clause(p):
    '''where_clause : where_item
                    | where_item and_or where_clause
                    | LPAREN where_clause RPAREN
                    | LPAREN where_clause RPAREN and_or where_clause'''
    
    if len(p) == 6:
        lparen = p[1]
        clause1 = p[2]
        rparen = p[3]
        and_or = p[4]
        clause2 = p[5]

        p[0] = [lparen] + clause1 + [rparen, and_or] + clause2
    elif len(p) == 4:
        if p[1] == '(' and p[3] == ')':
            lparen = p[1]
            clause = p[2]
            rparen = p[3]
            p[0] = [lparen] + clause + [rparen]
        else:
            condition = p[1]
            and_or = p[2]
            next_clause = p[3]
            p[0] = [condition, and_or] + next_clause
    else:
        condition = p[1]
        p[0] = [condition]

def p_and_or(p):
    '''and_or : AND
              | OR'''
    
    p[0] = p[1]

def p_where_item(p):
    '''where_item : IDENTIFIER EQUALS number_or_string'''
    p[0] = (p[1], p[3].strip("'"))

def p_select_columns(p):
    '''select_columns : STAR COMMA select_columns
                      | STAR
                      | IDENTIFIER COMMA select_columns
                      | IDENTIFIER
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_create_schema(p):
    'create_schema : CREATE SCHEMA IDENTIFIER'
    p[0] = {
        'type': 'CREATE_SCHEMA',
        'schema_name': p[3]
    }

def p_create_table(p):
    'create_table : CREATE TABLE IDENTIFIER LPAREN create_table_columns RPAREN'
    table_name = p[3]
    columns = p[5]
    
    primary_key = None
    for column in columns:
        if 'PRIMARY KEY' in column[2]:
            primary_key = column[0]
            break

    if primary_key is None:
        raise ValueError("Cannot create a table without a primary key.")
    
    p[0] = CreateTableCommand(table_name, columns, primary_key)

def p_create_table_columns(p):
    '''create_table_columns : table_column_definition COMMA create_table_columns
                            | table_column_definition
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_table_column_definition(p):
    '''table_column_definition : IDENTIFIER column_type
                               | IDENTIFIER column_type PRIMARY KEY
    '''
    if len(p) == 5:
        p[0] = [p[1], p[2], ['PRIMARY KEY']]
    else:
        p[0] = [p[1], p[2], []]

def p_column_type(p):
    '''column_type : INT
                   | STRING
    '''
    p[0] = p[1]

def p_insert_statement(p):
    'insert_statement : INSERT INTO IDENTIFIER LPAREN insert_column_names RPAREN VALUES insert_column_values'
    table = p[3]
    columns = p[5]
    values = p[8]
    p[0] = InsertCommand(table, columns, values)

def p_insert_column_names(p):
    '''insert_column_names : IDENTIFIER COMMA insert_column_names
                           | IDENTIFIER
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_insert_column_values(p):
    '''insert_column_values : LPAREN insert_values RPAREN COMMA insert_column_values
                            | LPAREN insert_values RPAREN
    '''
    if len(p) == 6:
        p[0] = [p[2]] + p[5]
    else:
        p[0] = [p[2]]

# Rename This
def p_insert_values(p):
    '''insert_values : number_or_string COMMA insert_values
                     | number_or_string
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_number_or_string(p):
    '''number_or_string : STRING
                            | NUMBER
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()