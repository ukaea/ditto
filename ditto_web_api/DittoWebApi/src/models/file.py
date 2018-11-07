import os


class File:

    def __init__(self, file_path, root_dir):
        self._file = file_path
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

    def _parse(self, path_to_file):
        self._name = path_to_file
        self._abs_path = os.path.abspath(path_to_file)
        if os.path.relpath(self._abs_path, self._root_dir)[0:2] == '..':
            raise NameError("Root directory not in file path")
        self._rel_path = os.path.relpath(self._abs_path, self._root_dir)
        self._file_name = os.path.basename(self._abs_path)
