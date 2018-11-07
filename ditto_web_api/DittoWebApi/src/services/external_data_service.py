import os
import re
from minio import Minio
from DittoWebApi.src.utils.path_helpers import to_posix
from DittoWebApi.src.models.bucket import Bucket
from DittoWebApi.src.models.object import Object


class ExternalDataService:
    def __init__(self, configuration):
        self._s3_client = Minio(configuration.s3_url,
                                configuration.s3_access_key,
                                configuration.s3_secret_key,
                                configuration.s3_use_secure)
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

    def valid_bucket(self, bucket_name):
        if len(bucket_name) > 63:
            return False
        if '..' in bucket_name:
            return False
        match = re.compile('^[a-z0-9][a-z0-9\\.\\-]+[a-z0-9]$').match(bucket_name)
        if match is None or match.end() != len(bucket_name):
            return False
        return bucket_name.split('-')[0] == self._bucket_standard
