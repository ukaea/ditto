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
        self.execution_folder_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..',
            'execution_space'
        ))
        self.ditto_api_process = None
        self.console_logger = ProcessLogger('console')

    def clean_up(self):
        print('cleaning up test')
        self.console_logger.clean_up()
        self.shut_down_ditto_api()

    def shut_down_ditto_api(self):
        if self.ditto_api_process is not None:
            self.ditto_api_process = None


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
        # clear out the old logs

        #the following two lines should probably be uncommented but, when they are,the first test gets an error
        #shutil.rmtree(self.context.execution_folder_path + '/logs')
        #os.makedirs(self.context.execution_folder_path + '/logs')

        shutil.rmtree(self.context.execution_folder_path + '/testing_area')
        os.makedirs(self.context.execution_folder_path + '/testing_area/src')
        os.makedirs(self.context.execution_folder_path + '/testing_area/staging')
        os.makedirs(self.context.execution_folder_path + '/testing_area/target')

