from boto.exception import S3CreateError
from boto.exception import S3ResponseError
from boto.s3.bucketlistresultset import BucketListResultSet
import boto.s3.connection
from DittoWebApi.src.models.bucket_information import BucketInformation
from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.services.external.storage_adapters.is3_adapter import IS3Adapter


class BotoAdapter(IS3Adapter):
    def __init__(self, configuration):
        self._s3_client = boto.connect_s3(
                aws_access_key_id=configuration.s3_access_key,
                aws_secret_access_key=configuration.s3_secret_key,
                host=configuration.s3_host,
                port=configuration.s3_port,
                is_secure=configuration.s3_use_secure,
                calling_format=boto.s3.connection.OrdinaryCallingFormat()
        )

    @staticmethod
    def _get_bucket_information(boto_bucket):
        return BucketInformation.create(
            boto_bucket.name,
            boto_bucket.creation_date
        )

    @staticmethod
    def _get_s3_object_information(boto_object):
        return S3ObjectInformation.create(
            boto_object.object_name,
            boto_object.bucket_name,
            boto_object.is_dir,
            boto_object.etag,
            boto_object.last_modified
        )

    def _get_bucket(self, bucket_name):
        try:
            return self._s3_client.get_bucket(bucket_name)
        except S3ResponseError:
            return None

    def list_buckets(self):
        return self._s3_client.list_buckets()

    def list_objects(self, bucket_name, directory_to_search, recursive=True):
        bucket = self._get_bucket(bucket_name)
        if bucket is None:
            return []
        results_set = bucket.list(prefix=directory_to_search)
        objects = [BotoAdapter._get_s3_object_information(boto_object) for boto_object in results_set]
        return objects


    def put_object(self, bucket_name, object_name, data, length,
                   content_type='application/octet-stream', metadata=None):
        bucket = self._get_bucket()
        if bucket is None:
            return False
        key = bucket.get_key(object_name)
        # try:
        key.set_contents_from_filename(object_name)
        return True
        # except ResponseError:
        # return False

    def make_bucket(self, bucket_name, location="eu-west-1"):
        try:
            self._s3_client.create_bucket(bucket_name, location)
            return True
        except S3CreateError:
            return False

    def bucket_exists(self, bucket_name):
        bucket = self._s3_client.lookup(bucket_name)
        return bucket is not None

    def stat_object(self, bucket_name, object_name):
        return self._s3_client.stat_object(bucket_name, object_name)

    def remove_object(self, bucket_name, object_name):
        bucket = self._get_bucket()
        if bucket is None:
            return False
        key = bucket.get_key(object_name)
        key.delete()
        return True
