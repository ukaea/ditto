from testScenarios.context import BaseSystemTest


class TestListPresent(BaseSystemTest):
    def test_list_present_shows_warning_when_bucket_does_not_exist(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.list_present_called_for_simple_bucket_whole_directory_structure()

        self.then.standard_s3_bucket_does_not_exist()
        self.then.response_shows_warning_as_bucket_does_not_exist()

    def test_list_present_shows_content_of_directory(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_is_setup_in_s3()
        self.given.simple_sub_dir_with_test_file_is_setup_in_s3()

        self.when.list_present_called_for_simple_bucket_whole_directory_structure()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_body_shows_simple_file_in_s3()
        self.then.response_body_shows_file_in_sub_dir_in_s3()

    def test_list_present_shows_empty_bucket_when_no_files(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.list_present_called_for_simple_bucket_whole_directory_structure()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_shows_no_objects_in_bucket()
