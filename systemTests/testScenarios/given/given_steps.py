import os
import time
import json

from testScenarios.given.ditto_api_server import DittoApiServer


class GivenSteps:
    def __init__(self, context):
        self._context = context
        self._ditto_api_server = DittoApiServer(context)

    @property
    def ditto_web_api(self):
        return self._ditto_api_server

    def _write_test_file(self, file_name, content):
        with open(os.path.join(self._context.local_data_folder_path, file_name), 'w') as file:
            file.write(content)

    def simple_test_file_is_setup_locally(self):
        self._write_test_file('testA.txt', 'example test content A')

    def simple_sub_dir_with_test_file_is_setup_locally(self):
        self._write_test_file_locally_in_sub_dir(os.path.join('sub_dir_A', 'testB.txt'), 'example test content B')

    def _write_test_file_locally_in_sub_dir(self, file_name, content):
        filename = os.path.join(self._context.local_data_folder_path, file_name)
        os.makedirs(os.path.dirname(filename))
        with open(filename, 'w') as file:
            file.write(content)

    def standard_bucket_exists_in_s3(self):
        self._make_s3_bucket(self._context.standard_bucket_name)

    def update_simple_file(self):
        file_path = os.path.join(self._context.local_data_folder_path, 'testA.txt')
        new_content = ". A new bit of text"
        with open(file_path, 'a') as file:
            file.write(new_content)

    def _make_s3_bucket(self, bucket):
        bucket_path = os.path.join(self._context.s3_data_folder_path, bucket)
        os.system(f"mkdir {bucket_path}")
        os.system(f"sudo chown 'minio':'minio' {bucket_path}/")
        os.system(f"sudo chmod 0777 {bucket_path}/")

    def _make_s3_sub_dir(self, bucket, sub_dir_name):
        sub_dir_path = os.path.join(self._context.s3_data_folder_path, bucket, sub_dir_name)
        os.system(f"mkdir {sub_dir_path}")
        os.system(f"sudo chown 'minio':'minio' {sub_dir_path}/")
        os.system(f"sudo chmod 0777 {sub_dir_path}/")

    def _create_file_in_s3(self, bucket, file_name, content):
        file_path = os.path.join(self._context.s3_data_folder_path, bucket, file_name)
        os.system(f"sudo echo {content} > {file_path}")
        os.system(f"sudo chown -R 'minio':'minio' {file_path}")

    def simple_test_file_is_setup_in_s3(self):
        self._create_file_in_s3(self._context.standard_bucket_name, 'testA.txt', 'example test content A')

    def simple_sub_dir_with_test_file_is_setup_in_s3(self):
        self._make_s3_sub_dir(self._context.standard_bucket_name, 'sub_dir_A')
        self._create_file_in_s3(self._context.standard_bucket_name,
                                os.path.join('sub_dir_A', 'testB.txt'),
                                'example test content B')

    def archive_file_already_exists_in_local_root(self):
        file_path = os.path.join(self._context.local_data_folder_path, ".ditto_archived")
        content = '{}'
        with open(file_path, 'w') as file:
            file.write(content)
        self._context.archive_creation_time = time.time()

    def old_transfer_in_archive_file(self):
        file_path = os.path.join(self._context.local_data_folder_path, ".ditto_archived")
        content = {"testB.txt":
                       {"file": "testB.txt",
                        "size": 22,
                        "latest update": "1543590765.7174373",
                        "type of transfer": "new upload"}
                   }
        with open(file_path, 'w') as file:
            json.dump(content, file)
        self._context.archive_creation_time = time.time()


    @staticmethod
    def s3_interface_is_running():
        os.system("sudo systemctl start minio")
