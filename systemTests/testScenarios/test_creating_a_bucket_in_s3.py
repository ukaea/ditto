from testScenarios.context import BaseSystemTest


class CreateBucket(BaseSystemTest):
    def test_creating_a_bucket(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authorised_create_bucket_called_for_simple_bucket()

        self.then.response_shows_request_was_completed_successfully()
        self.then.simple_bucket_exists_in_s3()

    def test_trying_to_create_a_bucket_with_invalid_name(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authorised_create_bucket_called_with_name('BAD')

        self.then.response_shows_error_that_bad_bucket_name_given()
