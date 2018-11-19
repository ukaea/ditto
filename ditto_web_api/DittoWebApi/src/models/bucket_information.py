# pylint: disable=W0212
class BucketInformation:
    def __init__(self):
        self._name = None
        self._creation_date = None

    @property
    def name(self):
        return self._name

    @property
    def creation_date(self):
        return self._creation_date

    @staticmethod
    def create(name, creation_date):
        output = BucketInformation()
        output._name = name
        output._creation_date = creation_date
        return output
