from testScenarios.context import BaseSystemTest


class CreateBucket(BaseSystemTest):
    def test_create_bucket_succeeds(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authenticated_create_bucket_called_for_simple_bucket()

        self.then.response_shows_request_was_completed_successfully()
        self.then.standard_s3_bucket_exists()

    def test_create_bucket_fails_when_invalid_name_given(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authenticated_create_bucket_called_with_name('BAD')

        self.then.response_shows_error_that_bad_bucket_name_given()

    def test_create_bucket_fails_when_invalid_authentication(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.unauthenticated_create_bucket_called_for_simple_bucket()

        self.then.response_fails_with_reason_authentication_required()

    def test_create_bucket_fails_with_no_user_credentials_provided(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.create_bucket_called_for_simple_bucket_with_no_user_credentials()

        self.then.response_fails_with_reason_authentication_required()
