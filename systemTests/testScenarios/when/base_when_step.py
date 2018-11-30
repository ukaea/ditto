import requests
from requests.auth import HTTPBasicAuth

from testScenarios.tools.process_helper import print_port_state

# Standard request timeout, in seconds
TIMEOUT = 5


class BaseWhenStep:
    def __init__(self, context):
        self._context = context

    def _make_authorised_request(self, handler, body):
        url = f'http://{self._context.host_address}:{self._context.app_port}/{handler}/'
        authentication = HTTPBasicAuth(self._context.authentication_username, self._context.authentication_password)
        method = "DELETE" if handler == "deletefile" else "POST"
        self._context.http_client_response = None
        try:
            response = requests.request(method, url, json=body, auth=authentication, timeout=TIMEOUT)
            self._context.http_client_response = response
        except Exception as exception:
            print_port_state(self._context.host_address, self._context.app_port)
            print(f'Tried to connect to "{url}"')
            print(exception)

    def _make_unauthorised_request(self, handler, body):
        url = f'http://{self._context.host_address}:{self._context.app_port}/{handler}/'
        authentication = HTTPBasicAuth('unknown_user', 'password')
        method = "DELETE" if handler == "deletefile" else "POST"
        self._context.http_client_response = None
        try:
            response = requests.request(method, url, json=body, auth=authentication, timeout=TIMEOUT)
            self._context.http_client_response = response
        except Exception as exception:
            print_port_state(self._context.host_address, self._context.app_port)
            print(f'Tried to connect to "{url}"')
            print(exception)

    def _make_request_with_no_authorisation_credentials(self, handler, body):
        url = f'http://{self._context.host_address}:{self._context.app_port}/{handler}/'
        method = "DELETE" if handler == "deletefile" else "POST"
        self._context.http_client_response = None
        try:
            response = requests.request(method, url, json=body, timeout=TIMEOUT)
            self._context.http_client_response = response
        except Exception as exception:
            print_port_state(self._context.host_address, self._context.app_port)
            print(f'Tried to connect to "{url}"')
            print(exception)