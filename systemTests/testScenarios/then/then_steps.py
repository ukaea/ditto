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
        assert os.path.isdir(bucket_dir_path)

    def new_simple_file_exists_in_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path,
                                 'systemtest-textbucket',
                                 self._context.simple_file_name)
        assert os.path.exists(file_path)

    def new_file_exists_in_sub_dir_of_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path,
                                 'systemtest-textbucket',
                                 'sub_dir_A/testB.txt')
        assert os.path.exists(file_path)

    def list_present_response_body_shows_simple_file_in_s3(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["message"] == "objects returned successfully"
        assert self._context.file_name_in_objects_returned_in_list_present_body('testA.txt', response)

    def list_present_response_body_shows_file_in_sub_dir_in_s3(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["message"] == "objects returned successfully"
        assert self._context.file_name_in_objects_returned_in_list_present_body('sub_dir_A/testB.txt', response)

    def list_present_response_body_shows_simple_file_not_in_s3(self):
        response = self._context.http_client_response
        assert self._context.file_name_in_objects_returned_in_list_present_body('testA.txt', response) is False

    def response_returns_status_code_200(self):
        response = self._context.http_client_response
        assert response.status_code == 200

    def response_status_is_success(self):
        response = self._context.http_client_response
        assert self._context.response_status(response) == "success"

    def response_shows_request_was_completed_successfully(self):
        self.response_returns_status_code_200()
        self.response_status_is_success()

    def response_shows_copy_dir_copied_no_new_files_as_directory_already_exists(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["new files uploaded"] == 0
        assert self._context.response_data(response)["message"] == "Directory root already exists on S3," \
                                                                   " 2 files skipped"

    def response_message_confirms_transfer(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["message"] == "Transfer successful"

    def response_message_body_indicates_one_new_file_uploaded(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["new files uploaded"] == 1

    def response_shows_warning_as_bucket_does_not_exist(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["message"] == "Warning, bucket does not exist " \
                                                                   "(systemtest-textbucket)"

    def response_confirms_simple_file_deleted(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["message"] == 'File testA.txt successfully deleted ' \
                                                                   'from bucket systemtest-textbucket'

    def simple_file_does_not_exist_in_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path,
                                 'systemtest-textbucket',
                                 self._context.simple_file_name)
        assert os.path.exists(file_path) is False

    def response_shows_old_file_skipped(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["files skipped"] == 1

    def response_indicates_no_new_file_uploaded(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["new files uploaded"] == 0

    def response_indicates_no_files_updated(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["files updated"] == 0

    def response_message_body_indicates_one_file_updated(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["files updated"] == 1

    def simple_file_content_is_updated_on_s3(self):
        file_path = os.path.join(self._context.s3_data_folder_path,
                                 'systemtest-textbucket',
                                 self._context.simple_file_name)
        with open(file_path, 'r') as file:
            content = file.read()
        assert content == 'example test content A. A new bit of text'

    def response_message_complains_simple_file_does_not_exist(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["message"] == "File testA.txt does not exist" \
                                                                   " in bucket systemtest-textbucket"

    def response_message_complains_directory_does_not_exist(self):
        response = self._context.http_client_response
        assert self._context.response_data(response)["message"] == "No files found in directory" \
                                                                   " or directory does not exist (root)"

    def response_shows_no_objects_in_bucket(self):
        response = self._context.http_client_response
        assert self._context.object_names_from_list_present_response_body(response) == []
