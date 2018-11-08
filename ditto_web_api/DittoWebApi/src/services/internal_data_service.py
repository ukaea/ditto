from DittoWebApi.src.models.file import File


class InternalDataService:
    def __init__(self, configuration, file_system_helper):
        self._root_dir = configuration.root_dir
        self._file_system_helper = file_system_helper

    def find_files(self, dir_path):
        dir_to_search = self._file_system_helper.join_paths(self._root_dir, dir_path) \
            if dir_path \
            else self._root_dir
        list_of_files = self._file_system_helper.find_all_files_in_folder(dir_to_search)
        file_information_list = [File(full_file_name, self._root_dir) for full_file_name in list_of_files]
        return file_information_list
