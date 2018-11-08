import os


class FileSystemHelpers:
    def join_paths(self, directory, file_name):
        return os.path.join(directory, file_name)

    def find_all_files_in_folder(self, directory):
        list_of_files = []
        for path, subdirs, files in os.walk(directory):
            for name in files:
                list_of_files.append(self.join_paths(path, name))
        return list_of_files
