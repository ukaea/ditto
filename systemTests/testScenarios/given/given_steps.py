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
        url = f'http://{self._context.s3host}:{self._context.app_port}/createbucket/'
        body = {'bucket': 'systemtest-textbucket'}
        response = requests.post(url, json=body)
        assert response.status_code == 200
        print(self._context.response_data(response)["message"])
        assert self._context.response_data(response)["message"] == "Bucket Created (systemtest-textbucket)"

    def simple_test_file_is_setup_in_s3(self):
        self._write_test_file_in_s3('testA.txt', 'example test content A')

    def _write_test_file(self, file_name, content):
        with open(os.path.join(self._context.local_data_folder_path, file_name), 'w') as file:
            file.write(content)
