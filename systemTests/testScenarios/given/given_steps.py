import os

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
