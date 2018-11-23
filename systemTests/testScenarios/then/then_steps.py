import os

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
        print(bucket_dir_path)
        assert os.path.isdir(bucket_dir_path)

    def new_file_exists_in_s3_bucket(self):
        print(self._context.response.text)
        file_path = os.path.join(self._context.s3_data_folder_path, 'systemtest-textbucket', 'testA.txt')
        print(file_path)
        assert os.path.exists(file_path)

    def list_present_body_shows_newly_created_file(self):
        print(self._context.response.text)
        assert self._context.response.text == {"status": "success",
                                               "data":
                                                   {"message": "objects returned successfully", "objects": []}
                                               }
