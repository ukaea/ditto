from tornado.testing import gen_test

from DittoWebApi.src.handlers.copy_new import CopyNewHandler
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class CopyNewHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return CopyNewHandler

    @property
    def standard_body(self):
        return {'bucket': "test-bucket"}

    # Security

    @gen_test
    def test_post_returns_401_when_no_credentials_given(self):
        self.assert_post_returns_401_when_no_credentials_given(self.standard_body)

    @gen_test
    def test_post_returns_401_when_invalid_credentials_given(self):
        self.assert_post_returns_401_when_invalid_credentials_given(self.standard_body)

    @gen_test
    def test_post_returns_403_when_user_is_unauthorised(self):
        self.assert_post_returns_403_when_unauthorised_user(self.standard_body)

    @gen_test
    def test_post_returns_404_when_bucket_nonexistent(self):
        self.assert_post_returns_404_when_unrecognised_bucket_named(self.standard_body)

    @gen_test
    def test_post_returns_200_when_credentials_accepted(self):
        self.assert_post_returns_200_when_credentials_accepted(self.standard_body)

    # Coupling with Data Replication Service

    @gen_test
    def test_post_returns_summary_of_single_object_transferred_when_successful(self):
        # Arrange
        transfer_summary = {
            'message': 'Transfer successful',
            'new files transferred': 1,
            'files updated': 0,
            'files skipped': 3,
            'data transferred (bytes)': 100
        }
        self.mock_data_replication_service.copy_new.return_value = transfer_summary
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.copy_new.assert_called_once_with("test-bucket", None)
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
            files_skipped=3,
            data_transferred=100
        )
        self.mock_data_replication_service.copy_new.return_value = transfer_summary
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_returns_summary_of_skipped_transfer_as_json(self):
        # Arrange
        transfer_summary = {
            "message": "objects returned successfully",
            "objects": [
                {"object": "file_1.txt", "bucket": "test-bucket"},
                {"object": "file_2.txt", "bucket": "test-bucket"}
            ]
        }
        self.mock_data_replication_service.copy_new.return_value = transfer_summary
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.copy_new.assert_called_once_with("test-bucket", None)
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
            data_transferred=0
        )
        self.mock_data_replication_service.copy_new.return_value = transfer_summary
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.copy_new.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary

    @gen_test
    def test_post_returns_warning_when_nonexistent_bucket_name_provided(self):
        # Arrange
        transfer_summary = {"message": "test-bucket does not exist in S3", "objects": []}
        self.mock_data_replication_service.copy_new.return_value = transfer_summary
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.copy_new.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == transfer_summary
