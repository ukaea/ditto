import pytest
from tornado.testing import gen_test
from tornado.httpclient import HTTPClientError
import tornado.web

from DittoWebApi.src.handlers.delete_file import DeleteFileHandler
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.src.utils.return_status import StatusCodes
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class DeleteFileHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return DeleteFileHandler

    @property
    def standard_body(self):
        return {'bucket': "test-bucket", 'file': 'test.txt'}

    # Security

    @gen_test
    def test_delete_returns_401_when_no_credentials_given(self):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        # Act
        with pytest.raises(tornado.httpclient.HTTPClientError) as error:
            yield self.send_DELETE_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_not_called()
        assert error.value.response.code == 401

    @gen_test
    def test_delete_returns_401_when_invalid_credentials_given(self):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        # Act
        with pytest.raises(tornado.httpclient.HTTPClientError) as error:
            yield self.send_authorised_DELETE_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        assert error.value.response.code == 401

    @gen_test
    def test_delete_returns_403_when_user_is_unauthorised(self):
        # Arrange
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = True
        self.mock_bucket_settings_service.bucket_permitted_groups.return_value = ['other']
        self.mock_security_service.is_in_group.return_value = False
        # Act
        with pytest.raises(tornado.httpclient.HTTPClientError) as error:
            yield self.send_authorised_DELETE_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        self.mock_security_service.is_in_group.assert_called_once_with(self._auth_username, 'other')
        assert error.value.response.code == 403

    @gen_test
    def test_delete_returns_404_when_bucket_not_recognised(self):
        # Arrange
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = False
        # Act
        with pytest.raises(tornado.httpclient.HTTPClientError) as error:
            yield self.send_authorised_DELETE_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        self.mock_bucket_settings_service.is_bucket_recognised.assert_called_once_with('test-bucket')
        assert error.value.response.code == 404

    @gen_test
    def test_delete_returns_200_when_credentials_accepted(self):
        # Arrange
        self.mock_data_replication_service.try_delete_file.return_value = {'message': 'File successfully deleted',
                                                                           'status': StatusCodes.Okay}
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_DELETE_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        self.mock_security_service.is_in_group.assert_called_once_with(self._auth_username, self._user_group)
        assert response_code == 200
        assert response_body['status'] == 'success'

    # Coupling with Data Replication Service

    @gen_test
    def test_delete_file_returns_summary_of_deleted_files_as_json_when_successful(self):
        # Arrange
        action_summary = {
            "message": "File successfully deleted",
            "file": "test.txt",
            "bucket": "test-bucket",
            "status": StatusCodes.Okay
        }
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self._set_authentication_authorisation_ok()
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
        action_summary = return_delete_file_helper(
            "File successfully deleted", "test.txt", "test-bucket", StatusCodes.Okay)
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self._set_authentication_authorisation_ok()
        # Act
        body = {'bucket': "test-bucket", 'file': "test.txt"}
        response_body, response_code = yield self.send_authorised_DELETE_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_delete_file_reports_404_when_file_is_missing(self):
        # Arrange
        action_summary = {
            "message": "File does not exist in the bucket",
            "file": "test.txt",
            "bucket": "test-bucket",
            "status": StatusCodes.Not_found
        }
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self._set_authentication_authorisation_ok()
        # Act
        body = {'bucket': "test-bucket", 'file': "test.txt"}
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_DELETE_request(body)
        # Assert
        error.value.response.code == 404
