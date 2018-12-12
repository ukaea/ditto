from testScenarios.context import BaseSystemTest


class CreateBucket(BaseSystemTest):
    def test_create_bucket_as_admin_succeeds_when_bucket_nonexistent(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started_without_bucket_settings()

        self.when.admin_create_bucket_called_for_simple_bucket()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.standard_s3_bucket_exists()
        self.then.bucket_settings_includes_standard_bucket()

    def test_create_bucket_as_admin_fails_when_bucket_exists_in_s3(self):
        self.given.s3_interface_is_running()
        self.given.standard_bucket_exists_in_s3()
        self.given.ditto_web_api.is_started_without_bucket_settings()

        self.when.admin_create_bucket_called_for_simple_bucket()

        self.then.response_shows_request_failed()
        self.then.response_status_is(400)
        self.then.standard_s3_bucket_exists()
        self.then.bucket_settings_file_does_not_exist()

    def test_create_bucket_as_admin_fails_when_bucket_exists_in_bucket_settings(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.admin_create_bucket_called_for_simple_bucket()

        self.then.response_shows_request_failed()
        self.then.response_status_is(400)
        self.then.standard_s3_bucket_does_not_exist()

    def test_create_bucket_fails_as_admin_when_invalid_name_given(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started_without_bucket_settings()

        self.when.admin_create_bucket_called_with_name('BAD')

        self.then.response_shows_error_that_bad_bucket_name_given()
        self.then.response_shows_request_failed()
        self.then.response_status_is(400)
        self.then.bucket_settings_file_does_not_exist()

    def test_create_bucket_as_non_admin_fails(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started_without_bucket_settings()

        self.when.authenticated_create_bucket_called_for_simple_bucket()

        self.then.response_shows_failed_as_not_admin()
        self.then.response_shows_request_failed()
        self.then.response_status_is(403)
        self.then.standard_s3_bucket_does_not_exist()
        self.then.bucket_settings_file_does_not_exist()

    def test_create_bucket_fails_when_invalid_authentication(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started_without_bucket_settings()

        self.when.unauthenticated_create_bucket_called_for_simple_bucket()

        self.then.response_fails_with_reason_authentication_required()
        self.then.response_status_is(401)
        self.then.standard_s3_bucket_does_not_exist()
        self.then.bucket_settings_file_does_not_exist()

    def test_create_bucket_fails_with_no_user_credentials_provided(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started_without_bucket_settings()

        self.when.create_bucket_called_for_simple_bucket_with_no_user_credentials()

        self.then.response_fails_with_reason_authentication_required()
        self.then.response_status_is(401)
        self.then.standard_s3_bucket_does_not_exist()
        self.then.bucket_settings_file_does_not_exist()


    def test_create_bucket_creates_archive_with_data_if_root_not_specified(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started_without_bucket_settings()

        self.when.admin_create_bucket_called_for_simple_bucket_without_archive_root()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_status_is(200)
        self.then.standard_s3_bucket_exists()
        self.then.bucket_settings_includes_standard_bucket_with_archive_root_in_data()
