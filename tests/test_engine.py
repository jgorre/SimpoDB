import pytest
import shutil
import random
import pathlib

from sql_engine.engine import DatabaseEngine

from sql_engine.engine import DatabaseEngine
from sql_engine.config.config import Config

TEST_DATA_PATH = "./test/data"

def reset_config():
    Config._instance = None

def prepare_persons_table(database_engine):
    person_value_batches = [
        "('Alice', 'painting', 34),('Bob', 'cycling', 29),('Cathy', 'photography', 25),('David', 'hiking', 32)",
        "('Eva', 'reading', 28),('Frank', 'cooking', 31),('Grace', 'gardening', 40),('Henry', 'swimming', 22),('Ivy', 'dancing', 26)",
        "('Jack', 'fishing', 35),('Karen', 'knitting', 37),('Leo', 'running', 30),('Mona', 'yoga', 33),('Nate', 'gaming', 24),('Olivia', 'traveling', 27)",
        "('Paul', 'writing', 29),('Quincy', 'woodworking', 38),('Rachel', 'bird watching', 41),('Sam', 'tennis', 23),('Tina', 'surfing', 36),('Uma', 'scuba diving', 34),('Victor', 'guitar', 29),('Wendy', 'baking', 25),('Xander', 'archery', 32),('Yara', 'singing', 28),('Zane', 'skiing', 31),('Amy', 'pottery', 40),('Brian', 'rock climbing', 22),('Cara', 'chess', 26),('Derek', 'camping', 35),('Ella', 'scrapbooking', 37)",
        "('Finn', 'kayaking', 30),('Gina', 'horseback riding', 33),('Hank', 'bird watching', 24)",
        "('Iris', 'jogging', 27),('Jake', 'drumming', 29),('Kara', 'quilting', 38),('Liam', 'painting', 41)",
        "('Mia', 'snowboarding', 23),('Noah', 'skateboarding', 36)",
        "('Owen', 'fencing', 34),('Pia', 'calligraphy', 29),('Quinn', 'magic tricks', 25),('Rita', 'ice skating', 32)",
        "('Sean', 'flying drones', 28),('Tara', 'kitesurfing', 31),('Ursula', 'diving', 40),('Vince', 'model building', 22),('Wade', 'metal detecting', 26),('Xena', 'embroidery', 35)",
        "('Yvonne', 'origami', 37),('Zach', 'boxing', 30),('Anna', 'pilates', 33),('Blake', 'geocaching', 24),('Clara', 'bird watching', 27),('Dean', 'puzzle solving', 29),('Eliza', 'knitting', 38),('Frankie', 'watercolor', 41)",
        "('George', 'trampolining', 23),('Holly', 'bowling', 36),('Ian', 'robotics', 34),('Jess', 'blogging', 29),('Kurt', 'crossfit', 25),('Lila', 'tattoo art', 32),('Mark', 'poetry', 28),('Nina', 'ceramics', 31),('Oscar', 'dog training', 40),('Penny', 'antiquing', 22),('Quentin', 'spelunking', 26),('Roxy', 'hiking', 35)",
        "('Stan', 'glass blowing', 37),('Tina', 'surfing', 30),('Ulysses', 'blacksmithing', 33),('Vera', 'hula hooping', 24),('Wyatt', 'model trains', 27),('Ximena', 'fencing', 29),('Yosef', 'yoga', 38),('Zoey', 'candle making', 41),('Aria', 'songwriting', 23),('Ben', 'jujitsu', 36),('Cora', 'sailing', 34),('Dylan', 'freediving', 29)",
        "('Eve', 'cheerleading', 25),('Felix', 'marathon running', 32),('Gwen', 'pottery', 28),('Harvey', 'chess', 31),('Ivy', 'dancing', 40),('John', 'reading', 22)",
        "('Kelly', 'bird watching', 26),('Landon', 'golfing', 35)",
        "('Mara', 'yoga', 37),('Nate', 'gaming', 30),('Opal', 'puzzles', 33),('Pete', 'skateboarding', 24)",
        "('Quinn', 'quilting', 27),('Rose', 'photography', 29),('Seth', 'sculpting', 38),('Tina', 'surfing', 41),('Uri', 'wood carving', 23)",
        "('Val', 'magic tricks', 36),('Willa', 'writing', 34),('Xavier', 'coding', 29),('Yara', 'singing', 25),('Zane', 'skiing', 32),('Anya', 'painting', 28)",
        "('Blake', 'rock climbing', 31),('Cleo', 'swimming', 40),('Dane', 'running', 22),('Ella', 'gardening', 26),('Finn', 'kayaking', 35),('Gia', 'knitting', 37),('Hugh', 'writing', 30),('Iris', 'jogging', 33),('Jake', 'drumming', 24),('Kara', 'quilting', 27),('Leo', 'running', 29),('Mona', 'yoga', 38),('Nina', 'ceramics', 41),('Owen', 'fencing', 23),('Pia', 'calligraphy', 36),('Quincy', 'magic tricks', 34),('Rita', 'ice skating', 29)",
        "('Sean', 'flying drones', 25),('Tara', 'kitesurfing', 32),('Ursula', 'diving', 28),('Victor', 'guitar', 31),('Wendy', 'baking', 40),('Xander', 'archery', 22),('Yvonne', 'origami', 26),('Zach', 'boxing', 35),('Amy', 'pottery', 37),('Brian', 'rock climbing', 30),('Cara', 'chess', 33)",
        "('Derek', 'camping', 24),('Eva', 'reading', 27),('Frank', 'cooking', 29),('Grace', 'gardening', 38),('Henry', 'swimming', 41),('Ivy', 'dancing', 23),('Jack', 'fishing', 36),('Karen', 'knitting', 34),('Leo', 'running', 29),('Mona', 'yoga', 25),('Nate', 'gaming', 32),('Olivia', 'traveling', 28),('Paul', 'writing', 31),('Quincy', 'woodworking', 40)",
        "('Rachel', 'bird watching', 22),('Sam', 'tennis', 26),('Tina', 'surfing', 35),('Uma', 'scuba diving', 37),('Victor', 'guitar', 30),('Wendy', 'baking', 33),('Xander', 'archery', 24),('Yara', 'singing', 27)",
        "('Zane', 'skiing', 29),('Alice', 'painting', 38),('Bob', 'cycling', 41),('Cathy', 'photography', 23),('David', 'hiking', 36),('Eva', 'reading', 34),('Frank', 'cooking', 29),('Grace', 'gardening', 25),('Henry', 'swimming', 32),('Ivy', 'dancing', 28),('Jack', 'fishing', 31),('Karen', 'knitting', 40),('Leo', 'running', 22),('Mona', 'yoga', 26),('Nate', 'gaming', 35)",
        "('Olivia', 'traveling', 37),('Paul', 'writing', 30),('Quincy', 'woodworking', 33),('Rachel', 'bird watching', 24),('Sam', 'tennis', 27),('Tina', 'surfing', 29),('Uma', 'scuba diving', 38),('Victor', 'guitar', 41),('Wendy', 'baking', 23),('Xander', 'archery', 36)",
        "('Yara', 'singing', 34),('Zane', 'skiing', 29),('Amy', 'pottery', 25),('Brian', 'rock climbing', 32),('Cara', 'chess', 28),('Derek', 'camping', 31),('Eva', 'reading', 40),('Frank', 'cooking', 22),('Grace', 'gardening', 26),('Henry', 'swimming', 35),('Ivy', 'dancing', 37),('Jack', 'fishing', 30),('Karen', 'knitting', 33)",
        "('Leo', 'running', 24),('Mona', 'yoga', 27),('Nate', 'gaming', 29),('Olivia', 'traveling', 38),('Paul', 'writing', 41),('Quincy', 'woodworking', 23),('Rachel', 'bird watching', 36),('Sam', 'tennis', 34),('Tina', 'surfing', 29),('Uma', 'scuba diving', 25),('Victor', 'guitar', 32),('Wendy', 'baking', 28),('Xander', 'archery', 31)",
        "('Yara', 'singing', 40),('Zane', 'skiing', 22),('Alice', 'painting', 26),('Bob', 'cycling', 35),('Cathy', 'photography', 37),('David', 'hiking', 30),('Eva', 'reading', 33),('Frank', 'cooking', 24)",
        "('Grace', 'gardening', 27),('Henry', 'swimming', 29),('Ivy', 'dancing', 38),('Jack', 'fishing', 41),('Karen', 'knitting', 23),('Leo', 'running', 36),('Mona', 'yoga', 34),('Nate', 'gaming', 29),('Olivia', 'traveling', 25),('Paul', 'writing', 32),('Quincy', 'woodworking', 28),('Rachel', 'bird watching', 31),('Sam', 'tennis', 40),('Tina', 'surfing', 22)"
    ]

    statements = []
    create_table_statement = 'create table persons (name string primary key, hobby string, age int)'

    statements.append(create_table_statement)
    for vals in person_value_batches:
        insert = f'insert into persons (name, hobby, age) values {vals}'
        statements.append(insert)

    for statement in statements:
        database_engine.process_command(statement)


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
        "data": {
            "path": TEST_DATA_PATH,
            "sstable_size": 50 # entries
        }
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
    result = list(database_engine.process_command(query))

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
    

