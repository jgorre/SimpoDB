from sql_engine.data_serialization.writer import ByteWriter

def test_encode_bytes():
    schema_version = 1
    writer = ByteWriter(schema_version)

    int1 = 5091
    str1 = 'mystring'
    int2 = 5

    writer.add_integer(int1)
    writer.add_string(str1)
    writer.add_integer(int2)

    encoded_bytes = writer.build()
    assert encoded_bytes == b'\x01\xc6O\x08mystring\n'