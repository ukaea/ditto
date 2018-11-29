from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary


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

    def archive_file_transfer(self, file_summary):
        sub_directory_file_summaries = self.split_file_summary_by_sub_dir(file_summary)
        for sub_dir in sub_directory_file_summaries:
            full_sub_dir_path = \
                self._file_system_helper.join_paths(self._root_dir, sub_dir) if sub_dir else self._root_dir
            archive_file_path = self._file_system_helper.join_paths(full_sub_dir_path, self._archive_file_name)

            if self._file_system_helper.does_file_exist(archive_file_path):
                self._archiver.update_archive(archive_file_path, file_summary)
            else:
                self._archiver.write_archive(archive_file_path, file_summary)

    def split_file_summary_by_sub_dir(self, file_summary):
        dict_of_sub_dir_summaries = {}

        for file in file_summary.new_files:
            directory = self._file_system_helper.file_directory(file.rel_path)
            directory_rel_path = self._file_system_helper.relative_file_path(directory, self._root_dir)
            if directory_rel_path in dict_of_sub_dir_summaries:
                dict_of_sub_dir_summaries[directory_rel_path].new_files.append(file)
            else:
                dict_of_sub_dir_summaries[directory_rel_path] = FilesStorageSummary(None)
                dict_of_sub_dir_summaries[directory_rel_path].new_files.append(file)

        for file in file_summary.updated_files:
            directory = self._file_system_helper.file_directory(file.rel_path)
            directory_rel_path = self._file_system_helper.relative_file_path(directory, self._root_dir)
            if directory_rel_path in dict_of_sub_dir_summaries:
                dict_of_sub_dir_summaries[directory_rel_path].updated_files.append(file)
            else:
                dict_of_sub_dir_summaries[directory_rel_path] = FilesStorageSummary(None)
                dict_of_sub_dir_summaries[directory_rel_path].updated_files.append(file)
        return dict_of_sub_dir_summaries




