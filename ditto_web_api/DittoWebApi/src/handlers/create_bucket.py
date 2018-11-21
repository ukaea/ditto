# pylint: disable=W0221,W0223
from DittoWebApi.src.handlers.schemas.schema_builder import SchemaBuilder
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema

schema_builder = SchemaBuilder()


class CreateBucketHandler(APIHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    @schema.validate(
        input_schema=schema_builder.create_object_schema_with_string_properties(["bucket"], ["bucket"]),
        input_example={
            "type": "object",
            "properties": {
                "bucket": {"type": "string"}
            },
        },
        output_schema=schema_builder.create_object_schema_with_string_properties(["message", "bucket"]),
        output_example={
            "type": "object",
            "properties": {
                "message": "Bucket test-bucket-name created",
                "bucket": "test-bucket-name",
            }
        }
    )
    def post(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        result = self._data_replication_service.create_bucket(bucket_name)
        return result