def test_where_condition_operators(database_engine):
    prepare_persons_table(database_engine)

    query = 'select * from persons where age >= 20 and age < 30 and age != 27'
    res = database_engine.process_command(query)
    assert len(res) == 45

    bad_vals = [p for p in res if p['age'] < 20 or p['age'] >= 30 or p['age'] == 27]
    assert len(bad_vals) == 0

    query = "select * from persons where name = 'Zoey' or (age >= 20 and age < 30 and age != 27)"
    res = database_engine.process_command(query)
    assert len(res) == 46


def test_compaction(database_engine):
    create_table_statement = 'create table pplzz (name string primary key, recency string)'
    database_engine.process_command(create_table_statement)

    def insert_p(name, recency):
        return f"insert into pplzz (name, recency) values ('{name}', '{recency}')"
    
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

    pplzdir = pathlib.Path(TEST_DATA_PATH) / "pplzz" / "sstables"
    files_before_compaction = [f for f in pplzdir.glob("*")]
    assert len(files_before_compaction) == 5

    command = "compact pplzz"
    database_engine.process_command(command)

    files_after_compaction = [f for f in pplzdir.glob("*")]
    assert len(files_after_compaction) == 2

    # Check that vals are proper vals.
    query = "select * from pplzz"
    result = list(database_engine.process_command(query))

    assert len(result) == len(names)

    bad_vals = [val for val in result if val['recency'] != 'latest']

    assert len(bad_vals) == 0