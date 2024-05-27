import pytest
import shutil

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

def test_setup(database_engine):
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

    query = "select * from pups where name = 'luna'"
    database_engine.process_command(query)