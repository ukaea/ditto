import os
import shutil
import signal
import unittest
import pytest
import json

from testScenarios.given.given_steps import GivenSteps
from testScenarios.when.when_steps import WhenSteps
from testScenarios.then.then_steps import ThenSteps
from testScenarios.tools.process_logger import ProcessLogger


class SystemTestContext:
    def __init__(self):
        self._execution_folder_path = '/home/vagrant/systemTests/execution_space'
        self.ditto_api_process = None
        self.console_logger = ProcessLogger('console', self.log_folder_path)
        self.http_client_response = None

    def clean_up(self):
        print('cleaning up test')
        self.shut_down_ditto_api()
        self.console_logger.clean_up()

    def shut_down_ditto_api(self):
        print(f'Shutting down DITTO API process on port {self.app_port}')
        process_id = os.getpgid(self.ditto_api_process.pid)
        print(f'Process has ID {process_id}')
        os.killpg(process_id, signal.SIGTERM)
        if self.ditto_api_process is not None:
            self.ditto_api_process = None

    @property
    def ditto_web_api_folder_path(self):
        return os.path.join(self._execution_folder_path, 'ditto_web_api')
        # return '/home/vagrant/ditto_web_api'

    @property
    def log_folder_path(self):
        return os.path.join(self._execution_folder_path, 'logs')

    @property
    def log_level(self):
        return 'DEBUG'

    @property
    def app_port(self):
        return 8080

    @property
    def host_address(self):
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
        return "/usr/tmp/data"

    @property
    def s3_data_folder_path(self):
        return '/opt/minio/data'

    def _response_body_as_json(self):
        return json.loads(self.http_client_response.text)

    def response_status(self):
        return self._response_body_as_json()["status"]

    def response_data(self):
        return self._response_body_as_json()["data"]

    def object_names_from_list_present_response_body(self):
        objects = self.response_data()["objects"]
        return [obj["object_name"] for obj in objects]

    def file_name_in_objects_returned_in_list_present_body(self, file_name):
        objects_in_response = self.object_names_from_list_present_response_body()
        return file_name in objects_in_response

    @property
    def standard_bucket_name(self):
        return 'systemtest-textbucket'

    @property
    def simple_file_name(self):
        return "testA.txt"

class BaseSystemTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self, request):
        print("setting up test")
        self.context = SystemTestContext()
        self._clean_up_working_folders()
        self._clear_up_s3_data()
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

    def _clear_up_s3_data(self):
        # Find everything in the s3_data_folder_path
        s3_items = os.listdir(self.context.s3_data_folder_path)
        s3_items = [os.path.join(self.context.s3_data_folder_path, s3_item) for s3_item in s3_items]
        # Filter this to just directories that match the bucket standardisation
        s3_dirs = [s3_dir for s3_dir in s3_items if os.path.isdir(s3_dir)]
        s3_dirs = [s3_dir for s3_dir in s3_dirs if self._s3_dir_belongs_to_system_tests(s3_dir)]
        # Delete these directories
        for s3_dir in s3_dirs:
            if s3_dir.strip() == "*":
                raise SystemError
            os.system(f"sudo rm -rf {s3_dir}")

    def _s3_dir_belongs_to_system_tests(self, s3_dir):
        base_name = os.path.basename(s3_dir)
        nchar = len(self.context.bucket_standardisation)+1
        target = self.context.bucket_standardisation + '-'
        return base_name[:nchar] == target
