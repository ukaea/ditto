import os


class File:

    def __init__(self, file, root_dir):
        self._file = file
        self._name = None
        self._length = None
        self._root_dir = root_dir
        self._parse(self._file)

    @property
    def data(self):
        with open(self._name, 'rb') as file_data:
            return file_data

    @property
    def abs_path(self):
        return self._abs_path

    @property
    def file_name(self):
        return self._file_name

    @property
    def rel_path(self):
        return self._rel_path

    @property
    def length(self):
        return self._length

    def _parse(self, f):
        self._name = f
        self._abs_path = os.path.abspath(f)
        self._rel_path = os.path.relpath(self._abs_path, self._root_dir)
        self._file_name = os.path.split(self._abs_path)[1]
        file_stats = os.stat(f)
        self._length = file_stats.st_size
