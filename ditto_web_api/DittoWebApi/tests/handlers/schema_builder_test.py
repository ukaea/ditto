import pytest
from DittoWebApi.src.handlers.schemas.schema_builder import SchemaBuilder


class TestSchemaBuilder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.schema_builder = SchemaBuilder()

    def test_create_object_schema_with_string_properties_returns_schema_with_all_properties_with_none_required(self):
        # Arrange
        properties = ["name", "bucket", "message", "file"]
        # Act
        schema = self.schema_builder.create_object_schema_with_string_properties(properties)
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
        properties = ["name", "bucket", "message", "file"]
        required = ["bucket", "file"]
        # Act
        schema = self.schema_builder.create_object_schema_with_string_properties(properties, required)
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

    def test_create_object_schema_creates_blank_properties_section_when_none_given(self):
        # Arrange
        properties = []
        # Act
        schema = self.schema_builder.create_object_schema_with_string_properties(properties)
        # Assert
        assert schema == {"type": "object",
                          "properties": {},
                          }

    def test_create_list_present_output_schema(self):
        # Act
        schema = self.schema_builder.create_list_present_output_schema()
        # Assert
        assert schema == {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "objects": {"type": "array",
                            "items": {
                                "type": "object",
                                "properties":
                                    {
                                        "object": {"type": "string"},
                                        "bucket": {"type": "string"},
                                    },
                            },
                            },
            },
        }
