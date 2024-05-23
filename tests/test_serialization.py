# from sql_engine.data_serialization.writer import ByteWriter
# from sql_engine.data_serialization.reader import ByteReader

# def make_schema(col_types: list[str]):
#     col_type_objects = [{ 'type': col_type } for col_type in col_types]
#     return {
#         'columns': col_type_objects
#     }

# def encode_values_with_writer(writer: ByteWriter, values: list):
#     col_types = []
#     for val in values:
#         if isinstance(val, str):
#             writer.add_string(val)
#             col_types.append('STRING')
#         elif isinstance(val, int):
#             writer.add_integer(val)
#             col_types.append('INT')
#         else:
#             raise ValueError(f'Unexpected type {type(val)} is not supported')
        
#     return (writer.build(), make_schema(col_types))

# def assert_expected_values_are_decoded(schema, encoded_bytes, values_to_encode):
#     reader = ByteReader()
#     decoded_values = reader.read_bytes(schema, encoded_bytes[1:])
#     assert decoded_values == values_to_encode

# def test_serialization():
#     schema_version = 1
#     writer = ByteWriter(schema_version)

#     values_to_encode = [1, 'str']

#     encoded_bytes, schema = encode_values_with_writer(writer, values_to_encode)

#     assert_expected_values_are_decoded(schema, encoded_bytes, values_to_encode)

# def test_serialization_big_int():
#     schema_version = 1
#     writer = ByteWriter(schema_version)

#     values_to_encode = [5506]

#     encoded_bytes, schema = encode_values_with_writer(writer, values_to_encode)

#     assert_expected_values_are_decoded(schema, encoded_bytes, values_to_encode)

# def test_serialization_big_int_and_big_str():
#     schema_version = 1
#     writer = ByteWriter(schema_version)

#     values_to_encode = [5506, 'a' * 367]

#     encoded_bytes, schema = encode_values_with_writer(writer, values_to_encode)

#     assert_expected_values_are_decoded(schema, encoded_bytes, values_to_encode)

