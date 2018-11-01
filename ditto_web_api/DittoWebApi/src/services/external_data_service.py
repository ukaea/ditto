from minio import Minio
from DittoWebApi.src.models.bucket import Bucket
from DittoWebApi.src.models.object import Object


class ExternalDataService:
    def __init__(self, configuration):
        self.s3_client = Minio(configuration.s3_url,
                               configuration.s3_access_key,
                               configuration.s3_secret_key,
                               configuration.s3_use_secure)
        self._buckets = self.s3_client.list_buckets()

    def get_objects(self):
        objs = []
        for bucket in self._buckets:
            bucket = Bucket(bucket)
            objects = self.s3_client.list_objects(bucket.name)
            for obj in objects:
                obj = Object(obj)
                objs.append(obj.to_dict())
        return objs

