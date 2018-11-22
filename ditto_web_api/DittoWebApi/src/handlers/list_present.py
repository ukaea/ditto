# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
from DittoWebApi.src.handlers.schemas.schema_builder import SchemaBuilder

SCHEMA_BUILDER = SchemaBuilder()


class ListPresentHandler(APIHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    @schema.validate(
        input_schema=SCHEMA_BUILDER.create_object_schema_with_string_properties(["bucket", "directory"], ["bucket"]),
        input_example={
            "bucket": "test-bucket-name",
            "directory": "testdir/testsubdir",
        },
        output_schema=SCHEMA_BUILDER.create_list_present_output_schema(),
        output_example={
            "message": "objects retrieved successfully",
            "objects": [{"object": "testdir/file1.txt", "bucket": "test_bucket_1"},
                        {"object": "testdir/subdir/file2.txt", "bucket": "test_bucket_1"}]
        },
    )
    def post(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        dir_path = attrs["directory"] if "directory" in attrs.keys() else None
        object_dicts = self._data_replication_service.retrieve_object_dicts(bucket_name, dir_path)
        return object_dicts
