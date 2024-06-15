import io
from pathlib import Path

from .schema import SchemaManager
from .entity import Entity
        

class ByteStreamProccessor:
    def __init__(self, table: str, binary_data_path: Path):
        self.table = table
        self.data_path = binary_data_path
        self.schema_manager = SchemaManager()

    def process(self, from_byte=None, until_byte=None):
        with open(self.data_path, 'rb') as file:
            self.buffer = io.BytesIO(file.read())

        if from_byte is not None:
            self.buffer.seek(from_byte)
        else:
            self.buffer.seek(0)
        
        until_byte = until_byte if until_byte is not None else len(self.buffer.getvalue())

        while self.buffer.tell() < until_byte:
            schema_version = self._decode_unsigned_int()
            schema = self.schema_manager.get_schema_with_version(self.table, schema_version)

            data = {}
            for column in schema['columns']:
                col_type = column['type']
                value = None
                if col_type == 'STRING':
                    value = self._decode_string()
                elif col_type == 'INT':
                    value = self._decode_signed_int()
                data[column['name']] = value

            primary_key = schema['primary_key']
            yield Entity(schema_version, primary_key, data)

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


def decode(table: str, file_path: Path, from_byte=None, until_byte=None):
    byte_processor = ByteStreamProccessor(table, file_path)
    yield from byte_processor.process(from_byte, until_byte)
