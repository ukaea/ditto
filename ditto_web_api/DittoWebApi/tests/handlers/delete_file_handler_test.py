import pytest
from tornado.testing import gen_test
from tornado.httpclient import HTTPClientError

from DittoWebApi.src.handlers.delete_file import DeleteFileHandler
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.src.utils.return_status import StatusCodes
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
    def test_delete_returns_401_when_invalid_credentials_given(self):
        yield self.assert_request_returns_401_when_invalid_credentials_given(self.standard_body)

    @gen_test
    def test_delete_returns_403_when_user_is_unauthorised(self):
        yield self.assert_request_returns_403_when_unauthorised_user(self.standard_body)

    @gen_test
    def test_delete_returns_404_when_bucket_nonexistent(self):
        yield self.assert_request_returns_404_when_unrecognised_bucket_named(self.standard_body)

    @gen_test
    def test_delete_returns_200_when_credentials_accepted(self):
        self._set_data_in_root_dir()
        self.mock_data_replication_service.try_delete_file.return_value = {'message': 'File successfully deleted',
                                                                           'status': StatusCodes.Okay}
        yield self.assert_request_returns_200_when_credentials_accepted(self.standard_body)

    # Arguments

    @gen_test
    def test_delete_returns_400_when_bucket_name_is_missing(self):
        body = {'file': "test_dir/test_sub_dir"}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_delete_returns_400_when_bucket_name_is_blank(self):
        body = {'bucket': '  ', 'file': "test_dir/test_sub_dir"}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_delete_returns_400_when_file_is_missing(self):
        body = {'bucket': 'test-bucket'}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_delete_returns_400_when_file_is_blank(self):
        body = {'bucket': 'test-bucket', 'file': "   "}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_delete_returns_403_when_file_is_outside_path_from_root(self):
        body = {'bucket': 'test-bucket', 'file': '../some_file.txt'}
        self._set_data_outside_root_dir()
        yield self.assert_request_returns_403_with_authorisation_okay(body)

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
        self.set_authentication_authorisation_ok()
        self._set_data_in_root_dir()
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
        action_summary = return_delete_file_helper(
            "File successfully deleted", "test.txt", "test-bucket", StatusCodes.Okay)
        self.mock_data_replication_service.try_delete_file.return_value = action_summary
        self.set_authentication_authorisation_ok()
        self._set_data_in_root_dir()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
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
        self.set_authentication_authorisation_ok()
        self._set_data_in_root_dir()
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert error.value.response.code == 404

    @gen_test()
    def test_delete_file_returns_404_when_bucket_does_not_exist_in_s3(self):
        # Arrange
        self.set_authentication_authorisation_ok()
        transfer_summary = return_delete_file_helper(
            message="Bucket does not exist in s3",
            bucket_name="test-bucket",
            file_rel_path="some_file",
            status=StatusCodes.Not_found
        )
        self.mock_data_replication_service.try_delete_file.return_value = transfer_summary
        self._set_data_in_root_dir()
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert error.value.response.code == 404
