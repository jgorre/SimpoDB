import pytest
import shutil
import random

from sql_engine.engine import DatabaseEngine

from sql_engine.engine import DatabaseEngine
from sql_engine.config.config import Config

def reset_config():
    Config._instance = None

def prepare_pups_table(database_engine):
    create_table_statement = 'create table pups (name string primary key, age int, favorite_activity string)'
    database_engine.process_command(create_table_statement)

    pups = [
        "('luna', 6, 'barking and finding a cozy place to sleep')",
        "('baby', 25, 'eating')",
        "('cleo', 22, 'playing with toys')",
        "('ginger', 15, 'cuddling')"
    ]

    for pup in pups:
        insert_statement = f'insert into pups (name, age, favorite_activity) values {pup}'
        database_engine.process_command(insert_statement)

@pytest.fixture(scope="function")
def database_engine():
    reset_config()

    configuration = {
        "dataPath": "./test/data"
    }

    engine = DatabaseEngine(configuration)

    yield engine

    shutil.rmtree('./test')


def test_small_table(database_engine):
    prepare_pups_table(database_engine)

    luna_query = "select * from pups where name = 'luna'"
    luna_query_result = database_engine.process_command(luna_query)
    
    ginger_query = "select * from pups where name = 'ginger'"
    ginger_query_result = database_engine.process_command(ginger_query)

    assert luna_query_result == [{'name': 'luna', 'age': 6, 'favorite_activity': 'barking and finding a cozy place to sleep'}]
    assert ginger_query_result == [{'name': 'ginger', 'age': 15, 'favorite_activity': 'cuddling'}]


def test_large_table(database_engine):
    create_table_statement = 'create table items (id int primary key, str string)'
    database_engine.process_command(create_table_statement)

    for i in range(0, 5000):
        random_string = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 10))
        insert_statement = f"insert into items (id, str) values ({i}, '{random_string}')"
        database_engine.process_command(insert_statement)

    query = "select id from items where id = 5"
    result = database_engine.process_command(query)
    assert result[0] == { 'id': 5 }


def test_read_all_contains_only_latest_writes_per_key(database_engine):
    create_table_statement = 'create table pplz (name string primary key, recency string)'
    database_engine.process_command(create_table_statement)

    def insert_p(name, recency):
        return f"insert into pplz (name, recency) values ('{name}', '{recency}')"
    
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack", "Kathy", "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Rachel", "Sam", "Tina", "Uma", "Vince", "Wendy", "Xander", "Yara", "Zack", "Ava", "Ben", "Clara", "Daniel", "Ella", "Felix", "Georgia", "Henry", "Isla", "Jacob", "Karen", "Leo", "Megan", "Nina", "Oscar", "Penny", "Quincy", "Rita", "Sean", "Tara", "Uri", "Victor", "Willow", "Xena", "Yvonne", "Zane", "Amy", "Brian", "Cindy", "Dylan", "Emily", "Finn", "Gina", "Harry", "Iris", "James", "Kelly", "Lucas", "Molly", "Nick", "Opal", "Peter", "Quentin", "Ruby", "Scott", "Tiffany", "Ulysses", "Violet", "Wesley", "Xiomara", "Yasmin", "Zoe", "Abby", "Blake", "Chris", "Dana", "Eli", "Faith", "Gabe", "Holly", "Ian", "Jess", "Kyle", "Lily", "Miles", "Nate", "Owen"]

    for name in names:
        statement = insert_p(name, 'oldest')
        database_engine.process_command(statement)

    for name in names:
        statement = insert_p(name, 'older')
        database_engine.process_command(statement)

    for name in names:
        statement = insert_p(name, 'latest')
        database_engine.process_command(statement)

    query = "select * from pplz"
    result = database_engine.process_command(query)

    assert len(result) == len(names)

    bad_vals = [val for val in result if val['recency'] != 'latest']

    assert len(bad_vals) == 0


def test_simple_non_index_where_conditions(database_engine):
    prepare_pups_table(database_engine)

    query = 'select * from pups where age = 22'
    res = database_engine.process_command(query)
    assert res == [{ 'name': 'cleo', 'age': 22, 'favorite_activity': 'playing with toys' }]

    query = "select * from pups where favorite_activity = 'cuddling'"
    res = database_engine.process_command(query)
    assert res == [{ 'name': 'ginger', 'age': 15, 'favorite_activity': 'cuddling' }]

    query = "select * from pups where favorite_activity = 'cuddling' or age = 6"
    res = database_engine.process_command(query)
    assert res == [
        { 'name': 'ginger', 'age': 15, 'favorite_activity': 'cuddling' },
        {'name': 'luna', 'age': 6, 'favorite_activity': 'barking and finding a cozy place to sleep'}
    ]


def test_indexed_where_conditions(database_engine):
    prepare_pups_table(database_engine)

    query = "select * from pups where name = 'cleo'"
    res = database_engine.process_command(query)
    assert res == [{ 'name': 'cleo', 'age': 22, 'favorite_activity': 'playing with toys' }]


def test_search_columns(database_engine):
    prepare_pups_table(database_engine)

    query = "select age from pups where name = 'cleo'"
    res = database_engine.process_command(query)
    assert res == [{ 'age': 22 }]

    query = "select name, favorite_activity from pups where age = 6 or age = 22"
    res = database_engine.process_command(query)
    assert res == [
        { 'name': 'cleo', 'favorite_activity': 'playing with toys' },
        { 'name': 'luna', 'favorite_activity': 'barking and finding a cozy place to sleep' },
    ]
    