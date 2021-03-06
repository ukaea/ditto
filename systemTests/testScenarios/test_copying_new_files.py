from testScenarios.context import BaseSystemTest


class TestCopyNew(BaseSystemTest):
    def test_copy_new_fails_when_no_bucket(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.standard_s3_bucket_does_not_exist()
        self.then.response_status_is(404)
        self.then.response_shows_request_failed()
        self.then.response_shows_warning_as_bucket_does_not_exist()

    def test_copy_new_fails_when_no_dir_to_copy(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_status_is(404)
        self.then.response_shows_request_failed()
        self.then.response_data_reports_directory_does_not_exist()

    def test_copy_new_fails_when_tyring_to_access_data_outside_of_root_for_bucket(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.authorised_copy_new_called_for_directory_up_from_root()

        self.then.response_shows_request_failed()
        self.then.response_status_is(403)

    def test_copy_new_copies_whole_dir_not_on_s3_to_s3(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.simple_file_exists_in_s3_bucket()

    def test_copy_new_copies_no_files_when_none_are_new(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_test_file_exists_in_s3()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
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
        self.then.response_status_is(200)
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
        self.then.response_status_is(403)
        self.then.simple_file_does_not_exist_in_s3_bucket()

    def test_copy_new_fails_when_authentication_is_invalid(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.unauthenticated_copy_new_called_for_whole_directory()

        self.then.response_fails_with_reason_authentication_required()
        self.then.response_status_is(401)

    def test_copy_new_fails_when_authentication_credentials_are_missing(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.copy_new_called_with_no_authorisation_credentials()

        self.then.response_fails_with_reason_authentication_required()
        self.then.response_status_is(401)

    def test_archive_file_is_created_at_each_sub_dir_when_copy_new_called_for_whole_dir(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_sub_dir_with_test_file_exists_locally()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.archive_file_exists_in_archive_root_dir()
        self.then.archive_file_exists_in_sub_dir_of_archive_root()
        self.then.file_in_sub_dir_is_in_archive_in_sub_dir_as_new_upload()
        self.then.simple_file_is_in_root_archive_file_as_new_upload()
        self.then.archive_file_does_not_exist_in_s3_bucket()

    def test_when_archive_file_exists_it_is_not_copied_but_is_updated(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.archive_file_already_exists_in_local_root()
        self.given.old_transfer_in_archive_file()

        self.when.authorised_copy_new_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.archive_file_exists_in_archive_root_dir()
        self.then.archive_file_has_been_updated()
        self.then.simple_file_is_in_root_archive_file_as_new_upload()
        self.then.archive_file_does_not_exist_in_s3_bucket()
        self.then.simple_file_exists_in_s3_bucket()
        self.then.old_content_in_archive_file_is_untouched()
