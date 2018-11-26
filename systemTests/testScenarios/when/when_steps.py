import requests


class WhenSteps:
    def __init__(self, context):
        self._context = context

    def environment_is_stopped(self):
        self._context.shut_down_ditto_api()

    def something_happens(self):
        print(self.__class__)

    def create_bucket_called_for_simple_bucket(self):
        handler = 'createbucket'
        body = {'bucket': 'systemtest-textbucket'}
        self.make_request(handler, body)

    def copy_dir_called_for_whole_directory(self):
        handler = 'copydir'
        body = {'bucket': self._context.standard_bucket_name}
        self.make_request(handler, body)

    def copy_dir_called_for_sub_directory(self):
        handler = 'copydir'
        body = {'bucket': 'systemtest-textbucket', 'directory': 'sub_dir_A'}
        self.make_request(handler, body)

    def list_present_called_for_simple_bucket_whole_directory_structure(self):
        handler = 'listpresent'
        body = {'bucket': 'systemtest-textbucket'}
        self.make_request(handler, body)

    def copy_new_called_for_whole_directory(self):
        handler = 'copynew'
        body = {'bucket': 'systemtest-textbucket'}
        self.make_request(handler, body)

    def delete_file_is_called_for_simple_file_in_s3(self):
        handler = 'deletefile'
        body = {'bucket': 'systemtest-textbucket', 'file': 'testA.txt'}
        self.make_request(handler, body)

    def copy_update_called_for_whole_directory(self):
        handler = 'copyupdate'
        body = {'bucket': 'systemtest-textbucket'}
        self.make_request(handler, body)

    def make_request(self, handler, body):
        url = f'http://{self._context.host_address}:{self._context.app_port}/{handler}/'
        if handler == "deletefile":
            response = requests.delete(url, json=body)
        else:
            response = requests.post(url, json=body)
        self._context.http_client_response = response
