from DittoWebApi.src.models.file_information import FileInformation


class InternalDataService:
    def __init__(self, archiver, configuration, file_system_helper, logger):
        self._root_dir = configuration.root_dir
        self._file_system_helper = file_system_helper
        self._archiver = archiver
        self._logger = logger
        self._archive_file_name = configuration.archive_file_name

    def find_files(self, dir_path):
        dir_to_search = self._file_system_helper.join_paths(self._root_dir, dir_path) \
            if dir_path \
            else self._root_dir
        self._logger.debug(f"Finding files in directory {dir_to_search}")
        all_files = self._file_system_helper.find_all_files_in_folder(dir_to_search)
        list_of_files = list(filter(lambda name: not name.endswith(self._archive_file_name), all_files))
        self._logger.debug(f"Found {len(list_of_files)} files, converting to file information objects")
        file_information_list = [self.build_file_information(full_file_name) for full_file_name in list_of_files]
        self._logger.info(f"{len(file_information_list)} files found in {dir_path}")
        return file_information_list

    def build_file_information(self, file_path):
        abs_path_to_file = self._file_system_helper.absolute_file_path(file_path)
        rel_path_to_file = self._file_system_helper.relative_file_path(file_path, self._root_dir)
        file_name = self._file_system_helper.file_name(abs_path_to_file)
        return FileInformation(abs_path_to_file, rel_path_to_file, file_name)

    def archive_file_transfer(self, dir_path, file_summary):
        full_dir_path = self._file_system_helper.join_paths(self._root_dir, dir_path) if dir_path else self._root_dir
        file_path = self._file_system_helper.join_paths(full_dir_path, self._archive_file_name)
        if self._file_system_helper.does_file_exist(file_path):
            self._archiver.update_archive(file_path, file_summary)
        else:
            self._archiver.write_archive(file_path, file_summary)

    def archive_file_deletion(self, file_rel_path):
        pass
    #    full_path = self._file_system_helper.join_paths(self._root_dir, file_rel_path)

