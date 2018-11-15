import os
from DittoWebApi.src.utils.file_system.path_helpers import to_posix


class ExternalDataService:
    def __init__(self, configuration, s3_adapter):
        self._bucket_standard = configuration.bucket_standard
        self._s3_client = s3_adapter

    def get_buckets(self):
        return self._s3_client.list_buckets()

    def get_objects(self, bucket_name, dir_path):
        """Passes list of object of Objects up to data replication service"""
        objects = self._s3_client.list_objects(bucket_name, dir_path, recursive=True)
        objects = [obj for obj in objects if not obj.is_dir]
        return objects

    def does_dir_exist(self, bucket, dir_path):
        objects = self._s3_client.list_objects(bucket, dir_path)
        return len(objects) > 0

    def upload_file(self, bucket_name, processed_file):
        with open(processed_file.abs_path, 'rb') as file:
            file_length = os.stat(processed_file.abs_path).st_size
            self._s3_client.put_object(bucket_name, to_posix(processed_file.rel_path), file, file_length)
        return file_length

    def does_bucket_exist(self, bucket_name):
        return self._s3_client.bucket_exists(bucket_name)

    def create_bucket(self, bucket_name):
        self._s3_client.make_bucket(bucket_name, location="eu-west-1")

    def does_bucket_match_standard(self, bucket_name):
        length_of_bucket_standard = len(self._bucket_standard)
        return bucket_name[:(length_of_bucket_standard + 1)] == (self._bucket_standard + "-")

    def delete_file(self, bucket_name, file_name):
        return self._s3_client.remove_object(bucket_name, file_name)

    def does_object_exist(self, bucket_name, file_name):
        return self._s3_client.object_exists(bucket_name, file_name)
