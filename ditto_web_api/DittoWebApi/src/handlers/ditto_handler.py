from base64 import b64decode

from tornado_json.requesthandlers import APIHandler
from tornado_json import exceptions

from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.utils.parse_strings import is_str_empty

class DittoHandler(APIHandler):
    # pylint: disable=arguments-differ
    def initialize(self, bucket_settings_service, data_replication_service, security_service):
        self._bucket_settings_service = bucket_settings_service
        self._data_replication_service = data_replication_service
        self._security_service = security_service
        self._file_system_helper = FileSystemHelper()

    def prepare(self):
        self._check_credentials()

    def get_body_attribute(self, key, default=None, required=False):
        # pylint: disable=no-member
        if key in self.body:
            self._check_attribute_is_not_empty(key, default, required)
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

    def _check_attribute_is_not_empty(self, key, default, required):
        if is_str_empty(self.body[key]) is True:
            raise exceptions.APIError(400, 'Attribute provided is empty') \
                if required \
                else self._set_attribute_value_to_default(key, default)

    def _set_attribute_value_to_default(self, key, default=False):
        self.body[key] = default

    def check_not_trying_to_access_data_outside_root(self, bucket_name, rel_path_to_data):
        if rel_path_to_data is not None:
            abs_bucket_root_dir = self._file_system_helper.absolute_file_path(
                self._bucket_settings_service.bucket_root_directory(bucket_name))
            abs_data_path = self._file_system_helper.absolute_file_path(rel_path_to_data)
            relative_path_bucket_to_data = self._file_system_helper.relative_file_path(abs_data_path,
                                                                                       abs_bucket_root_dir)
            if '..' in relative_path_bucket_to_data:
                raise exceptions.APIError(400, 'Can not access data outside root directory!')
