from tornado.testing import gen_test

from DittoWebApi.src.handlers.copy_update import CopyUpdateHandler
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class CopyUpdateHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return CopyUpdateHandler

    # Security

    @gen_test
    def test_post_returns_401_when_no_credentials_given(self):
        self.assert_post_returns_401_when_no_credentials_given()

    @gen_test
    def test_post_returns_401_when_invalid_credentials_given(self):
        self.assert_post_returns_401_when_invalid_credentials_given()

    @gen_test
    def test_post_returns_200_when_credentials_accepted(self):
        self.assert_post_returns_200_when_credentials_accepted()

    # Coupling with Data Replication Service

    @gen_test
    def test_post_returns_summary_of_transfer_as_json_when_successful(self):
        # Arrange
        transfer_summary = {
            'message': 'Transfer successful',
            'new files uploaded': 2,
            'files updated': 1,
            'files skipped': 3,
            'data transferred (bytes)': 100
        }
        self.mock_data_replication_service.copy_new_and_update.return_value = transfer_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'directory': "some_directory"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.copy_new_and_update.assert_called_once_with("test-bucket", "some_directory")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_successful_transfer_summary_helper_coupled_with_method_schema(self):
        # Arrange
        transfer_summary = return_transfer_summary(
            message='Transfer successful',
            new_files_uploaded=2,
            files_updated=1,
            files_skipped=3,
            data_transferred=100
        )
        self.mock_data_replication_service.copy_new_and_update.return_value = transfer_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'directory': "some_directory"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_returns_summary_of_skipped_transfer_as_json(self):
        # Arrange
        transfer_summary = {
            'message': "No new or updated files found in directory",
            'new files transferred': 0,
            'files updated': 0,
            'files skipped': 5,
            'data transferred (bytes)': 0
        }
        self.mock_data_replication_service.copy_new_and_update.return_value = transfer_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'directory': "test_dir"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.copy_new_and_update.assert_called_once_with("test-bucket", "test_dir")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_skipped_transfer_summary_helper_coupled_with_method_schema(self):
        # Arrange
        transfer_summary = return_transfer_summary(
            message="No new or updated files found in directory some_directory",
            new_files_uploaded=0,
            files_updated=0,
            files_skipped=5,
            data_transferred=0
        )
        self.mock_data_replication_service.copy_new_and_update.return_value = transfer_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "bucket_1", 'directory': "some_directory"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_returns_warning_when_nonexistent_bucket_name_provided(self):
        # Arrange
        transfer_summary = {"message": "test-bucket does not exist in S3", "objects": []}
        self.mock_data_replication_service.copy_new_and_update.return_value = transfer_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'directory': "some_directory"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_returns_warning_when_directory_empty_or_nonexistent(self):
        # Arrange
        transfer_summary = {
            "message": "No files found in directory or directory does not exist (some_directory)",
            "objects": []
        }
        self.mock_data_replication_service.copy_new_and_update.return_value = transfer_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'directory': "some_directory"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary
