class FileInformation:

    def __init__(self, absolute_path, relative_path, file_name):
        self._abs_path = absolute_path
        self._rel_path = relative_path
        self._file_name = file_name

    @property
    def abs_path(self):
        return self._abs_path

    @property
    def rel_path(self):
        return self._rel_path

    @property
    def file_name(self):
        return self._file_name
