import requests
from requests.auth import HTTPBasicAuth

from testScenarios.tools.process_helper import print_port_state
from testScenarios.when.base_when_step import BaseWhenStep


class CreateBucketWhenSteps(BaseWhenStep):
    def authenticated_create_bucket_called_for_simple_bucket(self):
        handler = 'createbucket'
        body = {
            'bucket': self._context.standard_bucket_name,
            'groups': ['group1', 'group2'],
            'data_root': self._context.local_data_folder_path,
            'archive_root': self._context.local_archive_root_path
        }
        self._make_authorised_request(handler, body)

    def admin_create_bucket_called_for_simple_bucket_without_archive_root(self):
        body = {
            'bucket': self._context.standard_bucket_name,
            'groups': ['group1', 'group2'],
            'data_root': self._context.local_data_folder_path
        }
        url = f'http://{self._context.host_address}:{self._context.app_port}/createbucket/'
        authentication = HTTPBasicAuth('AdminUser', 'IamAdmin')
        self._context.http_client_response = None
        try:
            response = requests.request("POST", url, json=body, auth=authentication)
            self._context.http_client_response = response
        except Exception as exception:
            print_port_state(self._context.host_address, self._context.app_port)
            print(f'Tried to connect to "{url}"')
            print(exception)

    def unauthenticated_create_bucket_called_for_simple_bucket(self):
        handler = 'createbucket'
        body = {
            'bucket': self._context.standard_bucket_name,
            'groups': ['group1', 'group2'],
            'data_root': self._context.local_data_folder_path,
            'archive_root': self._context.local_archive_root_path
        }
        self._make_unauthenticated_request(handler, body)

    def create_bucket_called_for_simple_bucket_with_no_user_credentials(self):
        handler = 'createbucket'
        body = {
            'bucket': self._context.standard_bucket_name,
            'groups': ['group1', 'group2'],
            'data_root': self._context.local_data_folder_path,
            'archive_root': self._context.local_archive_root_path
        }
        self._make_request_with_no_user_credentials(handler, body)

    def authenticated_create_bucket_called_with_name(self, name):
        handler = 'createbucket'
        body = {'bucket': name, 'groups': ['group1', 'group2'], 'data_root': self._context.local_data_folder_path}
        self._make_authorised_request(handler, body)

    def admin_create_bucket_called_for_simple_bucket(self):
        self.admin_create_bucket_called_with_name(self._context.standard_bucket_name)

    def admin_create_bucket_called_with_name(self, name):
        body = {'bucket': name,
                'groups': ['group1', 'group2'],
                'data_root': self._context.local_data_folder_path,
                'archive_root': self._context.local_archive_root_path}
        url = f'http://{self._context.host_address}:{self._context.app_port}/createbucket/'
        authentication = HTTPBasicAuth('AdminUser', 'IamAdmin')
        self._context.http_client_response = None
        try:
            response = requests.request("POST", url, json=body, auth=authentication)
            self._context.http_client_response = response
        except Exception as exception:
            print_port_state(self._context.host_address, self._context.app_port)
            print(f'Tried to connect to "{url}"')
            print(exception)

