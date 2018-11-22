import os
import shutil
import unittest
import pytest

from testScenarios.given.given_steps import GivenSteps
from testScenarios.when.when_steps import WhenSteps
from testScenarios.then.then_steps import ThenSteps
from testScenarios.tools.process_logger import ProcessLogger


class SystemTestContext:
    def __init__(self):
        self._execution_folder_path = '/home/vagrant/execution_space'
        self.ditto_api_process = None
        self.console_logger = ProcessLogger('console', self.log_folder_path)

    def clean_up(self):
        print('cleaning up test')
        self.console_logger.clean_up()
        self.shut_down_ditto_api()

    def shut_down_ditto_api(self):
        if self.ditto_api_process is not None:
            self.ditto_api_process = None

    @property
    def ditto_web_api_folder_path(self):
        return os.path.join(self._execution_folder_path, 'ditto_web_api')

    @property
    def log_folder_path(self):
        return os.path.join(self._execution_folder_path, 'logs')

    @property
    def log_level(self):
        return 'DEBUG'

    @property
    def app_port(self):
        return 8888

    @property
    def s3host(self):
        # This is set in Vagrantfile
        return '172.28.129.160'

    @property
    def s3port(self):
        # This is the Minio default
        return 9000

    @property
    def s3access(self):
        # This is set in minio.conf
        return 'AKIAIOSFODNN7EXAMPLE'

    @property
    def s3secret(self):
        # This is set in minio.conf
        return 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'

    @property
    def s3secure(self):
        return 'FALSE'

    @property
    def bucket_standardisation(self):
        return 'systemtest'

    @property
    def local_data_folder_path(self):
        return os.path.join(self._execution_folder_path, 'data')


class BaseSystemTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, request):
        print("setting up test")
        self.context = SystemTestContext()
        self._clean_up_working_folders()
        self._set_up_loggers()
        self.given = GivenSteps(self.context)
        self.when = WhenSteps(self.context)
        self.then = ThenSteps(self.context)
        request.addfinalizer(self.context.clean_up)

    def _set_up_loggers(self):
        self.context.console_logger.set_up()

    def _clean_up_working_folders(self):
        # Clear out the logs
        shutil.rmtree(self.context.log_folder_path)
        os.makedirs(self.context.log_folder_path)

        # Clear out the local data
        shutil.rmtree(self.context.local_data_folder_path)
        os.makedirs(self.context.local_data_folder_path)
