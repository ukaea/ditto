def create_object_schema_with_string_properties(list_of_properties, required=None):
    if not list_of_properties:
        raise ValueError("No properties provided for the schema")
    schema = {"type": "object",
              "properties":
                  {property: {"type": "string"} for property in list_of_properties},
              }
    if required:
        schema["required"] = required
    return schema


def create_list_present_output_schema():
    return {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "objects": {"type": "array",
                        "items": create_object_schema_with_string_properties(["object", "bucket"])
                        },
        },
    }


def create_transfer_output_schema():
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
