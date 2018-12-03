# pylint: disable=W0221,W0223
from tornado_json import schema, exceptions
from DittoWebApi.src.handlers.ditto_handler import DittoHandler
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties
from DittoWebApi.src.handlers.schemas.schema_helpers import create_transfer_output_schema


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
        dir_path = self.get_body_attribute("directory", default=None)
        result = self._data_replication_service.copy_dir(bucket_name, dir_path)
        exceptions.api_assert(result["message"] == "Transfer successful",
                              400,
                              result["message"])
        return result
