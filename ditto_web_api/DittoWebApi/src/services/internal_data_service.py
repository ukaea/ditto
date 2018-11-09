from DittoWebApi.src.models.fileinformation import FileInformation


class InternalDataService:
    def __init__(self, configuration, file_system_helper, logger):
        self._root_dir = configuration.root_dir
        self._file_system_helper = file_system_helper
        self._logger = logger

    def find_files(self, dir_path):
        dir_to_search = self._file_system_helper.join_paths(self._root_dir, dir_path) \
            if dir_path \
            else self._root_dir
        self._logger.debug("Finding files in directory {}".format(dir_to_search))
        list_of_files = self._file_system_helper.find_all_files_in_folder(dir_to_search)
        self._logger.debug("Found {} files, converting to file information objects".format(len(list_of_files)))
        file_information_list = [self.build_file_information(full_file_name) for full_file_name in list_of_files]
        return file_information_list

    def build_file_information(self, file_path):
        abs_path_to_file = self._file_system_helper.absolute_file_path(file_path)
        rel_path_to_file = self._file_system_helper.relative_file_path(file_path, self._root_dir)
        file_name = self._file_system_helper.file_name(abs_path_to_file)
        return FileInformation(abs_path_to_file, rel_path_to_file, file_name)
