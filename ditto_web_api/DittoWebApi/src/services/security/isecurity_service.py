from abc import ABCMeta, abstractmethod


class ISecurityService(metaclass=ABCMeta):

    @abstractmethod
    def check_credentials(self, name, password):
        pass

    @abstractmethod
    def is_in_group(self, name, group):
        pass
