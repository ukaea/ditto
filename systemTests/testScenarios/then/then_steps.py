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
        assert self._context.response_data(response)["message"] == "objects returned successfully"
        assert self._context.response_data(response)["objects"][0]["object_name"] == "testA.txt"

    def copy_dir_completed_successfully(self, response):
        self.response_returns_status_code_200(response)

    def response_returns_status_code_200(self, response):
        assert response.status_code == 200

    def copy_dir_copied_no_new_files_as_already_exists(self, response):
        print(json.loads(response.text))
        assert self._context.response_data(response)["new files uploaded"] == 0
        assert self._context.response_data(response)["message"] == "Directory None already exists on S3," \
                                                                   " 2 files skipped"

    def response_message_confirms_transfer(self, response):
        assert self._context.response_data(response)["message"] == "Transfer successful"
        assert self._context.response_data(response)["new files uploaded"] == 1


