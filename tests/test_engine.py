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

    print('initializing db')
    engine = DatabaseEngine(configuration)

    yield engine

    print('cleaning up database stuffs')
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

    assert luna_query_result == {'name': 'luna', 'age': 6, 'favorite_activity': 'barking and finding a cozy place to sleep'}
    assert ginger_query_result == {'name': 'ginger', 'age': 15, 'favorite_activity': 'cuddling'}


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