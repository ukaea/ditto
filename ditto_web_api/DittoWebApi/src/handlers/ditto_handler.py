from base64 import b64decode

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
            raise ValueError('Attribute missing')
        return default

    def check_current_user_authorised_for_bucket(self, bucket_name):
        if not self._bucket_settings_service.is_bucket_recognised(bucket_name):
            self.set_status(404)
            self.finish({'reason': 'Bucket name not recognised'})
        permitted_groups = self._bucket_settings_service.bucket_permitted_groups(bucket_name)
        for group_name in permitted_groups:
            if self._security_service.is_in_group(self._current_user, group_name):
                return
        self.set_status(403)
        self.finish({'reason': 'Not authorised for this bucket'})

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

    def _authentication_failed(self):
        raise exceptions.APIError(401, 'Authentication required')
