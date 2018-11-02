class File:

    def __init__(self, file):
        self._file = file
        self._data = None
        self._name = None
        self._length = None
        self._parse(self._file)

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def length(self):
        return self._length

    def _parse(self, f):
        with open(f, 'rb') as file_data:
            self._data = file_data
        self._name = f
        file_stats = os.stat(f)
        self._length = file_stats.st_size
