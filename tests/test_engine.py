import pytest
import shutil
import random

from sql_engine.engine import DatabaseEngine

from sql_engine.engine import DatabaseEngine
from sql_engine.config.config import Config

def reset_config():
    Config._instance = None

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
    create_table_statement = 'create table pups (name string primary key, age int, favorite_activity string)'
    result = database_engine.process_command(create_table_statement)

    pups = [
        "('luna', 6, 'barking and finding a cozy place to sleep')",
        "('baby', 25, 'eating')",
        "('cleo', 22, 'playing with toys')",
        "('ginger', 15, 'cuddling')"
    ]

    for pup in pups:
        insert_statement = f'insert into pups (name, age, favorite_activity) values {pup}'
        database_engine.process_command(insert_statement)

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

    query = "select * from items where id = 5"
    result = database_engine.process_command(query)
    assert result


def test_tmp(database_engine):
    create_table_statement = 'create table pickles (id int primary key, str string)'
    database_engine.process_command(create_table_statement)

    for i in range(0, 100):
        random_string = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 10))
        insert_statement = f"insert into pickles (id, str) values ({i}, '{random_string}')"
        database_engine.process_command(insert_statement)

    query = "select * from pickles"
    result = database_engine.process_command(query)
    assert result


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