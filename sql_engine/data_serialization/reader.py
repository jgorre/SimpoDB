import io
from pathlib import Path

from .schema import get_all_schemas
        

class ByteStreamProccessor:
    def __init__(self, table: str, binary_data_path: Path):
        self.table = table
        self.data_path = binary_data_path
        self.schemas = get_all_schemas(table) # temporary solution. Just pre-emptively load in all schemas.

    def process(self):
        with open(self.data_path, 'rb') as file:
            self.buffer = io.BytesIO(file.read())

        self.buffer.seek(0)
        
        while self.buffer.tell() < len(self.buffer.getvalue()):
            schema_version = self._decode_unsigned_int()
            schema = self.schemas[str(schema_version)]

            entity = {}
            for column in schema['columns']:
                col_type = column['type']
                value = None
                if col_type == 'STRING':
                    value = self._decode_string()
                elif col_type == 'INT':
                    value = self._decode_signed_int()
                entity[column['name']] = value
            yield entity

    def _decode_string(self):
        str_length = self._decode_unsigned_int()
        return self.buffer.read(str_length).decode('utf-8')

    def _decode_unsigned_int(self):
        unsigned_int = 0
        shift_amount = 0
        while True:
            byte = int.from_bytes(self.buffer.read(1), 'little')
            unsigned_int = unsigned_int | (byte & 0x7F) << shift_amount
            shift_amount += 7
            if not (byte & 0x80):
                break
        
        return unsigned_int
    
    def _decode_signed_int(self):
        result = 0
        shift_amount = 0
        first_byte = True
        is_negative = False

        while True:
            byte = int.from_bytes(self.buffer.read(1), 'little')
            if first_byte:
                is_negative = (byte & 0x01) == 1
                result |= ((byte & 0x7E) >> 1) << shift_amount
                shift_amount += 6
            else:
                result |= (byte & 0x7F) << shift_amount
                shift_amount += 7

            if not (byte & 0x80):
                break

            first_byte = False

        return -result if is_negative else result


def decode(table: str, file_path: Path):
    byte_processor = ByteStreamProccessor(table, file_path)
    yield from byte_processor.process()
