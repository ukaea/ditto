# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema


class CopyNewHandler(APIHandler):
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
                "message": {"type": "string"},
                "new files transferred": {"type": "integer"},
                "files updated": {"type": "integer"},
                "files skipped": {"type": "integer"},
                "data transferred (bytes)": {"type": "integer"},
            }
        },
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
        result = self._data_replication_service.copy_new_with_optional_updates(bucket_name,
                                                                               dir_path,
                                                                               check_for_update=False)
        return result
