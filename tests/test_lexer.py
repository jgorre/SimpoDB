# from sql_engine.sql_parser.tokens import lexer
# import sys
# sys.path.insert(0, '/home/jordan.gorrell/practiceRepos/parser')
# print(sys.path)

from sql_engine.sql_parser.tokens import lexer, tokens

def assert_token_type_value(token, expected_token_type, expected_value):
    assert token.type == expected_token_type and token.value == expected_value


def test_tokens():
    pass


def test_select_star_statement():
    lexer.input('select * from mytable')
    tokens = list(lexer)
    
    assert len(tokens) == 4
    assert tokens[0].type == 'SELECT'
    assert tokens[1].type == 'STAR'
    assert tokens[2].type == 'FROM'

    table_token = tokens[3]
    assert_token_type_value(table_token, 'IDENTIFIER', 'mytable')


def test_select_columns_statement():
    lexer.input('select col1, col2, col3 from mytable')
    tokens = list(lexer)
    
    col1_token = tokens[1]
    col2_token = tokens[3]
    col3_token = tokens[5]
    assert_token_type_value(col1_token, 'IDENTIFIER', 'col1')
    assert_token_type_value(col2_token, 'IDENTIFIER', 'col2')
    assert_token_type_value(col3_token, 'IDENTIFIER', 'col3')


# def test_