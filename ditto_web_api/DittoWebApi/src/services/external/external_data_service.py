import os
from minio.error import NoSuchKey
from DittoWebApi.src.utils.file_system.path_helpers import to_posix
from DittoWebApi.src.models.bucket_information import Bucket
from DittoWebApi.src.models.object_information import Object
from DittoWebApi.src.services.external.storage_adapters.minio_adaptor import MinioAdapter


class ExternalDataService:
    def __init__(self, configuration):
        self._s3_client = MinioAdapter(configuration)
        self._bucket_standard = configuration.bucket_standard

    def get_buckets(self):
        return [Bucket(bucket) for bucket in self._s3_client.list_buckets()]

    def get_objects(self, buckets, dir_path):
        """Passes list of object of Objects up to data replication service"""
        objs = []
        for bucket in buckets:
            bucket = Bucket(bucket)
            objects = self._s3_client.list_objects(bucket.name, dir_path, recursive=True)
            objs += [Object(obj) for obj in objects if not obj.is_dir]
        return objs

    def does_dir_exist(self, dir_path, bucket):
        objects = [obj for obj in self._s3_client.list_objects(bucket, dir_path)]
        return len(objects) > 0

    def upload_file(self, processed_file, target_bucket):
        bucket_name = target_bucket.name
        with open(processed_file.abs_path, 'rb') as file:
            file_length = os.stat(processed_file.abs_path).st_size
            self._s3_client.put_object(bucket_name, to_posix(processed_file.rel_path), file, file_length)
        return file_length

    def does_bucket_exist(self, bucket_name):
        return self._s3_client.bucket_exists(bucket_name)

    def create_bucket(self, bucket_name):
        self._s3_client.make_bucket(bucket_name, location="eu-west-1")

    def is_valid_bucket(self, bucket_name):
        return bucket_name.split('-')[0] == self._bucket_standard

    def delete_file(self, file_name, bucket_name):
        self._s3_client.remove_object(bucket_name, file_name)

    def does_object_exist(self, file_name, bucket_name):
        try:
            self._s3_client.stat_object(bucket_name, file_name)
            return True
        except NoSuchKey:
            return False
