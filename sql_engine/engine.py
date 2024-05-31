from .sql_parser.parse import parser
from .commands.sql_command import SqlCommand
from .storage.storage import TableStorage
from .config.config import Config



def handle_sql_command(sql: SqlCommand):
    return sql.execute()

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
    def __init__(self, config) -> None:
        # Fix this hackiness
        Config().initialize(config)
        db_config = Config()
        if not db_config.data_path.exists():
            db_config.data_path.mkdir(parents=True)

        TableStorage().do_startup_initialization()

    def process_command(self, command: str):
        parsed_sql_command = parser.parse(command)
        return handle_sql_command(parsed_sql_command)