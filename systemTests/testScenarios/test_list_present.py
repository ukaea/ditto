from testScenarios.context import BaseSystemTest


class TestListPresent(BaseSystemTest):
    def test_list_present(self):
        # Start the api
        self.given.ditto_web_api.is_started()

        # Try list present for invalid bucket
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_warning_as_bucket_does_not_exist()

        # Create bucket
        self.given.standard_bucket_exists_in_s3()

        # list present returns no items in empty bucket
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_no_objects_in_bucket()

        # Create file
        self.given.simple_test_file_is_setup()
        self.when.copy_dir_called_for_whole_directory()
        self.when.list_present_called_for_simple_bucket_whole_directory_structure()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_body_shows_simple_file_in_s3()
