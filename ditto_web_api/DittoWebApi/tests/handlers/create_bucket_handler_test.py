from tornado.testing import gen_test

from DittoWebApi.src.handlers.create_bucket import CreateBucketHandler
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class CreateBucketHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return CreateBucketHandler

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
    def test_post_create_bucket_returns_summary_of_new_bucket_when_successful(self):
        # Arrange
        action_summary = {"message": "Bucket created", "bucket": "some-bucket"}
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.create_bucket.assert_called_once_with("test-bucket")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_post_create_bucket_successful_return_helper_coupled_with_method_schema(self):
        # Arrange
        action_summary = return_bucket_message("Bucket created", "some-bucket")
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", 'directory': "some_directory"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_post_create_bucket_reports_warning_as_json(self):
        # Arrange
        action_summary = {"message": "Bucket already exists", "bucket": "some-bucket"}
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.create_bucket.assert_called_once_with("test-bucket")
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_post_create_bucket_reports_warning_coupled_with_method_schema(self):
        # Arrange
        action_summary = return_bucket_message("Bucket already exists", "some-bucket")
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket"}
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary
