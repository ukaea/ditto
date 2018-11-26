from testScenarios.context import BaseSystemTest


class TestCopyNew(BaseSystemTest):
    def test_copy_new(self):
        # Start the api
        self.given.ditto_web_api.is_started()

        # Try copy_new before bucket is created
        self.when.copy_new_called_for_whole_directory()
        self.then.response_shows_warning_as_bucket_does_not_exist()

        # Create a bucket in s3
        self.given.standard_bucket_exists_in_s3()

        # Try copy_new_ when directory doesn't exist
        self.when.copy_new_called_for_whole_directory()
        self.then.response_message_complains_directory_does_not_exist()

        # Create a basic file
        self.given.simple_test_file_is_setup()
        # Copy whole directory to s3 bucket
        self.when.copy_new_called_for_whole_directory()
        self.then.response_shows_request_was_completed_successfully()
        self.then.new_simple_file_exists_in_s3_bucket()

        # list present shows file in s3
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_request_was_completed_successfully()
        self.then.list_present_response_body_shows_simple_file_in_s3()

        # Failure for no new file
        self.when.copy_new_called_for_whole_directory()
        self.then.response_shows_old_file_skipped()

        # Create new file in subdir
        self.given.simple_sub_dir_with_test_file_is_setup()

        # Copy new copies new file across
        self.when.copy_new_called_for_whole_directory()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_confirms_transfer()
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.response_shows_old_file_skipped()
        self.then.new_file_exists_in_sub_dir_of_s3_bucket()

        # list present shows both files in s3
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_request_was_completed_successfully()
        self.then.list_present_response_body_shows_simple_file_in_s3()
        self.then.list_present_response_body_shows_file_in_sub_dir_in_s3()
