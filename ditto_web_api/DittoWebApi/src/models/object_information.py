class Object:

    def __init__(self, minio_object):
        self._minio_object = minio_object
        self._object_name = None
        self._bucket_name = None
        self._is_dir = None
        self._size = None
        self._etag = None
        self._last_modified = None

        self._parse(self._minio_object)

    @property
    def object_name(self):
        return self._object_name

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def is_dir(self):
        return self._is_dir

    @property
    def size(self):
        return self._size

    @property
    def etag(self):
        return self._etag

    @property
    def last_modified(self):
        return self._last_modified

    def _parse(self, obj):
        self._object_name = obj.object_name
        self._bucket_name = obj.bucket_name
        self._is_dir = obj.is_dir
        self._size = obj.size
        self._etag = obj.etag
        self._last_modified = obj.last_modified.timestamp()

    def to_dict(self):
        return {"object_name": self.object_name,
                "bucket_name": self.bucket_name,
                "is_dir": self.is_dir,
                "size": self.size,
                "etag": self.etag,
                "last modified": self.last_modified}
