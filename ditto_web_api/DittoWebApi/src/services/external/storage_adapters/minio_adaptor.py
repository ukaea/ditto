from minio import Minio
from minio.error import NoSuchKey
from minio.error import ResponseError
from DittoWebApi.src.models.bucket_information import BucketInformation
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.services.external.storage_adapters.is3_adapter import IS3Adapter


class MinioAdapter(IS3Adapter):
    def __init__(self, configuration):
        self._s3_client = Minio(configuration.s3_host + ":" + str(configuration.s3_port),
                                configuration.s3_access_key,
                                configuration.s3_secret_key,
                                configuration.s3_use_secure)

    @staticmethod
    def _get_bucket_information(minio_bucket):
        return BucketInformation.create(
            minio_bucket.name,
            minio_bucket.creation_date
        )

    @staticmethod
    def _get_s3_object_information(minio_object):
        return S3ObjectInformation.create(
            minio_object.object_name,
            minio_object.bucket_name,
            minio_object.is_dir,
            minio_object.size,
            minio_object.etag,
            minio_object.last_modified
        )

    def list_buckets(self):
        minio_buckets = self._s3_client.list_buckets()
        ditto_buckets = [MinioAdapter._get_bucket_information(minio_bucket) for minio_bucket in minio_buckets]
        return ditto_buckets

    def list_objects(self, bucket_name, directory_to_search, recursive=True):
        minio_objects = self._s3_client.list_objects(bucket_name, directory_to_search, recursive)
        ditto_objects = [MinioAdapter._get_s3_object_information(minio_object) for minio_object in minio_objects]
        return ditto_objects

    def put_object(self, bucket_name, object_name, data, length,
                   content_type='application/octet-stream', metadata=None):
        try:
            self._s3_client.put_object(bucket_name, object_name, data, length, content_type, metadata)
            return True
        except ResponseError:
            return False

    def make_bucket(self, bucket_name, location="eu-west-1"):
        try:
            self._s3_client.make_bucket(bucket_name, location)
            return True
        except ResponseError:
            return False

    def bucket_exists(self, bucket_name):
        return self._s3_client.bucket_exists(bucket_name)

    def object_exists(self, bucket_name, object_name):
        try:
            self._s3_client.stat_object(bucket_name, object_name)
            return True
        except NoSuchKey:
            return False

    def remove_object(self, bucket_name, object_name):
        try:
            self._s3_client.remove_object(bucket_name, object_name)
            return True
        except ResponseError:
            return False
