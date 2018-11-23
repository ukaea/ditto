from testScenarios.context import BaseSystemTest


class TestTemplate(BaseSystemTest):
    def test_copy_dir(self):
        # Start the api
        self.given.ditto_web_api.is_started()

        # Create a basic file
        self.given.simple_test_file_is_setup()

        # Create a bucket in s3
        response_1 = self.when.create_bucket_called_for_simple_bucket()

        self.then.simple_bucket_exists_in_s3(response_1)

        # Copy whole directory to s3 bucket
        response_2 = self.when.copy_dir_called_for_whole_directory()

        self.then.new_file_exists_in_s3_bucket()
        self.then.copy_dir_completed_successfully(response_2)

        # List files in s3 bucket to show new files
        response_3 = self.when.list_present_called_for_simple_bucket_whole_directory_structure()

        self.then.list_present_body_shows_newly_created_file(response_3)

        # Create a file in a sub-directory
        self.given.simple_sub_dir_with_test_file_is_setup()

        # Try to copy across the new file with copy dir without specifying directory
        response_4 = self.when.copy_dir_called_for_whole_directory()

        self.then.copy_dir_copied_no_new_files_as_already_exists(response_4)

        # Use copy_dir handler with sub_dir argument to copy across the new file
        response_5 = self.when.copy_dir_called_for_sub_directory()

        self.then.copy_dir_completed_successfully(response_5)
        self.then.response_message_confirms_transfer(response_5)
