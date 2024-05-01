from .sql_parser.parse import parser
from .commands.sql_command import SqlCommand


def handle_sql_command(sql: SqlCommand):
    sql.execute()

def run():
    while True:
        try:
            s = input('sql_command > ')
        except EOFError:
            break
        if not s: continue
        parsed_sql_command = parser.parse(s)
        handle_sql_command(parsed_sql_command)
