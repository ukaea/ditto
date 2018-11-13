# pylint: disable=W0221,W0223
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema


class CreateBucketHandler(APIHandler):
    def initialize(self, data_replication_service):
        self._data_replication_service = data_replication_service

    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "bucket": {"type": "string"},
            },
            "required": ["bucket"]
        },
        input_example={
            "bucket": "test-bucket-name",
        },
        output_schema={
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "bucket": {"type": "string"},
            }
        },
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
