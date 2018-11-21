class SchemaBuilder:
    def create_object_schema(self, list_of_properties, required):
        return {"type": "object",
                "properties":
                    {property: {"type": "string"} for property in list_of_properties},
                "required": [property for property in required]
                }

    def create_list_present_schame(self):
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "objects": {"type": "array",
                            "items": self.create_object_schema(["object_name", "bucket_name"], [])
                            },
            },
        }

