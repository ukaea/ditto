from minio import Minio
from DittoWebApi.src.models.bucket import Bucket
from DittoWebApi.src.models.object import Object


class ExternalDataService:
    def __init__(self, configuration):
        self._s3_client = Minio(configuration.s3_url,
                                configuration.s3_access_key,
                                configuration.s3_secret_key,
                                configuration.s3_use_secure)

    def get_buckets(self):
        self._buckets = [Bucket(bucket) for bucket in self._s3_client.list_buckets()]
        return self._buckets

    def get_objects(self, buckets):
        """Passes list of object of Objects up to data replication service"""
        objs = []
        for bucket in buckets:
            bucket = Bucket(bucket)
            objects = self._s3_client.list_objects(bucket.name)
            objs += [Object(obj) for obj in objects]
        return objs

    def upload(self, processed_file, target_bucket):
        bucket_name = target_bucket.name
        self._s3_client.put_object(bucket_name, processed_file.name, processed_file.data, processed_file.length)

