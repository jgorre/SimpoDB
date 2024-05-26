from .sql_parser.parse import parser
from .commands.sql_command import SqlCommand
from .storage.storage import TableStorage
from .config.config import Config



def handle_sql_command(sql: SqlCommand):
    sql.execute()

def run():
    TableStorage().do_startup_initialization()
    while True:
        try:
            s = input('sql_command > ')
        except EOFError:
            break
        if not s: 
            continue
        
        parsed_sql_command = parser.parse(s)
        handle_sql_command(parsed_sql_command)


class DatabaseEngine:
    def __init__(self, config: Config) -> None:
        TableStorage().do_startup_initialization()

    def process_command(self, command: str):
        parsed_sql_command = parser.parse(command)
        handle_sql_command(parsed_sql_command)