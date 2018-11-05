import os


class File:

    def __init__(self, file, root_dir):
        self._file = file
        self._name = None
        self._root_dir = root_dir
        self._parse(self._file)

    @property
    def abs_path(self):
        return self._abs_path

    @property
    def file_name(self):
        return self._file_name

    @property
    def rel_path(self):
        return self._rel_path

    def _parse(self, f):
        self._name = f
        self._abs_path = os.path.abspath(f)
        self._rel_path = os.path.relpath(self._abs_path, self._root_dir)
        self._file_name = os.path.split(self._abs_path)[1]
