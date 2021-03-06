from abc import ABCMeta, abstractmethod
import json
import mock
import pytest
from tornado.httpclient import HTTPClientError
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from DittoWebApi.src.services.bucket_settings_service import BucketSettingsService
from DittoWebApi.src.services.data_replication.data_replication_service import DataReplicationService
from DittoWebApi.src.services.security.isecurity_service import ISecurityService
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.utils.route_helper import format_route_specification


class BaseHandlerTest(AsyncHTTPTestCase, metaclass=ABCMeta):
    # Standard properties

    @property
    def auth_username(self):
        return 'testuser'

    @property
    def auth_password(self):
        return 'password'

    @property
    def user_group(self):
        return 'group'

    # Test setup

    @property
    @abstractmethod
    def handler(self):
        pass

    @property
    @abstractmethod
    def standard_request_method(self):
        pass

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

    def set_authentication_authorisation_ok(self):
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = True
        self.mock_bucket_settings_service.bucket_permitted_groups.return_value = [self.user_group]
        self.mock_security_service.is_in_group.return_value = True

    def _set_admin_user(self):
        self.set_authentication_authorisation_ok()
        self.mock_security_service.is_in_group.return_value = True
        self.mock_bucket_settings_service.admin_groups = [self.user_group]

    def _set_data_in_root_dir(self):
        self.mock_file_system_helper.canonical_path.side_effect = ["root", "root/data"]

    def _set_data_outside_root_dir(self):
        self.mock_file_system_helper.canonical_path.side_effect = ["root", "data"]

    # Request methods

    async def _request(self, method, body, username, password):
        allow_nonstandard_methods = self.standard_request_method == "DELETE"
        json_body = json.dumps(body)
        response = await self.http_client.fetch(
            self.url,
            method=method,
            body=json_body,
            auth_username=username,
            auth_password=password,
            allow_nonstandard_methods=allow_nonstandard_methods
        )
        return response

    @staticmethod
    def _get_body(response):
        return json.loads(response.body, encoding='utf-8')

    async def send_authorised_authenticated_request(self, body):
        response = await self._request(self.standard_request_method, body, self.auth_username, self.auth_password)
        response_body = BaseHandlerTest._get_body(response)
        return response_body, response.code

    # Security

    async def assert_request_returns_401_when_no_credentials_given(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        method = self.standard_request_method
        # Act
        with pytest.raises(HTTPClientError) as error:
            await self._request(method, body, None, None)
        # Assert
        assert error.value.response.code == 401

    async def assert_request_returns_401_when_invalid_credentials_given(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = False
        # Act
        with pytest.raises(HTTPClientError) as error:
            await self._request(self.standard_request_method, body, self.auth_username, 'wrong')
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self.auth_username, 'wrong')
        assert error.value.response.code == 401

    async def assert_request_returns_403_when_unauthorised_user(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = True
        self.mock_bucket_settings_service.bucket_permitted_groups.return_value = ['other']
        self.mock_security_service.is_in_group.return_value = False
        # Act
        with pytest.raises(HTTPClientError) as error:
            await self._request(self.standard_request_method, body, self.auth_username, self.auth_password)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self.auth_username, self.auth_password)
        self.mock_security_service.is_in_group.assert_called_once_with(self.auth_username, 'other')
        assert error.value.response.code == 403

    async def assert_request_returns_404_when_unrecognised_bucket_named(self, body):
        # Arrange
        self.mock_security_service.check_credentials.return_value = True
        self.mock_bucket_settings_service.is_bucket_recognised.return_value = False
        # Act
        with pytest.raises(HTTPClientError) as error:
            await self._request(self.standard_request_method, body, self.auth_username, self.auth_password)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self.auth_username, self.auth_password)
        self.mock_bucket_settings_service.is_bucket_recognised.assert_called_once_with(body['bucket'])
        assert error.value.response.code == 404

    async def assert_request_returns_200_when_credentials_accepted(self, body):
        # Arrange
        self.set_authentication_authorisation_ok()
        # Act
        response = await self._request(self.standard_request_method, body, self.auth_username, self.auth_password)
        response_body = BaseHandlerTest._get_body(response)
        # Assert
        self.mock_security_service.check_credentials.assert_called_once_with(self.auth_username, self.auth_password)
        self.mock_bucket_settings_service.is_bucket_recognised.assert_called_once_with('test-bucket')
        self.mock_security_service.is_in_group.assert_called_once_with(self.auth_username, self.user_group)
        assert response.code == 200
        assert response_body['status'] == 'success'

    # valid arguments

    async def assert_request_returns_400_with_authorisation_okay(self, body):
        # Arrange
        self.set_authentication_authorisation_ok()
        method = self.standard_request_method
        # Act
        with pytest.raises(HTTPClientError) as error:
            await self._request(method, body, self.auth_username, self.auth_password)
        # Assert
        assert error.value.response.code == 400

    async def assert_request_returns_403_with_authorisation_okay(self, body):
        # Arrange
        self.set_authentication_authorisation_ok()
        method = self.standard_request_method
        # Act
        with pytest.raises(HTTPClientError) as error:
            await self._request(method, body, self.auth_username, self.auth_password)
        # Assert
        assert error.value.response.code == 403
