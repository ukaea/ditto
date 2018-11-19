import boto.s3.connection

from DittoWebApi.src.services.external.storage_adapters.boto_bucket import BotoBucket
from DittoWebApi.src.services.external.storage_adapters.is3_adapter import IS3Adapter


class BotoAdapter(IS3Adapter):
    def __init__(self, configuration, logger):
        self._logger = logger
        try:
            self._s3_client = boto.connect_s3(
                aws_access_key_id=configuration.s3_access_key,
                aws_secret_access_key=configuration.s3_secret_key,
                host=configuration.s3_host,
                port=configuration.s3_port,
                is_secure=configuration.s3_use_secure,
                calling_format=boto.s3.connection.OrdinaryCallingFormat()
            )
        except Exception as exception:
            self._logger.critical(exception)
            raise exception

    def make_bucket(self, bucket_name, location=""):
        try:
            self._s3_client.create_bucket(bucket_name, location=location)
            return True
        except Exception as exception:
            self._logger.error(exception)
            return False

    def get_bucket(self, bucket_name):
        # if the bucket does not exist, lookup() returns None.
        # get_bucket() would throw an exception.
        bucket = self._s3_client.lookup(bucket_name)
        return None if bucket is None else BotoBucket(bucket)
