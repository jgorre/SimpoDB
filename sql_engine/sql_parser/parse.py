import ply.yacc as yacc

from .tokens import tokens
from .sql_commands import SelectCommand, CreateTableCommand, InsertCommand

def p_sql_statement(p):
    '''sql_statement : query 
                     | create_schema
                     | create_table
                     | insert_statement
    '''
    p[0] = p[1]

def p_query(p):
    '''query : SELECT select_columns FROM IDENTIFIER'''    
    columns = p[2]
    table = p[4]
    p[0] = SelectCommand(columns, table)

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
    p[0] = CreateTableCommand(table_name, columns)

def p_create_table_columns(p):
    '''create_table_columns : IDENTIFIER column_type COMMA create_table_columns
                            | IDENTIFIER column_type
    '''
    if len(p) == 5:
        p[0] = [(p[1], p[2])] + p[4]
    else:
        p[0] = [(p[1], p[2])]

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