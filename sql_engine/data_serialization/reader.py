from pathlib import Path

from ..constants import DATA_PATH

class ByteReader:
    def __init__(self):
        self.bytes = b''


    def get_values(self, table: str, meets_condition=lambda v: True):
        table_path = DATA_PATH / table
        table_data_path = table_path / 'data'
        
        bytestr = self._read_bytes(table_data_path)

        if bytestr is None:
            return []

        val_type_index = 0
        all_values = []
        item_values = []
        while True:
            val_type = bytestr[val_type_index]
            
            if val_type == 1:
                string_length = bytestr[val_type_index + 1]
                str_start_index = val_type_index + 2
                str_end_index = str_start_index + string_length
                string_bytes = bytestr[str_start_index:str_start_index+string_length]
                string = string_bytes.decode('utf-8')
                item_values.append(string)
                val_type_index = str_end_index
            elif val_type == 2:
                int_length = 4
                int_start_index = val_type_index + 1
                int_end_index = int_start_index + int_length
                int_bytes = bytestr[int_start_index:int_start_index+int_length]
                integer = int.from_bytes(int_bytes, byteorder='big')
                item_values.append(integer)
                val_type_index = int_end_index
            elif val_type == 0:
                if meets_condition(item_values):
                    all_values.append(item_values.copy())
                
                item_values.clear()
                val_type_index += 1
                if len(bytestr) <= val_type_index:
                    break
            else:
                raise ValueError(f'Bytes sketchy n borked {bytestr}. Got val_type = {val_type}')
            
        return all_values
    
    def _read_bytes(self, data_path: Path):
        if not data_path.exists():
            return None

        with open(data_path, 'rb') as data_file:
            data = data_file.read()
            return data
