from testScenarios.context import BaseSystemTest


class TestCopyDir(BaseSystemTest):
    def test_copy_dir_fails_when_no_bucket(self):
        # Start the api
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        # Try copy_dir before bucket is created
        self.when.authorised_copy_dir_called_for_whole_directory()

        self.then.response_shows_request_failed()
        self.then.response_status_is(404)
        self.then.standard_s3_bucket_does_not_exist()
        self.then.response_shows_warning_as_bucket_does_not_exist()

    def test_copy_dir_fails_for_empty_directory_into_bucket(self):
        # Create a bucket in s3
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        # try copy dir before directory formed
        self.when.authorised_copy_dir_called_for_whole_directory()

        self.then.response_shows_request_failed()
        self.then.response_status_is(404)

    def test_copy_dir_fails_when_tyring_to_access_data_outside_of_root_for_bucket(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.authorised_copy_dir_called_for_directory_up_from_root()

        self.then.response_shows_request_failed()
        self.then.response_status_is(403)

    def test_copy_dir_copies_whole_directory_into_s3_bucket(self):
        # Create a basic file
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        # Copy whole directory to s3 bucket
        self.when.authorised_copy_dir_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.simple_file_exists_in_s3_bucket()

    def test_copy_dir_copies_just_a_sub_dir_when_specified_as_argument(self):
        # Create a file in a sub-directory
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_sub_dir_with_test_file_exists_locally()

        # Copy sub-dir with copy-dir using directory argument
        self.when.authorised_copy_dir_called_for_sub_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.file_exists_in_sub_dir_of_s3_bucket()
        self.then.simple_file_does_not_exist_in_s3_bucket()

    def test_copy_dir_does_not_update_if_directory_already_exists_in_s3_bucket(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_test_file_exists_in_s3()

        self.when.authorised_copy_dir_called_for_whole_directory()

        self.then.response_indicates_no_new_file_uploaded()
        self.then.response_indicates_no_files_updated()
        self.then.response_shows_one_file_skipped()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)

    def test_copy_dir_fails_when_user_not_authorised_for_bucket(self):
        # Start the api
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        # Try to copy the bucket
        self.when.unauthorised_copy_dir_called_for_whole_directory()

        self.then.response_shows_failed_as_unauthorised()
        self.then.response_status_is(403)
        self.then.simple_file_does_not_exist_in_s3_bucket()

    def test_copy_dir_fails_when_authentication_is_not_valid(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.unauthenticated_copy_dir_called_for_whole_directory()

        self.then.response_fails_with_reason_authentication_required()
        self.then.response_status_is(401)

    def test_copy_dir_fails_when_authentication_credentials_not_provided(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.copy_dir_called_with_no_authorisation_credentials()

        self.then.response_fails_with_reason_authentication_required()
        self.then.response_status_is(401)

    def test_archive_file_is_created_when_copy_dir_called_for_whole_dir(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()

        self.when.authorised_copy_dir_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.archive_file_exists_in_archive_root_dir()
        self.then.simple_file_is_in_root_archive_file_as_new_upload()

    def test_seperate_archive_file_is_created_in_each_dir_when_copy_dir_called_for_whole_dir(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.simple_sub_dir_with_test_file_exists_locally()

        self.when.authorised_copy_dir_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.archive_file_exists_in_archive_root_dir()
        self.then.archive_file_exists_in_sub_dir_of_archive_root()
        self.then.simple_file_is_in_root_archive_file_as_new_upload()
        self.then.file_in_sub_dir_is_in_archive_in_sub_dir_as_new_upload()

    def test_when_archive_file_exists_it_is_not_copied_but_is_updated(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_locally()
        self.given.archive_file_already_exists_in_local_root()

        self.when.authorised_copy_dir_called_for_whole_directory()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.response_message_body_indicates_one_new_file_uploaded()
        self.then.archive_file_exists_in_archive_root_dir()
        self.then.archive_file_does_not_exist_in_s3_bucket()
        self.then.archive_file_has_been_updated()
        self.then.simple_file_exists_in_s3_bucket()
