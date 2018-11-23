from abc import ABCMeta, abstractmethod


class ISecurityService(metaclass=ABCMeta):

    @abstractmethod
    def is_authenticated(self, name, password):
        pass

    @abstractmethod
    def is_in_group(self, name, group):
        pass
