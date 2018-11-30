from testScenarios.context import BaseSystemTest


class TestDeleteFile(BaseSystemTest):
    def test_delete_file_fails_when_bucket_does_not_exist(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()

        self.when.authorised_delete_file_is_called_for_simple_file_in_s3()

        self.then.standard_s3_bucket_does_not_exist()
        self.then.response_shows_request_was_completed_successfully()
        self.then.response_shows_warning_as_bucket_does_not_exist()

    def test_delete_file_removes_simple_file_from_s3(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()
        self.given.simple_test_file_exists_in_s3()

        self.when.authorised_delete_file_is_called_for_simple_file_in_s3()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_confirms_simple_file_deleted()
        self.then.simple_file_does_not_exist_in_s3_bucket()

    def test_delete_file_fails_when_file_does_not_exist(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.authorised_delete_file_is_called_for_simple_file_in_s3()

        self.then.response_shows_request_was_completed_successfully()
        self.then.response_message_reports_simple_file_does_not_exist()

    def test_delete_file_is_rejected_when_authentication_is_invalid(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.unauthenticated_delete_file_is_called_for_simple_file_in_s3()

        self.then.response_fails_with_reason_authentication_required()

    def test_delete_file_is_rejected_when_authentication_credentials_are_not_provided(self):
        self.given.s3_interface_is_running()
        self.given.ditto_web_api.is_started()
        self.given.standard_bucket_exists_in_s3()

        self.when.delete_file_called_with_no_authorisation_credentials()

        self.then.response_fails_with_reason_authentication_required()
