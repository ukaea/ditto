from testScenarios.context import BaseSystemTest


class TestCopyDir(BaseSystemTest):
    def test_copy_dir(self):
        # Start the api
        self.given.ditto_web_api.is_started()

        # Create a basic file
        self.given.simple_test_file_is_setup()

        # Try copy_dir before bucket is created
        self.when.copy_dir_called_for_whole_directory()
        self.then.response_shows_warning_as_bucket_does_not_exist()

        # Create a bucket in s3
        self.given.standard_bucket_exists_in_s3()

        # Copy whole directory to s3 bucket
        self.when.copy_dir_called_for_whole_directory()
        self.then.response_shows_request_was_completed_successfully()
        self.then.new_simple_file_exists_in_s3_bucket()

        # Create a file in a sub-directory
        self.given.simple_sub_dir_with_test_file_is_setup()

        # Try to copy across the new file with copy dir without specifying directory
        self.when.copy_dir_called_for_whole_directory()
        self.then.response_shows_copy_dir_copied_no_new_files_as_directory_already_exists()

        # Copy sub-dir with copy-dir using directory argument
        self.when.copy_dir_called_for_sub_directory()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_body_indicates_one_new_file_uploaded()

        # List present shows both files in s3 bucket
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_request_was_completed_successfully()
        self.then.list_present_response_body_shows_returned_newly_created_file()
