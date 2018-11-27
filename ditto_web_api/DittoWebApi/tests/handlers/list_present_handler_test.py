from tornado.testing import gen_test

from DittoWebApi.src.handlers.list_present import ListPresentHandler
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class ListPresentHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return ListPresentHandler

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
    def test_post_returns_single_object_in_json_array(self):
        # Arrange
        object_dicts = {
            "message": "objects returned successfully",
            "objects": [
                {"object": "file_1.txt", "bucket": "test-bucket"}
            ]
        }
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", }
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.retrieve_object_dicts.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == object_dicts

    @gen_test
    def test_post_returns_multiple_objects_as_a_json_array(self):
        # Arrange
        object_dicts = {
            "message": "objects returned successfully",
            "objects": [
                {"object": "file_1.txt", "bucket": "test-bucket"},
                {"object": "file_2.txt", "bucket": "test-bucket"}
            ]
        }
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", }
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.retrieve_object_dicts.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == object_dicts

    @gen_test
    def test_post_returns_empty_array_when_no_objects(self):
        # Arrange
        object_dicts = {
            "message": "no objects in S3 bucket",
            "objects": []
        }
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", }
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.retrieve_object_dicts.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == object_dicts

    @gen_test
    def test_post_returns_warning_when_nonexistent_bucket_name_provided(self):
        # Arrange
        object_dicts = {"message": "test-bucket does not exist in S3", "objects": []}
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        self.mock_security_service.check_credentials.return_value = True
        # Act
        body = {'bucket': "test-bucket", }
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_data_replication_service.retrieve_object_dicts.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == object_dicts
