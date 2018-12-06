from tornado.testing import gen_test

from DittoWebApi.src.handlers.delete_file import DeleteFileHandler
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class DeleteFileHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return DeleteFileHandler

    @property
    def standard_request_method(self):
        return 'DELETE'

    @property
    def standard_body(self):
        return {'bucket': "test-bucket", 'file': 'test.txt'}

    # Security

    @gen_test
    def test_delete_returns_401_when_no_credentials_given(self):
        yield self.assert_request_returns_401_when_no_credentials_given(self.standard_body)

    @gen_test
    def test_post_returns_401_when_invalid_credentials_given(self):
        yield self.assert_request_returns_401_when_invalid_credentials_given(self.standard_body)

    @gen_test
    def test_post_returns_403_when_user_is_unauthorised(self):
        yield self.assert_request_returns_403_when_unauthorised_user(self.standard_body)

    @gen_test
    def test_post_returns_404_when_bucket_nonexistent(self):
        yield self.assert_request_returns_404_when_unrecognised_bucket_named(self.standard_body)

    @gen_test
    def test_post_returns_200_when_credentials_accepted(self):
        self.mock_data_replication_service.try_delete_file.return_value = \
            return_delete_file_helper('success', 'test.txt', 'test.txr')
        yield self.assert_request_returns_200_when_credentials_accepted(self.standard_body)

    # Coupling with Data Replication Service

    @gen_test
    def test_delete_file_returns_summary_of_deleted_files_as_json_when_successful(self):
        # Arrange
        action_summary = {
            "message": "File successfully deleted",
            "file": "test.txt",
            "bucket": "test-bucket"
        }
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.try_delete_file.assert_called_once_with("test-bucket", "test.txt")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_delete_file_successful_return_helper_coupled_with_method_schema(self):
        # Arrange
        action_summary = return_delete_file_helper("File successfully deleted", "test.txt", "test-bucket")
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_delete_file_reports_warning_as_json(self):
        # Arrange
        action_summary = {
            "message": "File does not exist in the bucket",
            "file": "test.txt",
            "bucket": "test-bucket"
        }
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.try_delete_file.assert_called_once_with("test-bucket", "test.txt")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_delete_file_reports_warning_coupled_with_method_schema(self):
        # Arrange
        action_summary = return_delete_file_helper(
            "File does not exist in the bucket",
            "test.txt",
            "test-bucket"
        )
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary
