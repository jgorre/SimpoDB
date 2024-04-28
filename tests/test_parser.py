from sql_engine.sql_parser.parse import parser

def test_select_star():
    query = 'select * from mytable'
    select_command = parser.parse(query)
    
    assert select_command.table   == 'mytable'
    assert select_command.columns == ['*']


def test_select_columns():
    query = 'select col1, col2, col3 from mytable'
    select_command = parser.parse(query)
    
    assert select_command.table   == 'mytable'
    assert select_command.columns == ['col1', 'col2', 'col3']


def test_create_table():
    sql = 'create table mytable (col1 string, col2 int)'
    create_table_command = parser.parse(sql)
    schema = create_table_command.schema()
    
    assert schema['table_name'] == 'mytable'
    assert schema['columns'] == [
        {
            'name': 'col1', 
            'type': 'STRING'
        },
        {
            'name': 'col2', 
            'type': 'INT'
        }
    ]


def test_insert_one_row():
    sql = 'insert into mytable (col1, col2) values (1, 2)'
    insert_command = parser.parse(sql)

    assert insert_command.columns == ['col1', 'col2']
    assert insert_command.values == [['1', '2']]


def test_insert_one_row():
    sql = 'insert into mytable (col1, col2) values (1, 2), (3, 4), (5, 6)'
    insert_command = parser.parse(sql)

    assert insert_command.columns == ['col1', 'col2']
    assert insert_command.values == [['1', '2'], ['3', '4'], ['5', '6']]
    