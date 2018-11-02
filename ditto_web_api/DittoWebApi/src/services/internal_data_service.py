import os
from DittoWebApi.src.models.file import File


class InternalDataService:
    def __init__(self, configuration):
        self.root_dir = configuration.root_dir

    def find_files(self):
        files = []
        for path, subdirs, files in os.walk(self.root_dir):
            for name in files:
                full_file_name = os.path.join(path, name)
                files.append(File(full_file_name))
        return files




