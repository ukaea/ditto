from abc import ABCMeta, abstractmethod

class IS3Adapter(metaclass=ABCMeta):
    @abstractmethod
    def list_buckets(self):
        pass

    @abstractmethod
    def list_objects(self, bucket_name, directory_to_search, recursive=True):
        pass

    @abstractmethod
    def put_object(self, bucket_name, object_name, data, length,
                   content_type='application/octet-stream', metadata=None):
        pass

    @abstractmethod
    def make_bucket(self, bucket_name, location="eu-west-1"):
        pass

    @abstractmethod
    def bucket_exists(self, bucket_name):
        pass

    @abstractmethod
    def stat_object(self, bucket_name, object_name):
        pass

    @abstractmethod
    def remove_object(self, bucket_name, object_name):
        pass
