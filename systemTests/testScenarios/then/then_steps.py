import os
import json

from .log_file_steps import LogFileSteps


class ThenSteps:
    def __init__(self, context):
        self._context = context
        self.console_output = LogFileSteps(context, 'console-stdout.log')
        self.console_error = LogFileSteps(context, 'console-stderr.log')
        self.ditto_api_log = LogFileSteps(context, 'ditto_api_server.log')

    def thing_is_true(self):
        assert isinstance(self, ThenSteps)

    def thing_is_false(self):
        assert isinstance(self, list)

    def simple_bucket_exists_in_s3(self, response):
        bucket_dir_path = os.path.join(self._context.s3_data_folder_path, 'systemtest-textbucket')
        assert os.path.isdir(bucket_dir_path)
        assert response.status_code == 200

    def new_file_exists_in_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path, 'systemtest-textbucket', 'testA.txt')
        assert os.path.exists(file_path)


    def list_present_body_shows_newly_created_file(self, response):
        assert response.status_code == 200
        assert json.loads(response.text)["data"]["message"] == "objects returned successfully"
        assert json.loads(response.text)["data"]["objects"][0]["object_name"] == "testA.txt"

    def copy_dir_completed_sucessfully(self, response):
        assert response.status_code == 200



