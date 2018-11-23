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

    def simple_bucket_exists_in_s3(self):
        bucket_dir_path = os.path.join(self._context.s3_data_folder_path, 'systemtest-textbucket')
        assert os.path.isdir(bucket_dir_path)

    def new_simple_file_exists_in_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path,
                                 'systemtest-textbucket',
                                 self._context.simple_file_name)
        assert os.path.exists(file_path)

    def list_present_response_body_shows_returned_newly_created_file(self, response):
        assert self._context.response_data(response)["message"] == "objects returned successfully"
        assert self._context.file_name_in_objects_returned_in_list_present_body('testA.txt', response)
        assert self._context.file_name_in_objects_returned_in_list_present_body('sub_dir_A/testB.txt', response)

    def response_returns_status_code_200(self, response):
        assert response.status_code == 200

    def response_status_is_success(self, response):
        assert self._context.response_status(response) == "success"

    def response_shows_request_was_completed_successfully(self, response):
        self.response_returns_status_code_200(response)
        self.response_status_is_success(response)

    def response_shows_copy_dir_copied_no_new_files_as_directory_already_exists(self, response):
        print(json.loads(response.text))
        assert self._context.response_data(response)["new files uploaded"] == 0
        assert self._context.response_data(response)["message"] == "Directory None already exists on S3," \
                                                                   " 2 files skipped"

    def response_message_confirms_transfer(self, response):
        assert self._context.response_data(response)["message"] == "Transfer successful"

    def response_message_body_indicates_one_new_file_uploaded(self, response):
        assert self._context.response_data(response)["new files uploaded"] == 1



