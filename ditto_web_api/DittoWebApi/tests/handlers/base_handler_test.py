from abc import ABCMeta, abstractmethod
import json
import mock
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from DittoWebApi.src.services.bucket_settings_service import BucketSettingsService
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.services.security.isecurity_service import ISecurityService
from DittoWebApi.src.utils.route_helper import format_route_specification


class BaseHandlerTest(AsyncHTTPTestCase, metaclass=ABCMeta):
    @property
    @abstractmethod
    def handler(self):
        pass

    @property
    def _auth_username(self):
        return 'testuser'

    @property
    def _auth_password(self):
        return 'password'

    @property
    def _user_group(self):
        return 'group'

    def get_app(self):
        self.mock_bucket_settings_service = mock.create_autospec(BucketSettingsService)
        self.mock_data_replication_service = mock.create_autospec(DataReplicationService)
        self.mock_file_system_helper = mock.create_autospec(FileSystemHelper)
        self.mock_security_service = mock.create_autospec(ISecurityService)
        self.container = {
            'bucket_settings_service': self.mock_bucket_settings_service,
            'data_replication_service': self.mock_data_replication_service,
            'file_system_helper': self.mock_file_system_helper,
            'security_service': self.mock_security_service
        }
        application = Application([
            (format_route_specification("testroute"), self.handler, self.container),
        ])
        self.url = self.get_url(r"/testroute/")
        return application

    # pylint: disable=invalid-name
    def send_DELETE_request(self, body):
        return self._send_request("DELETE", body, None, None, allow_nonstandard_methods=True)

    # pylint: disable=invalid-name
    def send_authorised_DELETE_request(self, body):
        return self._send_request("DELETE",
                                  body,
                                  self._auth_username,
                                  self._auth_password,
                                  allow_nonstandard_methods=True)

    # pylint: disable=invalid-name
    def send_POST_request(self, body):
        return self._send_request("POST", body, None, None)

    # pylint: disable=invalid-name
    def send_authorised_POST_request(self, body):
        return self._send_request("POST", body, self._auth_username, self._auth_password)

    def assert_post_returns_401_when_no_credentials_given(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_POST_request(body)
        # Assert
        assert error.value.response.code == 401

    def assert_post_returns_401_when_invalid_credentials_given(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        assert error.value.response.code == 401

    def assert_post_returns_403_when_unauthorised_user(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = True
        self.mock_bucket_settings_service.bucket_permitted_groups.return_value = ['other']
        self.mock_security_service.is_in_group.return_value = False
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        self.mock_security_service.is_in_group.assert_called_once_with(self._auth_username, 'other')
        assert error.value.response.code == 403

    def assert_post_returns_404_when_unrecognised_bucket_named(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = False
        # Act
        with pytest.raises(HTTPClientError) as error:
            yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        self.mock_bucket_settings_service.is_bucket_recognised.assert_called_once_with('test-bucket')
        assert error.value.response.code == 404

    def assert_post_returns_200_when_credentials_accepted(self, body):
        # Arrange
        self._set_authentication_authorisation_ok()
        # Act
        response_body, response_code = yield self.send_authorised_POST_request(body)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self._auth_username, self._auth_password)
        self.mock_bucket_settings_service.is_bucket_recognised.assert_called_once_with('test-bucket')
        self.mock_security_service.is_in_group.assert_called_once_with(self._auth_username, self._user_group)
        assert response_code == 200
        assert response_body['status'] == 'success'

    def _set_authentication_authorisation_ok(self):
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = True
        self.mock_bucket_settings_service.bucket_permitted_groups.return_value = [self._user_group]
        self.mock_security_service.is_in_group.return_value = True

    async def _send_request(self, method, body, username, password, allow_nonstandard_methods=False):
        response = await self.http_client.fetch(
            self.url,
            method=method,
            body=json.dumps(body),
            auth_username=username,
            auth_password=password,
            allow_nonstandard_methods=allow_nonstandard_methods
        )
        response_body = json.loads(response.body, encoding='utf-8')
        return response_body, response.code
