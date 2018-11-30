import os

from testScenarios.given.ditto_api_server import DittoApiServer


class GivenSteps:
    def __init__(self, context):
        self._context = context
        self._ditto_api_server = DittoApiServer(context)

    # Properties

    @property
    def ditto_web_api(self):
        return self._ditto_api_server

    # Private methods

    def _make_dir_for_s3(self, bucket, sub_dir_path=None):
        dir_path = os.path.join(self._context.s3_data_folder_path, bucket)
        dir_path = dir_path if sub_dir_path is None else os.path.join(dir_path, sub_dir_path)
        os.system(f"mkdir {dir_path}")
        os.system(f"sudo chown 'minio':'minio' {dir_path}/")
        os.system(f"sudo chmod 0777 {dir_path}/")

    def _write_file_in_s3(self, bucket_name, file_rel_path, content):
        file_path = os.path.join(self._context.s3_data_folder_path, bucket_name, file_rel_path)
        os.system(f"sudo echo {content} > {file_path}")
        os.system(f"sudo chown -R 'minio':'minio' {file_path}")

    def _write_file_locally(self, file_rel_path, content):
        file_path = os.path.join(self._context.local_data_folder_path, file_rel_path)
        dir_path = os.path.dirname(file_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        with open(file_path, 'w') as file:
            file.write(content)

    # Public methods

    def archive_file_already_exists_in_local_root(self):
        self._write_file_locally(".ditto_archived", "test")

    @staticmethod
    def s3_interface_is_running():
        os.system("sudo systemctl start minio")

    def simple_file_is_updated(self):
        file_path = os.path.join(self._context.local_data_folder_path, 'testA.txt')
        new_content = ". A new bit of text"
        with open(file_path, 'a') as file:
            file.write(new_content)

    def simple_sub_dir_with_test_file_exists_in_s3(self):
        file_rel_path = os.path.join('sub_dir_A', 'testB.txt')
        content = 'example test content B'
        self._make_dir_for_s3(self._context.standard_bucket_name, sub_dir_path='sub_dir_A')
        self._write_file_in_s3(self._context.standard_bucket_name, file_rel_path, content)

    def simple_sub_dir_with_test_file_exists_locally(self):
        file_rel_path = os.path.join('sub_dir_A', 'testB.txt')
        content = 'example test content B'
        self._write_file_locally(file_rel_path, content)

    def simple_test_file_exists_in_s3(self):
        self._write_file_in_s3(self._context.standard_bucket_name, 'testA.txt', 'example test content A')

    def simple_test_file_exists_locally(self):
        self._write_file_locally('testA.txt', 'example test content A')

    def standard_bucket_exists_in_s3(self):
        self._make_dir_for_s3(self._context.standard_bucket_name)
