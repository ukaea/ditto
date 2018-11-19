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
            "type": "object",
            "items": {
                "properties": {
                    "message": {"type": "string"},
                    "objects": {"type": "array"},
                },
                "required": ["message", "objects"]
            }
        },
        output_example={
            "message": "objects retrieved successfully",
            "objects": ["testdir/file1.txt", "testdir/subdir/file2.txt"]
        },
    )
    def post(self, *args, **kwargs):
        attrs = dict(self.body)
        bucket_name = attrs["bucket"]
        dir_path = attrs["directory"] if "directory" in attrs.keys() else None
        object_dicts = self._data_replication_service.retrieve_object_dicts(bucket_name, dir_path)
        return object_dicts
