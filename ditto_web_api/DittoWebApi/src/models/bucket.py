

class Bucket:

    def __init__(self, minio_bucket):
        self._minio_bucket = minio_bucket
        self._name = None
        self._creation_date = None
        self._parse(self._minio_bucket)

    @property
    def name(self):
        return self._name

    @property
    def creation_date(self):
        return self._creation_date

    def _parse(self, buck):
        self._name = buck.name
        self._creation_date = buck.creation_date



