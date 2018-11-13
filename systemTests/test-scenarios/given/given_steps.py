import os
from ftplib import FTP

from .ditto_api_server import DittoApiServer

class GivenSteps:
    def __init__(self, context):
        self._context = context
        self._ditto_api_server = DittoApiServer(context)

    def _write_test_file(self, file_name, content):
        with open(os.path.join(self._context.execution_folder_path, 'testing_area/src', file_name), 'w') as file:
            file.write(content)

    def simple_test_file_is_setup(self):
        self._write_test_file('testA.txt', 'example test content A')

    def an_ftp_client_is_connected(self):
        host = 'localhost'
        port = 5000
        self._context.ftp_client = FTP()
        self._context.ftp_client.set_debuglevel(2)
        self._context.ftp_client.connect(host, port)
        self._context.ftp_client.login()

    def a_file_in_src(self):
        self._write_test_file('testPermissions.txt', 'this is a text file for testing GET permissions')
        return self._file_in_src