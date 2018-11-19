class BotoKey:
    def __init__(self, key):
        self._key = key

    def delete(self, *args, **kwargs):
        return self._key.delete(*args, **kwargs)

    def set_contents_from_filename(self, *args, **kwargs):
        return self._key.set_contents_from_filename(*args, **kwargs)
