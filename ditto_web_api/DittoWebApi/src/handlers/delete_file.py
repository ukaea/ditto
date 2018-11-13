# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema


class DeleteFileHandler(APIHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "bucket": {"type": "string"},
                "file": {"type": "string"},
            },
            "required": ["bucket", "file"]
        },
        input_example={
            "bucket": "test-bucket-name",
            "file": "path_to_file/file_name",
        },
        output_schema={
            "type": "object",
            "properties": {
                "Message": {"type": "string"},
                "File attempted to delete": {"type": "string"},
                "Bucket containing file": {"type": "string"},
            }
        },
        output_example={
            "type": "object",
            "properties": {
                "Message": "File path_to_file/file_name, successfully deleted from bucket test-bucket-name",
                "File attempted to delete": "path_to_file/file_name",
                "Bucket containing file": "test-bucket-name",
            }
        }
    )
    def delete(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        file_name = attrs["file"]
        result = self._data_replication_service.try_delete_file(bucket_name, file_name)
        return result
