

class ByteReader:
    def read_bytes(self, schema, bytez: bytes):
        self.byte_index = 0
        self.bytez = bytez

        values = []
        for column in schema['columns']:
            col_type = column['type']
            if col_type == 'STRING':
                values.append(self._decode_string())
            elif col_type == 'INT':
                values.append(self._decode_int())

        return values

    def _decode_string(self):
        str_length = self._decode_str_length()
        start = self.byte_index
        end = self.byte_index + str_length
        self.byte_index = end
        return self.bytez[start:end].decode('utf-8')

    def _decode_str_length(self):
        str_length = 0
        shift_amount = 0
        for byte in self.bytez:
            str_length |= (byte & 0x7F) << shift_amount
            shift_amount += 7
            self.byte_index += 1
            if not (byte & 0x80):
                break
        
        return str_length
