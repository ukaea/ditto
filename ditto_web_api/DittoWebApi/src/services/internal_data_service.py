import os
from DittoWebApi.src.models.file import File


class InternalDataService:
    def __init__(self, configuration):
        self._root_dir = configuration.root_dir

    def find_files(self, dir_path=None):
        list_of_files = []
        if dir_path:
            dir_to_search = dir_path
        else:
            dir_to_search = self._root_dir
        for path, subdirs, files in os.walk(dir_to_search):
            for name in files:
                full_file_name = os.path.join(path, name)
                list_of_files.append(File(full_file_name, self._root_dir))
        return list_of_files
