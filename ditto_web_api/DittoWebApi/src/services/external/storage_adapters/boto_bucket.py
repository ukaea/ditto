from DittoWebApi.src.services.external.storage_adapters.boto_key import BotoKey


class BotoBucket:
    def __init__(self, bucket):
        self._bucket = bucket

    @property
    def creation_date(self):
        return self._bucket.creation_date

    def get_key(self, *args, **kwargs):
        key = self._bucket.get_key(*args, **kwargs)
        wrapped_key = BotoKey(key)
        return wrapped_key

    def list(self, *args, **kwargs):
        return self._bucket.list(*args, **kwargs)

    @property
    def name(self):
        return self._bucket.name

    def new_key(self, *args, **kwargs):
        return self._bucket.new_key(*args, **kwargs)
