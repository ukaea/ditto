import os
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
