from sql_engine.sql_parser.tokens import lexer, reserved_keywords
from ply.lex import LexError

def assert_token_type_value(token, expected_token_type, expected_value):
    assert token.type == expected_token_type and token.value == expected_value


def get_single_token(lexer):
    single_token_list = list(lexer)
    assert len(single_token_list) == 1
    return single_token_list[0]


## Tests ##

def test_simple_tokens():
    token_map = {
        'STAR': '*',
        'COMMA': ',',
        'LPAREN': '(',
        'RPAREN': ')',
        'EQUALS': '='
    }

    for token_type, token_value in token_map.items():
        lexer.input(token_value)
        token = get_single_token(lexer)
        assert token.type == token_type

def test_reserved_keywords():
    for keyword in reserved_keywords:
        upper_keyword = keyword.upper()
        lexer.input(upper_keyword)
        token = get_single_token(lexer)
        assert_token_type_value(token, keyword, token.value)

        lower_keyword = keyword.lower()
        lexer.input(lower_keyword)
        token = get_single_token(lexer)
        assert_token_type_value(token, keyword, token.value)


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


def test_unexpected_character():
    try:
        lexer.input("'asdf")
        get_single_token(lexer)
    except LexError:
        assert True


def test_string_and_identifier():
    input_str = "id 'string' anotherid 'another string'"
    lexer.input(input_str)
    tokens = list(lexer)

    first_identifier_token = tokens[0]
    first_string_token = tokens[1]
    second_identifier_token = tokens[2]
    second_string_token = tokens[3]

    assert first_identifier_token.type == 'IDENTIFIER'
    assert first_string_token.type == 'STRING'
    assert second_identifier_token.type == 'IDENTIFIER'
    assert second_string_token.type == 'STRING'


def test_number_and_string_and_identifier():
    input_str = "asdf 123 'adsf'"
    lexer.input(input_str)
    tokens = list(lexer)

    identifier_token = tokens[0]
    number_token = tokens[1]
    string_token = tokens[2]

    assert identifier_token.type == 'IDENTIFIER'
    assert number_token.type == 'NUMBER'
    assert string_token.type == 'STRING'