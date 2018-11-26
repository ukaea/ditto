from testScenarios.context import BaseSystemTest


class TestCopyUpdate(BaseSystemTest):
    def test_copy_update(self):
        # Start the api
        self.given.ditto_web_api.is_started()

        # Try copy_dir before bucket is created
        self.when.copy_update_called_for_whole_directory()
        self.then.response_shows_warning_as_bucket_does_not_exist()

        # Create a bucket in s3
        self.given.standard_bucket_exists_in_s3()

        # try copy-update before directory formed
        self.when.copy_update_called_for_whole_directory()
        self.then.response_message_complains_directory_does_not_exist()

        # Create a basic file
        self.given.simple_test_file_is_setup()

        # Copy whole directory to s3 bucket
        self.when.copy_update_called_for_whole_directory()
        self.then.response_shows_request_was_completed_successfully()
        self.then.new_simple_file_exists_in_s3_bucket()

        # list present shows file in s3
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_request_was_completed_successfully()
        self.then.list_present_response_body_shows_simple_file_in_s3()

        # Failure for no new or updated file
        self.when.copy_update_called_for_whole_directory()
        self.then.response_shows_old_file_skipped()
        self.then.response_indicates_no_files_updated()
        self.then.response_indicates_no_new_file_uploaded()

        # new file created, old files updated
        self.given.update_simple_file()
        self.given.simple_sub_dir_with_test_file_is_setup()

        # Copy and update files
        self.when.copy_update_called_for_whole_directory()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_confirms_transfer()
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.response_message_body_indicates_one_file_updated()
        self.then.simple_file_content_is_updated_on_s3()

        # list present shows both files in s3
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_request_was_completed_successfully()
        self.then.list_present_response_body_shows_file_in_sub_dir_in_s3()
        self.then.list_present_response_body_shows_simple_file_in_s3()
