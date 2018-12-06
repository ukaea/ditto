from base64 import b64decode

from tornado_json import exceptions
from tornado_json.requesthandlers import APIHandler
from tornado_json import exceptions


class DittoHandler(APIHandler):
    # pylint: disable=arguments-differ
    def initialize(self, bucket_settings_service, data_replication_service, security_service):
        self._bucket_settings_service = bucket_settings_service
        self._data_replication_service = data_replication_service
        self._security_service = security_service

    def prepare(self):
        self._check_credentials()

    def get_body_attribute(self, key, default=None, required=False):
        # pylint: disable=no-member
        if key in self.body:
            return self.body[key]
        if required:
            raise exceptions.APIError(400, 'Attribute missing')
        return default

    def check_current_user_authorised_for_bucket(self, bucket_name):
        if not self._bucket_settings_service.is_bucket_recognised(bucket_name):
            raise exceptions.APIError(404, 'Bucket name not recognised')
        permitted_groups = self._bucket_settings_service.bucket_permitted_groups(bucket_name)
        for group_name in permitted_groups:
            if self._security_service.is_in_group(self._current_user, group_name):
                return
        raise exceptions.APIError(403, 'Not authorised for this bucket')

    def check_current_user_is_admin(self):
        for group_name in self._bucket_settings_service.admin_groups:
            if self._security_service.is_in_group(self._current_user, group_name):
                return
        raise exceptions.APIError(403, 'Administrator authorisation required')

    def _check_credentials(self):
        auth_header = self.request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            self._authentication_failed()
            return

        auth_data = auth_header.split(None, 1)[-1]
        auth_data = b64decode(auth_data).decode('ascii')
        username, password = auth_data.split(':', 1)

        credentials_accepted = self._security_service.check_credentials(username, password)
        if credentials_accepted:
            # pylint: disable=attribute-defined-outside-init
            self._current_user = username
        else:
            self._authentication_failed()

    @staticmethod
    def check_request_was_completed_successfully(result):
        exceptions.api_assert(result["status"].value == 200,
                              result["status"].value,
                              result['message'])

    @staticmethod
    def _authentication_failed():
        raise exceptions.APIError(401, 'Authentication required')
