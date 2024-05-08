from sql_engine.data_serialization.writer import ByteWriter
from sql_engine.data_serialization.reader import ByteReader

def test_decode_str():
    reader = ByteReader()
    schema = {
        'columns': [
            { 
                'type': 'STRING' 
            }
        ] 
    }
    encoded_value = b'\x07teststr'
    decoded_value = reader.read_bytes(schema, encoded_value)
    assert decoded_value == ['teststr']

def test_decode_large_str():
    reader = ByteReader()
    schema = {
        'columns': [
            { 
                'type': 'STRING' 
            }
        ] 
    }
    
    a_256_times = ('a' * 256)
    encoded_long_str = b'\x80\x02' + a_256_times.encode()
    decoded_value = reader.read_bytes(schema, encoded_long_str)
    assert decoded_value == [a_256_times]
