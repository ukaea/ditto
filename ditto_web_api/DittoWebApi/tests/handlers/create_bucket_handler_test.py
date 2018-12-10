import json
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test

from DittoWebApi.src.handlers.create_bucket import CreateBucketHandler
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.src.utils.return_status import StatusCodes
from DittoWebApi.tests.handlers.base_handler_test import BaseHandlerTest


class CreateBucketHandlerTest(BaseHandlerTest):
    @property
    def handler(self):
        return CreateBucketHandler

    @property
    def standard_request_method(self):
        return 'POST'

    @property
    def standard_body(self):
        return {
            'bucket': 'test-bucket',
            'groups': ['testgroup'],
            'root': '/usr/tmp/data'
        }

    # Security

    @gen_test
    def test_post_returns_401_when_no_credentials_given(self):
        yield self.assert_request_returns_401_when_no_credentials_given(self.standard_body)

    @gen_test
    def test_post_returns_401_when_invalid_credentials_given(self):
        yield self.assert_request_returns_401_when_invalid_credentials_given(self.standard_body)

    @gen_test
    def test_post_returns_403_when_user_is_unauthorised(self):
        # Arrange
        self.set_authentication_authorisation_ok()
        self.mock_security_service.is_in_group.return_value = False
        self.mock_bucket_settings_service.admin_groups = ['admin']
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self.auth_username, self.auth_password)
        self.mock_security_service.is_in_group.assert_called_once_with(self.auth_username, 'admin')
        assert error.value.response.code == 403

    @gen_test
    def test_post_returns_400_when_bucket_already_exists(self):
        # Arrange
        action_summary = {"message": "Bucket already exists",
                          "bucket": "some-bucket",
                          "status": StatusCodes.Bad_request}
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self._set_admin_user()
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_authenticated_request(self.standard_body)
        response_body = json.loads(error.value.response.body, encoding='utf-8')
        # Assert
        assert error.value.response.code == 400
        assert response_body['status'] == 'fail'
        assert response_body['data'] == "Bucket already exists"

    @gen_test
    def test_post_returns_200_when_credentials_accepted(self):
        # Arrange
        action_summary = {"message": "Bucket created", "bucket": "some-bucket", 'status': StatusCodes.Okay}
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self._set_admin_user()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self.auth_username, self.auth_password)
        self.mock_security_service.is_in_group.assert_called_once_with(self.auth_username, self.user_group)
        assert response_code == 200
        assert response_body['status'] == 'success'

    # Coupling with Data Replication Service

    @gen_test
    def test_post_create_bucket_returns_summary_of_new_bucket_when_successful(self):
        # Arrange
        action_summary = {"message": "Bucket created", "bucket": "test-bucket", "status": StatusCodes.Okay}
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self._set_admin_user()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        self.mock_data_replication_service.create_bucket.assert_called_once_with(
            "test-bucket",
            ['testgroup'],
            "/usr/tmp/data"
        )
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    @gen_test
    def test_post_create_bucket_successful_return_helper_coupled_with_method_schema(self):
        # Arrange
        action_summary = return_bucket_message("Bucket created", "some-bucket", StatusCodes.Okay)
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self.mock_security_service.check_credentials.return_value = True
        self.mock_security_service.is_in_group.return_value = True
        self.mock_bucket_settings_service.admin_groups = [self.user_group]
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary

    # Arguments

    @gen_test
    def test_post_returns_403_when_bucket_name_is_missing(self):
        body = {'groups': ['testgroup'], 'root': '/usr/tmp/data'}
        yield self.assert_request_returns_403_with_authorisation_okay(body)

    @gen_test
    def test_post_returns_400_when_bucket_name_is_blank(self):
        self._set_admin_user()
        body = {'bucket': '  ', 'groups': ['testgroup'], 'root': '/usr/tmp/data'}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_post_returns_403_when_groups_is_missing(self):
        body = {'bucket': 'test-bucket', 'root': '/usr/tmp/data'}
        yield self.assert_request_returns_403_with_authorisation_okay(body)

    @gen_test
    def test_post_returns_400_when_groups_is_empty(self):
        self._set_admin_user()
        body = {'bucket': 'test-bucket', 'groups': [], 'root': '/usr/tmp/data'}
        yield self.assert_request_returns_400_with_authorisation_okay(body)

    @gen_test
    def test_post_returns_403_when_root_is_missing(self):
        body = {'bucket': 'test-bucket', 'groups': ['testgroup']}
        yield self.assert_request_returns_403_with_authorisation_okay(body)

    @gen_test
    def test_post_returns_400_when_root_is_blank(self):
        self._set_admin_user()
        body = {'bucket': 'test-bucket', 'groups': ['testgroup'], 'root': ' '}
        yield self.assert_request_returns_400_with_authorisation_okay(body)
