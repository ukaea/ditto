# pylint: disable=W0221,W0223
from tornado_json import schema, exceptions
from DittoWebApi.src.handlers.ditto_handler import DittoHandler
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties
from DittoWebApi.src.handlers.schemas.schema_helpers import create_transfer_output_schema
from DittoWebApi.src.utils.messages import positive_responses


class CopyDirHandler(DittoHandler):
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
        bucket_name = self.get_body_attribute("bucket", required=True)
        self.check_current_user_authorised_for_bucket(bucket_name)
        dir_path = self.get_body_attribute("directory", default=None)
        result = self._data_replication_service.copy_dir(bucket_name, dir_path)
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
