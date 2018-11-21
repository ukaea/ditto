class SchemaBuilder:
    def create_object_schema_with_string_properties(self, list_of_properties, required=None):
        if required is None:
            return {"type": "object",
                    "properties":
                        {property: {"type": "string"} for property in list_of_properties},
                    }
        return {"type": "object",
                "properties":
                    {property: {"type": "string"} for property in list_of_properties},
                "required": [property for property in required]
                }

    def create_list_present_output_schema(self):
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "objects": {"type": "array",
                            "items": self.create_object_schema_with_string_properties(["object_name", "bucket_name"])
                            },
            },
        }

    def create_copy_output_schema(self):
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "new files transferred": {"type": "integer"},
                "files updated": {"type": "integer"},
                "files skipped": {"type": "integer"},
                "data transferred (bytes)": {"type": "integer"},
            }
        }

