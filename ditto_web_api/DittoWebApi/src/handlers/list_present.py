# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema


class ListPresentHandler(APIHandler):
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
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "object_name": {"type": "string"},
                    "bucket_name": {"type": "string"},
                },
                "required": ["object_name", "bucket_name"]
            }
        },
        output_example=[
            {
                "object_name": "testdir/file1.txt",
                "bucket_name": "test-bucket-name"
            },
            {
                "object_name": "testdir/subdir/file2.txt",
                "bucket_name": "test-bucket-name"
            }
        ],
    )
    def post(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        dir_path = attrs["directory"] if "directory" in attrs.keys() else None
        object_dicts = self._data_replication_service.retrieve_object_dicts(bucket_name, dir_path)
        return object_dicts
