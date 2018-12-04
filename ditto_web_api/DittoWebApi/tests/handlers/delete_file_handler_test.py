import pytest
from tornado.testing import gen_test
import tornado.web

from DittoWebApi.src.handlers.delete_file import DeleteFileHandler
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class DeleteFileHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return DeleteFileHandler

    # Security

    @gen_test
    def test_delete_returns_401_when_no_credentials_given(self):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        # Act
        body = {'bucket': "test-bucket", 'file': 'test.txt'}
        with pytest.raises(tornado.httpclient.HTTPClientError) as error:
            yield self.send_DELETE_request(body)
        # Assert
        self.mock_security_service.check_credentials.assert_not_called()
        assert error.value.response.code == 401

    @gen_test
    def test_delete_returns_401_when_invalid_credentials_given(self):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        # Act
        body = {'bucket': "test-bucket", 'file': 'test.txt'}
        with pytest.raises(tornado.httpclient.HTTPClientError) as error:
            yield self.send_authorised_DELETE_request(body)
        # Assert
        assert error.value.response.code == 401

    @gen_test
    def test_delete_returns_200_when_credentials_accepted(self):
        # Arrange
        self.mock_data_replication_service.try_delete_file.return_value = {}
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'file': 'test.txt'}
        response_body, response_code = yield self.send_authorised_DELETE_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'

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
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'file': "test.txt"}
        response_body, response_code = yield self.send_authorised_DELETE_request(body)
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
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'file': "test.txt"}
        response_body, response_code = yield self.send_authorised_DELETE_request(body)
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
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'file': "test.txt"}
        response_body, response_code = yield self.send_authorised_DELETE_request(body)
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
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'file': "test.txt"}
        response_body, response_code = yield self.send_authorised_DELETE_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary
