from minio import Minio
from minio.error import ResponseError


class MinioAdapter:
    def __init__(self, configuration):
        self._s3_client = Minio(configuration.s3_url,
                                configuration.s3_access_key,
                                configuration.s3_secret_key,
                                configuration.s3_use_secure)

    def list_buckets(self):
        return self._s3_client.list_buckets()

    def list_objects(self, bucket_name, directory_to_search, recursive=True):
        return self._s3_client.list_objects(bucket_name, directory_to_search, recursive)

    def put_object(self, bucket_name, object_name, data, length,
                   content_type='application/octet-stream', metadata=None):
        return self._s3_client.put_object(bucket_name, object_name, data, length, content_type, metadata)

    def make_bucket(self, bucket_name, location="eu-west-1"):
        return self._s3_client.make_bucket(bucket_name, location)

    def bucket_exists(self, bucket_name):
        return self._s3_client.bucket_exists(bucket_name)

    def stat_object(self, object_name, bucket_name):
        return self._s3_client.stat_object(bucket_name, object_name)

    def remove_object(self, object_name, bucket_name):
        return self._s3_client.remove_object(bucket_name, object_name)
