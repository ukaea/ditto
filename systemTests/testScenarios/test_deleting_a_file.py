from testScenarios.context import BaseSystemTest


class TestTemplate(BaseSystemTest):
    def test_delete_file(self):
        # Start the api
        self.given.ditto_web_api.is_started()

        # Create a bucket in s3
        self.given.standard_bucket_exists_in_s3()

        # Create a basic file in s3
        self.given.simple_test_file_is_setup()
        self.when.copy_dir_called_for_whole_directory()
        self.then.new_simple_file_exists_in_s3_bucket()
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.list_present_response_body_shows_simple_file_in_s3()

        # delete file
        self.when.delete_file_is_called_for_simple_file_in_s3()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_confirms_simple_file_deleted()
        self.then.simple_file_does_not_exist_in_s3_bucket()
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.list_present_response_body_shows_simple_file_not_in_s3()
