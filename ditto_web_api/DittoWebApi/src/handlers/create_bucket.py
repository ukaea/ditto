# pylint: disable=W0221,W0223
from tornado_json import schema, exceptions
from DittoWebApi.src.handlers.ditto_handler import DittoHandler
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties


class CreateBucketHandler(DittoHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(["bucket"], ["bucket"]),
        input_example={
            "type": "object",
            "properties": {
                "bucket": {"type": "string"}
            },
        },
        output_schema=create_object_schema_with_string_properties(["message", "bucket"]),
        output_example={
            "message": "Bucket test-bucket-name created",
            "bucket": "test-bucket-name",

        }
    )
    def post(self, *args, **kwargs):
        bucket_name = self.get_body_attribute("bucket", required=True)
        result = self._data_replication_service.create_bucket(bucket_name)
        exceptions.api_assert("Bucket Created" in result["message"],
                              400,
                              result["message"])
        return result
