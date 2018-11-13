import subprocess
import os
import ftplib
from ftplib import FTP

from .gridftp_with_plugin import GridftpWithPlugin

class WhenSteps:
    def __init__(self, context):
        self._context = context
        self._gridftp_with_plugin = GridftpWithPlugin(context)

    def environment_is_stopped(self):
        self._context.stop_dms()

    def target_folder_listed(self, path_to_list):
        if path_to_list.startswith('/'):
            path_to_list = path_to_list.replace('/', '', 1)

        path = os.path.join(self._context.execution_folder_path, 'testing_area/target', path_to_list)
        shell_process = subprocess.Popen(
          'ls -l {}'.format(path),
          shell=True,
          stdout=self._context.console_logger.stdout_log_writer,
          stderr=self._context.console_logger.stderr_log_writer)
        shell_process.wait()

    def simple_file_is_copied(self):
        assert 1==0
        #fill out details - this should copy the test file created by given method "simple_test_file_is_setup" to /home/vagrant/systemTests/execution_space/testing_area/target/ using gridftp
        #possibly something like: os.system('globus-url-copy -v file:///home/${USER}/systemTests/execution_space/testing_area/src/testA.text ftp://localhost:5000/home/${USER}/systemTests/execution_space/testing_area/target/')

    def get_permissions_called(self):
        print('Send command to print working dir to gridFTP server...')
        print('Server returned: ')
        print('\t' + self._context.ftp_client.sendcmd('PWD'))
        print('\t' + self._context.ftp_client.sendcmd('SITE GETPERMISSIONS test'))

    def get_permissions_called_for_file(self):
        assert 1==0
        #we will use the command to get permissions for a file instead in this method
        #print('Send command to print working dir to gridFTP server...')
        #print('Server returned: ')
        #print('\t' + self._context.ftp_client.sendcmd('PWD'))
        #print('\t' + self._context.ftp_client.sendcmd('SITE GETPERMISSIONS test'))

    def gridftp_plugin_server(self):
        return self._gridftp_with_plugin