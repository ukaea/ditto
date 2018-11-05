import os


class File:

    def __init__(self, file):
        self._file = file
        self._name = None
        self._length = None
        self._parse(self._file)

    @property
    def data(self):
        with open(self.name, 'rb') as file_data:
            return file_data

    @property
    def name(self):
        return self._name

    @property
    def length(self):
        return self._length

    def _parse(self, f):
        self._name = f
        file_stats = os.stat(f)
        self._length = file_stats.st_size
