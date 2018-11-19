import os

from testScenarios.given.ditto_api_server import DittoApiServer


class GivenSteps:
    def __init__(self, context):
        self._context = context
        self._ditto_api_server = DittoApiServer(context)

    def _write_test_file(self, file_name, content):
        with open(os.path.join(self._context.execution_folder_path, 'testing_area/src', file_name), 'w') as file:
            file.write(content)

    def simple_test_file_is_setup(self):
        self._write_test_file('testA.txt', 'example test content A')

    def a_file_in_src(self):
        self._write_test_file('testPermissions.txt', 'this is a text file for testing GET permissions')
        return self._file_in_src