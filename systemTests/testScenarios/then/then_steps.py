import os
import json

from .log_file_steps import LogFileSteps


class ThenSteps:
    def __init__(self, context):
        self._context = context
        self.console_output = LogFileSteps(context, 'console-stdout.log')
        self.console_error = LogFileSteps(context, 'console-stderr.log')
        self.ditto_api_log = LogFileSteps(context, 'ditto_api_server.log')

    # Private properties

    @property
    def _standard_s3_bucket_path(self):
        return os.path.join(self._context.s3_data_folder_path, self._context.standard_bucket_name)

    @property
    def _simple_s3_file_path(self):
        return os.path.join(self._context.s3_data_folder_path,
                            self._context.standard_bucket_name,
                            self._context.simple_file_name)

    # Public methods: archive

    def archive_file_exists_in_root_dir(self):
        file_path = os.path.join(self._context.local_data_folder_path, ".ditto_archived")
        assert os.path.exists(file_path)

    def archive_file_does_not_exist_in_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path, ".ditto_archived")
        assert os.path.exists(file_path) is False

    def archive_file_exists_in_sub_dir(self):
        file_path = os.path.join(self._context.local_data_folder_path, "sub_dir_A", ".ditto_archived")
        assert os.path.exists(file_path)

    # Public methods: directories and files

    def standard_s3_bucket_exists(self):
        assert os.path.isdir(self._standard_s3_bucket_path)

    def standard_s3_bucket_does_not_exist(self):
        assert not os.path.isdir(self._standard_s3_bucket_path)

    def simple_file_exists_in_s3_bucket(self):
        assert os.path.isfile(self._simple_s3_file_path)

    def simple_file_does_not_exist_in_s3_bucket(self):
        assert not os.path.exists(self._simple_s3_file_path)

    def simple_file_content_is_updated_on_s3(self):
        with open(self._simple_s3_file_path, 'r') as file:
            content = file.read()
        assert content == 'example test content A. A new bit of text'

    def file_exists_in_sub_dir_of_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path,
                                 self._context.standard_bucket_name,
                                 'sub_dir_A',
                                 'testB.txt')
        assert os.path.isfile(file_path)

    # Public methods: HTTP responses

    def response_shows_no_objects_in_bucket(self):
        assert self._context.object_names_from_list_present_response_body() == []

    def response_body_shows_simple_file_in_s3(self):
        assert self._context.response_data()["message"] == "objects returned successfully"
        assert 'testA.txt' in self._context.object_names_from_list_present_response_body()

    def response_body_shows_simple_file_not_in_s3(self):
        assert 'testA.txt' not in self._context.object_names_from_list_present_response_body()

    def response_body_shows_file_in_sub_dir_in_s3(self):
        assert self._context.response_data()["message"] == "objects returned successfully"
        sub_dir_file = os.path.join('sub_dir_A', 'testB.txt')
        assert sub_dir_file in self._context.object_names_from_list_present_response_body()

    def response_shows_request_was_completed_successfully(self):
        assert self._context.response_status() == "success"

    def response_shows_request_failed(self):
        assert self._context.response_status() == "fail"

    def response_shows_copy_dir_copied_no_new_files_as_directory_already_exists(self):
        assert self._context.response_data()["new files uploaded"] == 0
        assert "Directory root already exists" in self._context.response_data()["message"]
        assert self._context.response_data()["files skipped"] > 0

    def response_message_confirms_transfer(self):
        assert self._context.response_data()["message"] == "Transfer successful"

    def response_message_body_indicates_one_new_file_uploaded(self):
        assert self._context.response_data()["new files uploaded"] == 1

    def response_shows_warning_as_bucket_does_not_exist(self):
        assert self._context.response_data() == "Warning, bucket does not exist " \
                                                                   "(systemtest-textbucket)"

    def response_shows_error_that_bad_bucket_name_given(self):
        assert "Bucket name breaks S3 naming convention" in \
               self._context.response_data() or \
               "Bucket breaks local naming standard" in\
               self._context.response_data()

    def response_confirms_simple_file_deleted(self):
        assert self._context.response_data()["message"] == 'File testA.txt successfully deleted ' \
                                                                   'from bucket systemtest-textbucket'

    def response_shows_one_file_skipped(self):
        assert self._context.response_data()["files skipped"] == 1

    def response_indicates_no_new_file_uploaded(self):
        assert self._context.response_data()["new files uploaded"] == 0

    def response_indicates_no_files_updated(self):
        assert self._context.response_data()["files updated"] == 0

    def response_message_body_indicates_one_file_updated(self):
        assert self._context.response_data()["files updated"] == 1

    def response_data_reports_simple_file_does_not_exist(self):
        assert self._context.response_data() == "File testA.txt does not exist" \
                                                                   " in bucket systemtest-textbucket"

    def response_data_reports_directory_does_not_exist(self):
        assert self._context.response_data() == "No files found in directory" \
                                                                   " or directory does not exist (root)"

    def response_fails_with_reason_authentication_required(self):
        assert json.loads(self._context.http_client_response.text)["data"] == "Authentication required"

    def response_shows_failed_as_unauthorised(self):
        assert self._context.http_client_response.json()['data'] == 'Not authorised for this bucket'

    def response_shows_failed_as_not_admin(self):
        assert self._context.http_client_response.json()['data'] == 'Administrator authorisation required'

    def response_status_is(self, status_code):
        assert self._context.http_client_response.status_code == status_code

    def archive_file_exists_in_archive_root_dir(self):
        file_path = os.path.join(self._context.local_archive_root_path, ".ditto_archived")
        assert os.path.exists(file_path)

    def archive_file_has_been_updated(self):
        file_path = os.path.join(self._context.local_archive_root_path, ".ditto_archived")
        last_modified = os.path.getmtime(file_path)
        assert last_modified > self._context.archive_creation_time

    def archive_file_exists_in_sub_dir_of_archive_root(self):
        file_path = os.path.join(self._context.local_archive_root_path, "sub_dir_A", ".ditto_archived")
        assert os.path.exists(file_path)

    def archive_content_is_as_expected(self):
        file_path = os.path.join(self._context.local_archive_root_path, ".ditto_archived")
        expected_content = "test"
        with open(file_path, 'rt') as file:
            content = file.read()
        assert content == expected_content

    def archive_file_does_not_exist_in_s3_bucket(self):
        file_path = os.path.join(self._context.s3_data_folder_path, ".ditto_archived")
        assert os.path.exists(file_path) is False

    def updated_archive_file_content_is_as_expected(self):
        file_path = os.path.join(self._context.local_archive_root_path, ".ditto_archived")
        expected_content = "test test"
        with open(file_path, 'rt') as file:
            content = file.read()
        assert content == expected_content

    def bucket_settings_includes_standard_bucket(self):
        file_path = os.path.join(self._context.ditto_web_api_folder_path, 'DittoWebApi', 'bucket_settings.ini')
        expected_content = f'[{self._context.standard_bucket_name}]\n'\
            'groups = group1,group2\n'\
            f'root = {self._context.local_data_folder_path}\n'
        with open(file_path, 'r') as file:
            content = file.read()
        assert expected_content in content

    def bucket_settings_file_does_not_exist(self):
        file_path = os.path.join(self._context.ditto_web_api_folder_path, 'DittoWebApi', 'bucket_settings.ini')
        assert not os.path.isfile(file_path)

    def simple_file_is_in_root_archive_file_as_new_upload(self):
        file_name = self._context.simple_file_name
        assert self._file_in_archive_file_at_folder_with_specified_type(file_name, None, 'new upload') is True

    def simple_file_is_in_root_archive_file_as_updated_file(self):
        file_name = self._context.simple_file_name
        assert self._file_in_archive_file_at_folder_with_specified_type(file_name, None, 'file update') is True

    def file_in_sub_dir_is_in_archive_in_sub_dir_as_new_upload(self):
        file_name = self._context.file_in_sub_dir_name
        directory = self._context.simple_sub_dir
        assert self._file_in_archive_file_at_folder_with_specified_type(file_name, directory, 'new upload') is True

    def file_in_sub_dir_is_in_archive_in_sub_dir_as_file_update(self):
        file_name = self._context.file_in_sub_dir_name
        directory = self._context.simple_sub_dir
        assert self._file_in_archive_file_at_folder_with_specified_type(file_name, directory, 'file update') is True

    def _file_in_archive_file_at_folder_with_specified_type(self, file_name, directory, type_of_transfer):
        root_to_directory = os.path.join(self._context.local_archive_root_path, directory) \
            if directory \
            else self._context.local_archive_root_path
        file_path = os.path.join(root_to_directory, ".ditto_archived")
        print(file_path)
        with open(file_path, 'r') as file:
            content = json.load(file)
            print(content)
        try:
            content[file_name]
        except KeyError:
            return False
        return content[file_name]['type of transfer'] == type_of_transfer

    def old_content_in_archive_file_is_untouched(self):
        file_name = self._context.file_in_sub_dir_name
        file_path = os.path.join(self._context.local_archive_root_path, ".ditto_archived")
        print(file_path)
        with open(file_path, 'r') as file:
            content = json.load(file)
        try:
            content[file_name]
        except KeyError:
            return False
        return content[file_name] is {
            "testB.txt":
                {"file": "testB.txt",
                 "size": 22,
                 "latest update": "1970-01-01 03:25:45",
                 "type of transfer": "new upload"}
                                      }
