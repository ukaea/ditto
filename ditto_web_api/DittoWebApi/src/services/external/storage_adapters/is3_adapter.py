from abc import ABCMeta, abstractmethod


class IS3Adapter(metaclass=ABCMeta):

    @abstractmethod
    def get_bucket(self, bucket_name):
        pass

    @abstractmethod
    def make_bucket(self, bucket_name, location=""):
        pass
