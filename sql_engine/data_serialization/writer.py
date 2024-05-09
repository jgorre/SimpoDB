from ..constants import DATA_PATH
from .schema import get_latest_schema

class Writer:
    def __init__(self, table):
        schema = get_latest_schema(table)
        self._table = table
        self._byte_writer = ByteWriter(schema['version'])

    def write(self, values: list[list[object]]):
        encoded_values = b''
        for value_list in values:
            for value in value_list:
                if isinstance(value, str):
                    self._byte_writer.add_string(value)
                elif isinstance(value, int):
                    self._byte_writer.add_integer(value)
                else:
                    raise ValueError(f"Unsupported type found while compiling bytes: {type(value)}. Value: {value}")
            
            value_bytes = self._byte_writer.build()
            encoded_values += value_bytes
            self._byte_writer.reset_bytes()

        data_path = DATA_PATH / self._table / 'data'
        with open(data_path, 'ab') as file:
            file.write(encoded_values)


class ByteWriter:
    def __init__(self, schema_version: int):
        self._schema_version_bytes = self._get_schema_version_bytes(schema_version)
        self.bytes = self._schema_version_bytes

    def _get_schema_version_bytes(self, schema_version: int):
        if schema_version == 0:
            return bytes([0x00])

        bits_remaining = schema_version.bit_length()
        encoded_bytes = []
        bit_offset = 0
        while bits_remaining > 0:
            bits = schema_version >> bit_offset
            bits = bits & 0b1111111

            bits_remaining -= 7

            if bits_remaining > 0:
                bits = bits | 128
                bit_offset += 7

            encoded_bytes.append(bits)

        return bytes(encoded_bytes)

    def add_string(self, string: str):
        encoded_string = string.encode('utf-8')
        num_bytes = len(encoded_string)

        bytes_list = []
        while True:
            byte = num_bytes & 0x7F
            num_bytes >>= 7
            if num_bytes != 0:
                byte |= 0x80

            bytes_list.append(byte)
            if num_bytes == 0:
                break

        self.bytes += bytes(bytes_list)
        self.bytes += encoded_string

    def add_integer(self, integer: int):
        is_negative = integer < 0

        first_byte = (integer & 0b00111111)
        first_byte <<= 1
        if is_negative:
            first_byte |= 0b00000001

        integer >>= 6

        if integer != 0:
            first_byte |= 0b10000000

        bytes_list = [first_byte]
        while integer > 0:
            byte = integer & 0x7F
            integer >>= 7
            if integer != 0:
                byte |= 0x80

            bytes_list.append(byte)

        self.bytes += bytes(bytes_list)

    def build(self):
        return self.bytes

    def reset_bytes(self):
        self.bytes = self._schema_version_bytes
