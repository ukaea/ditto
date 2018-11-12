# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema


class CopyDirHandler(APIHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "bucket": {"type": "string"},
                "directory": {"type": "string"},
            },
            "required": ["bucket"]
        },
        input_example={
            "bucket": "test-bucket-name",
            "directory": "testdir/testsubdir",
        },
        output_schema={
            "type": "object",
            "properties": {
                "Message": {"type": "string"},
                "Files transferred": {"type": "int"},
                "Files updated": {"type": "int"},
                "Files skipped": {"type": "int"},
                "Data transferred (bytes)": {"type": "int"},
            }
        },
        output_example={
            "type": "object",
            "properties": {
                "Message": "Transfer successful",
                "Files transferred": 1,
                "Files updated": 0,
                "Files skipped": 0,
                "Data transferred (bytes)": 1000,
            }
        },
    )
    def post(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        dir_path = attrs["directory"] if "directory" in attrs.keys() else None
        result = self._data_replication_service.copy_dir(bucket_name, dir_path)
        return result
