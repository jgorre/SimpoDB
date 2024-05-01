from pathlib import Path

from ..constants import DATA_PATH

class Writer:
    def __init__(self):
        self._byte_writer = ByteWriter()

    def write(self, values: list[list[object]], table: str):
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

        data_path = DATA_PATH / table / 'data'
        with open(data_path, 'ab') as file:
            file.write(encoded_values)


class ByteWriter:
    def __init__(self):
        self.bytes = b''

    def add_string(self, string: str):
        encoded_string = string.encode('utf-8')
        num_bytes = len(encoded_string)

        if num_bytes > 255:
            raise ValueError('UTF-8 string greater than 255 bytes is not supported.')
        
        str_type_byte = 0x01.to_bytes()
        num_bytes_as_bytes = num_bytes.to_bytes()

        self.bytes += str_type_byte
        self.bytes += num_bytes_as_bytes
        self.bytes += encoded_string

    def add_integer(self, integer: int):
        integer_bytes = integer.to_bytes(4, 'big')
        int_type_byte = 0x02.to_bytes()

        self.bytes += int_type_byte
        self.bytes += integer_bytes

    def build(self):
        self.bytes += 0x00.to_bytes()
        return self.bytes

    def reset_bytes(self):
        self.bytes = b''
