import pytest

from tornado.testing import gen_test
from tornado.httpclient import HTTPClientError

from DittoWebApi.src.handlers.list_present import ListPresentHandler
from DittoWebApi.src.utils.return_status import StatusCodes
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class ListPresentHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return ListPresentHandler

    @property
    def standard_body(self):
        return {'bucket': "test-bucket", }

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
    def test_post_returns_single_object_in_json_array(self):
        # Arrange
        object_dicts = {
            "message": "objects returned successfully",
            "objects": [
                {"object": "file_1.txt", "bucket": "test-bucket"}
            ],
            "status": StatusCodes.Okay
        }
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
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
            ],
            "status": StatusCodes.Okay
        }
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
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
            "objects": [],
            "status": StatusCodes.Okay
        }
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.retrieve_object_dicts.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == object_dicts

    @gen_test()
    def test_list_present_returns_404_when_bucket_does_not_exist_in_s3(self):
        # Arrange
        self._set_authentication_authorisation_ok()
        object_dicts = {"message": "Bucket does not exist in s3",
                        "objects": [],
                        "status": StatusCodes.Not_found}
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_POST_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        self.mock_bucket_settings_service.is_bucket_recognised.assert_called_once_with('test-bucket')
        self.mock_security_service.is_in_group.assert_called_once_with(self._auth_username, self._user_group)
        assert error.value.response.code == 404
