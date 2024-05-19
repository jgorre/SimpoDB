import io
from pathlib import Path

from .schema import get_all_schemas
        

# def read_bytes(self, schema, bytez: bytes):
#     self.byte_index = 0
#     self.bytez = bytez

#     values = []
#     for column in schema['columns']:
#         col_type = column['type']
#         if col_type == 'STRING':
#             values.append(self._decode_string())
#         elif col_type == 'INT':
#             values.append(self._decode_signed_int())

#     return values


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

            for column in schema['columns']:
                col_type = column['type']
                print(col_type)
            break

    def _decode_string(self):
        str_length = self._decode_unsigned_int()
        start = self.byte_index
        end = self.byte_index + str_length
        self.byte_index = end
        return self.bytez[start:end].decode('utf-8')

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

        for byte in self._get_remaining_bytes():
            self.byte_index += 1
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

    def _get_remaining_bytes(self):
        return self.bytez[self.byte_index:]


def decode(table: str, file_path: Path):
    byte_processor = ByteStreamProccessor(table, file_path)
    byte_processor.process()
