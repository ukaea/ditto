# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
from DittoWebApi.src.handlers.schemas.schema_builder import SchemaBuilder

SCHEMA_BUILDER = SchemaBuilder()


class CopyNewHandler(APIHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    @schema.validate(
        input_schema=SCHEMA_BUILDER.create_object_schema_with_string_properties(["bucket", "directory"], ["bucket"]),
        input_example={
            "bucket": "test-bucket-name",
            "directory": "testdir/testsubdir",
        },
        output_schema=SCHEMA_BUILDER.create_transfer_output_schema(),
        output_example={
            "type": "object",
            "properties": {
                "message": "Transfer successful",
                "new files transferred": 1,
                "files updated": 0,
                "files skipped": 0,
                "data transferred (bytes)": 1000,
            }
        },
    )
    def post(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        dir_path = attrs["directory"] if "directory" in attrs.keys() else None
        result = self._data_replication_service.copy_new(bucket_name, dir_path)
        return result
