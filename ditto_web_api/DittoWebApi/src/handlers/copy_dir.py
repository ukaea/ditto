# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties
from DittoWebApi.src.handlers.schemas.schema_helpers import create_transfer_output_schema


class CopyDirHandler(APIHandler):
    def initialize(self, data_replication_service, security_service):
        self._data_replication_service = data_replication_service
        self._security_service = security_service

    @schema.validate(
        input_schema=create_object_schema_with_string_properties(["bucket", "directory"], ["bucket"]),
        input_example={
            "bucket": "test-bucket-name",
            "directory": "testdir/testsubdir",
        },
        output_schema=create_transfer_output_schema(),
        output_example={
            "message": "Transfer successful",
            "new files transferred": 1,
            "files updated": 0,
            "files skipped": 0,
            "data transferred (bytes)": 1000,
        },
    )
    def post(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        dir_path = attrs["directory"] if "directory" in attrs.keys() else None
        result = self._data_replication_service.copy_dir(bucket_name, dir_path)
        return result
