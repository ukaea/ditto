import requests

from requests.auth import HTTPBasicAuth


class WhenSteps:
    def __init__(self, context):
        self._context = context

    def environment_is_stopped(self):
        self._context.shut_down_ditto_api()

    def something_happens(self):
        print(self.__class__)

    def authorised_create_bucket_called_for_simple_bucket(self):
        handler = 'createbucket'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_authorised_request(handler, body)

    def unauthorised_create_bucket_called_for_simple_bucket(self):
        handler = 'createbucket'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_unauthorised_request(handler, body)

    def authorised_create_bucket_called_with_name(self, name):
        handler = 'createbucket'
        body = {'bucket': name}
        self._make_authorised_request(handler, body)

    def authorised_copy_dir_called_for_whole_directory(self):
        handler = 'copydir'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_authorised_request(handler, body)

    def unauthorised_copy_dir_called_for_whole_directory(self):
        handler = 'copydir'
        body = {'bucket': self._context.standard_bucket_name}
        self._make_unauthorised_request(handler, body)

    def authorised_copy_dir_called_for_sub_directory(self):
        handler = 'copydir'
        body = {'bucket': 'systemtest-textbucket', 'directory': 'sub_dir_A'}
        self._make_authorised_request(handler, body)

    def authorised_list_present_called_for_simple_bucket_whole_directory_structure(self):
        handler = 'listpresent'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_authorised_request(handler, body)

    def unauthorised_list_present_called_for_simple_bucket_whole_directory_structure(self):
        handler = 'listpresent'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_unauthorised_request(handler, body)

    def authorised_copy_new_called_for_whole_directory(self):
        handler = 'copynew'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_authorised_request(handler, body)

    def unauthorised_copy_new_called_for_whole_directory(self):
        handler = 'copynew'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_unauthorised_request(handler, body)

    def authorised_delete_file_is_called_for_simple_file_in_s3(self):
        handler = 'deletefile'
        body = {'bucket': 'systemtest-textbucket', 'file': 'testA.txt'}
        self._make_authorised_request(handler, body)

    def unauthorised_delete_file_is_called_for_simple_file_in_s3(self):
        handler = 'deletefile'
        body = {'bucket': 'systemtest-textbucket', 'file': 'testA.txt'}
        self._make_unauthorised_request(handler, body)

    def authorised_copy_update_called_for_whole_directory(self):
        handler = 'copyupdate'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_authorised_request(handler, body)

    def unauthorised_copy_update_called_for_whole_directory(self):
        handler = 'copyupdate'
        body = {'bucket': 'systemtest-textbucket'}
        self._make_unauthorised_request(handler, body)

    def _make_authorised_request(self, handler, body):
        url = f'http://{self._context.host_address}:{self._context.app_port}/{handler}/'
        authentication = HTTPBasicAuth(self._context.authentication_username, self._context.authentication_password)
        if handler == "deletefile":
            response = requests.delete(url,
                                       json=body,
                                       auth=authentication)
        else:
            response = requests.post(url,
                                     json=body,
                                     auth=authentication)
        self._context.http_client_response = response

    def _make_unauthorised_request(self, handler, body):
        url = f'http://{self._context.host_address}:{self._context.app_port}/{handler}/'
        authentication = HTTPBasicAuth('unknown_user', 'password')
        if handler == "deletefile":
            response = requests.delete(url,
                                       json=body,
                                       auth=authentication)
        else:
            response = requests.post(url,
                                     json=body,
                                     auth=authentication)
        self._context.http_client_response = response
