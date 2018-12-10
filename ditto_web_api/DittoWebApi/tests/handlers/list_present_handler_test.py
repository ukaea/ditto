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
    def standard_request_method(self):
        return 'POST'

    @property
    def standard_body(self):
        return {'bucket': "test-bucket", }

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
        self.mock_data_replication_service.retrieve_object_dicts.return_value = {
            'message': 'success',
            'objects': [],
            'status': StatusCodes.Okay
        }
        yield self.assert_request_returns_200_when_credentials_accepted(self.standard_body)

    # Arguments

    @gen_test
    def test_post_returns_400_when_bucket_name_is_missing(self):
        body = {'directory': "test_dir/test_sub_dir"}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_post_returns_400_when_bucket_name_is_blank(self):
        body = {'bucket': '  ', 'directory': "test_dir/test_sub_dir"}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_post_returns_200_when_directory_is_blank(self):
        body = {'bucket': 'test-bucket', 'directory': '   '}
        self.mock_data_replication_service.retrieve_object_dicts.return_value = {
            'message': 'success',
            'objects': [],
            'status': StatusCodes.Okay
        }
        yield self.assert_request_returns_200_when_credentials_accepted(body)

    @gen_test
    def test_post_returns_403_when_directory_is_outside_path_from_root(self):
        self._set_data_outside_root_dir()
        body = {'bucket': 'test-bucket', 'directory': '../some_files'}
        yield self.assert_request_returns_403_with_authorisation_okay(body)

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
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
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
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
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
        self.set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.retrieve_object_dicts.assert_called_once_with("test-bucket", None)
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == object_dicts

    @gen_test()
    def test_list_present_returns_404_when_bucket_does_not_exist_in_s3(self):
        # Arrange
        self.set_authentication_authorisation_ok()
        object_dicts = {"message": "Bucket does not exist in s3",
                        "objects": [],
                        "status": StatusCodes.Not_found}
        self.mock_data_replication_service.retrieve_object_dicts.return_value = object_dicts
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert error.value.response.code == 404
