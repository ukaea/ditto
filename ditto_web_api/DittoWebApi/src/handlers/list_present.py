# pylint: disable=W0221,W0223
from tornado_json import schema, exceptions
from DittoWebApi.src.handlers.ditto_handler import DittoHandler
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties
from DittoWebApi.src.handlers.schemas.schema_helpers import create_list_present_output_schema


class ListPresentHandler(DittoHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(["bucket", "directory"], ["bucket"]),
        input_example={
            "bucket": "test-bucket-name",
            "directory": "testdir/testsubdir",
        },
        output_schema=create_list_present_output_schema(),
        output_example={
            "message": "objects retrieved successfully",
            "objects": [{"object": "testdir/file1.txt", "bucket": "test_bucket_1"},
                        {"object": "testdir/subdir/file2.txt", "bucket": "test_bucket_1"}]
        },
    )
    def post(self, *args, **kwargs):
        bucket_name = self.get_body_attribute("bucket", required=True)
        dir_path = self.get_body_attribute("directory", default=None)
        result = self._data_replication_service.retrieve_object_dicts(bucket_name, dir_path)
        exceptions.api_assert(result["message"] == "objects returned successfully",
                              404,
                              result["message"])
        return result
