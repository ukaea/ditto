# pylint: disable=W0221,W0223
from tornado_json import schema, exceptions
from DittoWebApi.src.handlers.ditto_handler import DittoHandler
from DittoWebApi.src.handlers.schemas.schema_helpers import create_object_schema_with_string_properties


class DeleteFileHandler(DittoHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(["bucket", "file"], ["bucket", "file"]),
        input_example={
            "bucket": "test-bucket-name",
            "file": "path_to_file/file_name",
        },
        output_schema=create_object_schema_with_string_properties(["message", "file", "bucket"]),
        output_example={
            "message": "File path_to_file/file_name, successfully deleted from bucket test-bucket-name",
            "file": "path_to_file/file_name",
            "bucket": "test-bucket-name",
        }

    )
    def delete(self, *args, **kwargs):
        bucket_name = self.get_body_attribute("bucket", required=True)
        self.check_current_user_authorised_for_bucket(bucket_name)
        file_rel_path = self.get_body_attribute("file", required=True)
        result = self._data_replication_service.try_delete_file(bucket_name, file_rel_path)
        exceptions.api_assert("successfully deleted from bucket" in result["message"],
                              400,
                              result["message"])
        return result
