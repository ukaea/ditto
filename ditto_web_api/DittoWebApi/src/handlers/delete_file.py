# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties


class DeleteFileHandler(APIHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    @schema.validate(
        input_schema=create_object_schema_with_string_properties(["bucket", "file"], ["bucket", "file"]),
        input_example={
            "bucket": "test-bucket-name",
            "file": "path_to_file/file_name",
        },
        output_schema=create_object_schema_with_string_properties(["message", "file", "bucket"]),
        output_example={
            "message": "File path_to_file/file_name, successfully deleted from bucket test-bucket-name",
            "file": "path_to_file/file_name",
            "bucket": "test-bucket-name",
        }

    )
    def delete(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        file_name = attrs["file"]
        result = self._data_replication_service.try_delete_file(bucket_name, file_name)
        return result
