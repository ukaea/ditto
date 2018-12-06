import pytest

from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test

from DittoWebApi.src.handlers.copy_dir import CopyDirHandler
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.src.utils.return_status import StatusCodes
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class CopyDirHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return CopyDirHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @property
    def standard_body(self):
        return {'bucket': "test-bucket", 'directory': "test_dir/test_sub_dir"}

    # Security

    @gen_test
    def test_post_returns_401_when_no_credentials_given(self):
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
        self.mock_data_replication_service.copy_dir.return_value = return_transfer_summary()
        yield self.assert_request_returns_200_when_credentials_accepted(self.standard_body)

    # Coupling with Data Replication Service

    @gen_test
    def test_post_returns_summary_of_single_object_transferred_when_successful(self):
        # Arrange
        transfer_summary = {
            "message": "Transfer successful",
            "new files uploaded": 1,
            "files updated": 0,
            "files skipped": 0,
            "data transferred (bytes)": 100,
            "status": StatusCodes.Okay
        }
        self.mock_data_replication_service.copy_dir.return_value = transfer_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.copy_dir.assert_called_once_with("test-bucket", "test_dir/test_sub_dir")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_successful_transfer_summary_helper_coupled_with_method_schema(self):
        # Arrange
        transfer_summary = return_transfer_summary(
            message='Transfer successful',
            new_files_uploaded=1,
            files_updated=0,
            files_skipped=0,
            data_transferred=100,
            status=StatusCodes.Okay
        )
        self.mock_data_replication_service.copy_dir.return_value = transfer_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_returns_summary_of_skipped_transfer_as_json(self):
        # Arrange
        transfer_summary = {
            "message": "Directory already exists",
            "new files uploaded": 0,
            "files updated": 0,
            "files skipped": 5,
            "data transferred (bytes)": 0,
            "status": StatusCodes.Okay
        }
        self.mock_data_replication_service.copy_dir.return_value = transfer_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.copy_dir.assert_called_once_with("test-bucket", "test_dir/test_sub_dir")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_skipped_transfer_summary_helper_coupled_with_method_schema(self):
        # Arrange
        transfer_summary = return_transfer_summary(
            message="Directory already exists, 5 files skipped",
            new_files_uploaded=0,
            files_updated=0,
            files_skipped=5,
            data_transferred=0,
            status=StatusCodes.Okay
        )
        self.mock_data_replication_service.copy_dir.return_value = transfer_summary
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test()
    def test_copy_dir_returns_404_when_bucket_does_not_exist_in_s3(self):
        # Arrange
        self.set_authentication_authorisation_ok()
        transfer_summary = return_transfer_summary(
            message="Bucket does not exist in s3",
            new_files_uploaded=0,
            files_updated=0,
            files_skipped=5,
            data_transferred=0,
            status=StatusCodes.Not_found
        )
        self.mock_data_replication_service.copy_dir.return_value = transfer_summary
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert error.value.response.code == 404
