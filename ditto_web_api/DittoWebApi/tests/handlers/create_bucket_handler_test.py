import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import gen_test

from DittoWebApi.src.handlers.create_bucket import CreateBucketHandler
from DittoWebApi.src.utils.return_helper import return_bucket_message
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
        return {'bucket': "test-bucket"}

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
    def test_post_returns_200_when_credentials_accepted(self):
        # Arrange
        action_summary = {"message": "Bucket created", "bucket": "some-bucket"}
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
        action_summary = {"message": "Bucket created", "bucket": "some-bucket"}
        self.mock_data_replication_service.create_bucket.return_value = action_summary
        self._set_admin_user()
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
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
        self.mock_security_service.is_in_group.return_value = True
        self.mock_bucket_settings_service.admin_groups = [self.user_group]
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
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
        self.mock_security_service.is_in_group.return_value = True
        self.mock_bucket_settings_service.admin_groups = [self.user_group]
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
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
        self.mock_security_service.is_in_group.return_value = True
        self.mock_bucket_settings_service.admin_groups = [self.user_group]
        # Act
        response_body, response_code = yield self.send_authorised_authenticated_request(self.standard_body)
        # Assert
        assert response_code == 200
        assert response_body['status'] == 'success'
        assert response_body['data'] == action_summary
