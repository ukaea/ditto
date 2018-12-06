# pylint: disable=W0212
class S3ObjectInformation:
    def __init__(self):
        self._object_name = None
        self._bucket_name = None
        self._size = None
        self._etag = None
        self._last_modified = None

    @property
    def object_name(self):
        return self._object_name

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def size(self):
        return self._size

    @property
    def etag(self):
        return self._etag

    @property
    def last_modified(self):
        return self._last_modified

    def to_dict(self):
        return {"object_name": self.object_name,
                "bucket_name": self.bucket_name,
                "size": self.size,
                "etag": self.etag,
                "last modified": self.last_modified}

    @staticmethod
    def create(object_name, bucket_name, size, etag, last_modified):
        output = S3ObjectInformation()
        output._object_name = object_name
        output._bucket_name = bucket_name
        output._size = size
        output._etag = etag
        output._last_modified = last_modified.timestamp()
        return output
