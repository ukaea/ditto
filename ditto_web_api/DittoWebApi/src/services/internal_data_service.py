import os
from DittoWebApi.src.models.file import File


class InternalDataService:
    def __init__(self, configuration):
        self.root_dir = configuration.root_dir

    def find_files(self):
        files = []
        for path, subdirs, files in os.walk(self.root_dir):
            for name in files:
                files.append(os.path.join(path, name))
        return files

    @staticmethod
    def process_file(file):
        return File(file)



