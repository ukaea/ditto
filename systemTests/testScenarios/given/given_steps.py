import os
import requests

from testScenarios.given.ditto_api_server import DittoApiServer


class GivenSteps:
    def __init__(self, context):
        self._context = context
        self._ditto_api_server = DittoApiServer(context)

    @property
    def ditto_web_api(self):
        return self._ditto_api_server

    def _write_test_file(self, file_name, content):
        with open(os.path.join(self._context.local_data_folder_path, file_name), 'w') as file:
            file.write(content)

    def simple_test_file_is_setup(self):
        self._write_test_file('testA.txt', 'example test content A')

    def simple_sub_dir_with_test_file_is_setup(self):
        self._write_test_file_in_sub_dir(os.path.join('sub_dir_A', 'testB.txt'), 'example test content B')

    def _write_test_file_in_sub_dir(self, file_name, content):
        filename = os.path.join(self._context.local_data_folder_path, file_name)
        os.makedirs(os.path.dirname(filename))
        with open(filename, 'w') as file:
            file.write(content)

    def standard_bucket_exists_in_s3(self):
        url = f'http://{self._context.host_address}:{self._context.app_port}/createbucket/'
        body = {'bucket': 'systemtest-textbucket'}
        requests.post(url, json=body)
        bucket_path = os.path.join(self._context.s3_data_folder_path, 'systemtest-textbucket')
        assert os.path.exists(bucket_path)

    def update_simple_file(self):
        file_path = os.path.join(self._context.local_data_folder_path, 'testA.txt')
        new_content = ". A new bit of text"
        with open(file_path, 'a') as file:
            file.write(new_content)
