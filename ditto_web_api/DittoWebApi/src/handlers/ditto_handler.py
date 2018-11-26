from base64 import b64decode

from tornado_json.requesthandlers import APIHandler


class DittoHandler(APIHandler):
    def initialize(self, data_replication_service, security_service):
        self._data_replication_service = data_replication_service
        self._security_service = security_service

    def prepare(self):
        self._check_credentials()

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
            self._current_user = username
        else:
            self._authentication_failed()

    def _authentication_failed(self):
        self.set_status(401)
        self.finish({'reason': 'Authentication required'})
