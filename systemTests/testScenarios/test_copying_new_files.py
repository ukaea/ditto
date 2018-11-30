from testScenarios.context import BaseSystemTest


class TestCopyNew(BaseSystemTest):
    def test_copy_new_fails_when_no_bucket(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.standard_s3_bucket_does_not_exist()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_shows_warning_as_bucket_does_not_exist()

    def test_copy_new_fails_when_no_dir_to_copy(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_reports_directory_does_not_exist()

    def test_copy_new_copies_whole_dir_not_on_s3_to_s3(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.response_shows_request_was_completed_successfully()
        self.then.simple_file_exists_in_s3_bucket()

    def test_copy_new_copies_no_files_when_none_are_new(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_test_file_exists_in_s3()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_shows_one_file_skipped()

    def test_copy_new_copies_only_new_files_when_new_and_old_exist(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_test_file_exists_in_s3()
        self.given.simple_sub_dir_with_test_file_exists_locally()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_confirms_transfer()
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.response_shows_one_file_skipped()
        self.then.file_exists_in_sub_dir_of_s3_bucket()

    def test_copy_new_fails_when_user_not_authorised_for_bucket(self):
        # Start the api
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        # Try to copy the bucket
        self.when.unauthorised_copy_new_called_for_whole_directory()

        self.then.response_shows_failed_as_unauthorised()
        self.then.simple_file_does_not_exist_in_s3_bucket()

    def test_copy_new_fails_when_authentication_is_invalid(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.unauthenticated_copy_new_called_for_whole_directory()

        self.then.response_fails_with_reason_authentication_required()

    def test_copy_new_fails_when_authentication_credentials_are_missing(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.copy_new_called_with_no_authorisation_credentials()

        self.then.response_fails_with_reason_authentication_required()

    def test_archive_file_is_created_when_copy_new_called_for_whole_dir(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.archive_file_exists_in_root_dir()
        self.then.archive_content_is_as_expected()

    def test_when_archive_file_exists_it_is_not_copied_but_is_updated(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.archive_file_already_exists_in_local_root()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.archive_file_exists_in_root_dir()
        self.then.archive_file_does_not_exist_in_s3_bucket()
        self.then.updated_archive_file_content_is_as_expected()
        self.then.simple_file_exists_in_s3_bucket()

