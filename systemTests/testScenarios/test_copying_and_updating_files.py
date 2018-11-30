import time
from testScenarios.context import BaseSystemTest


class TestCopyUpdate(BaseSystemTest):
    def test_copy_update_fails_when_bucket_does_not_exist(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authorised_copy_update_called_for_whole_directory()

        self.then.standard_s3_bucket_does_not_exist()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_shows_warning_as_bucket_does_not_exist()

    def test_copy_update_fails_when_no_file_in_directory(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.authorised_copy_update_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_reports_directory_does_not_exist()

    def test_copy_update_copies_across_whole_dir_that_is_new(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.authorised_copy_update_called_for_whole_directory()

        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.response_shows_request_was_completed_successfully()
        self.then.simple_file_exists_in_s3_bucket()

    def test_copy_update_transfers_no_data_when_all_files_are_present_and_up_to_date_in_s3(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_test_file_exists_in_s3()

        self.when.authorised_copy_update_called_for_whole_directory()

        self.then.response_shows_one_file_skipped()
        self.then.response_indicates_no_files_updated()
        self.then.response_indicates_no_new_file_uploaded()

    def test_copy_update_updates_relevant_files_and_transfers_new_files(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_test_file_exists_in_s3()
        self.given.simple_sub_dir_with_test_file_exists_locally()
        time.sleep(1)
        self.given.simple_file_is_updated()

        self.when.authorised_copy_update_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_confirms_transfer()
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.response_message_body_indicates_one_file_updated()
        self.then.simple_file_content_is_updated_on_s3()

    def test_copy_update_fails_when_authentication_is_invalid(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.unauthenticated_copy_update_called_for_whole_directory()

        self.then.response_fails_with_reason_authentication_required()

    def test_copy_update_fails_when_authentication_credentials_are_missing(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.copy_update_called_with_no_authorisation_credentials()

        self.then.response_fails_with_reason_authentication_required()

    def test_archive_file_is_created_when_copy_update_called_for_whole_dir(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.authorised_copy_update_called_for_whole_directory()

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

        self.when.authorised_copy_update_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.archive_file_exists_in_root_dir()
        self.then.archive_file_does_not_exist_in_s3_bucket()
        self.then.updated_archive_file_content_is_as_expected()
        self.then.simple_file_exists_in_s3_bucket()
