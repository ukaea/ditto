from DittoWebApi.src.handlers.schemas.schema_builder import SchemaBuilder

class TestSchemaBuilder:
    def test_create_object_schema_with_string_properties_returns_schema_with_all_properties_with_none_required(self):
        # Arrange
        schema_builder = SchemaBuilder()
        properties = ["name", "bucket", "message", "file"]
        # Act
        schema = schema_builder.create_object_schema_with_string_properties(properties)
        # Assert
        assert schema == {"type": "object",
                          "properties": {
                              "name": {"type": "string"},
                              "bucket": {"type": "string"},
                              "message": {"type": "string"},
                              "file": {"type": "string"}
                          },
                          }

    def test_create_object_schema_with_string_properties_returns_schema_with_all_properties_with_correct_required(self):
        # Arrange
        schema_builder = SchemaBuilder()
        properties = ["name", "bucket", "message", "file"]
        required = ["bucket", "file"]
        # Act
        schema = schema_builder.create_object_schema_with_string_properties(properties, required)
        # Assert
        assert schema == {"type": "object",
                          "properties": {
                              "name": {"type": "string"},
                              "bucket": {"type": "string"},
                              "message": {"type": "string"},
                              "file": {"type": "string"}
                          },
                          "required": ["bucket", "file"]
                          }
