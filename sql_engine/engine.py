from pathlib import Path
import json

from .sql_parser.parse import parser
from .sql_types.sql_type_mapping import sql_type_mapping
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

# def manual_pack(integer, string):
#     # Ensure the string is exactly 4 characters (for simplicity)
#     string = string.ljust(4)[:4]  

#     # Convert integer to bytes
#     integer_bytes = bytes([
#         (integer >> 24) & 0xFF,  # Most significant byte
#         (integer >> 16) & 0xFF,
#         (integer >> 8) & 0xFF,
#         integer & 0xFF           # Least significant byte
#     ])

#     # Convert string to bytes
#     string_bytes = string.encode('utf-8')

#     # Concatenate byte data
#     return integer_bytes + string_bytes

# packed_data = manual_pack(1234, 'ABCD')
# print(f'Packed Data: {packed_data.hex()}')  # Using .hex() to show binary data in hex form