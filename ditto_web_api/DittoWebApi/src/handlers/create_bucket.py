# pylint: disable=W0221,W0223
from tornado_json import schema
from DittoWebApi.src.handlers.ditto_handler import DittoHandler
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties
from DittoWebApi.src.handlers.schemas.schema_helpers import create_bucket_input_schema


class CreateBucketHandler(DittoHandler):
    @schema.validate(
        input_schema=create_bucket_input_schema(),
        input_example={
            "type": "object",
            "properties": {
                "bucket": "test-bucket-name",
                "groups": ["group1", "group2"],
                "archive_root": "/path/to/archive_root",
                "data_root": "/path/to/data_root"
            },
        },
        output_schema=create_object_schema_with_string_properties(["message", "bucket"]),
        output_example={
            "message": "Bucket test-bucket-name created",
            "bucket": "test-bucket-name",

        }
    )
    def post(self, *args, **kwargs):
        self.check_current_user_is_admin()
        bucket_name = self.get_body_attribute("bucket", required=True)
        groups = self.get_body_attribute("groups", required=True, value_type=list)
        data_root = self.get_body_attribute("data_root", required=True)
        archive_root = self.get_body_attribute("archive_root", required=False)
        archive_root = data_root if archive_root is None else archive_root
        result = self._data_replication_service.create_bucket(bucket_name, groups, archive_root, data_root)
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
