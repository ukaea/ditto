from DittoWebApi.src.models.file_information import FileInformation
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary


class InternalDataService:
    def __init__(self, archiver, configuration, file_system_helper, logger):
        self._archiver = archiver
        self._archive_file_name = configuration.archive_file_name
        self._file_system_helper = file_system_helper
        self._logger = logger

    def find_files(self, root_dir, dir_path):
        dir_to_search = self._file_system_helper.join_paths(root_dir, dir_path) \
            if dir_path \
            else root_dir
        self._logger.debug(f"Finding files in directory {dir_to_search}")
        all_files = self._file_system_helper.find_all_files_in_folder(dir_to_search)
        list_of_files = list(filter(lambda name: not name.endswith(self._archive_file_name), all_files))
        self._logger.debug(f"Found {len(list_of_files)} files, converting to file information objects")
        file_information_list = [
            self._build_file_information(root_dir, full_file_name) for full_file_name in list_of_files
        ]
        self._logger.info(f"{len(file_information_list)} files found in {dir_path}")
        return file_information_list

    def _build_file_information(self, root_dir, file_path):
        abs_path_to_file = self._file_system_helper.absolute_file_path(file_path)
        rel_path_to_file = self._file_system_helper.relative_file_path(file_path, root_dir)
        file_name = self._file_system_helper.file_name(abs_path_to_file)
        return FileInformation(abs_path_to_file, rel_path_to_file, file_name)

    def archive_file_transfer(self, file_summary, root_dir):
        sub_directory_file_summaries = self._split_file_summary_by_sub_dir(file_summary)

        for sub_dir in sub_directory_file_summaries:
            full_sub_dir_path = \
                self._file_system_helper.join_paths(root_dir, sub_dir) if sub_dir else root_dir
            self._logger.debug(f"Writing archive file in {full_sub_dir_path}")
            archive_file_path = self._file_system_helper.join_paths(full_sub_dir_path, self._archive_file_name)
            sub_dir_file_summary = sub_directory_file_summaries[sub_dir]

            if self._file_system_helper.does_path_exist(archive_file_path):
                self._archiver.update_archive(archive_file_path, sub_dir_file_summary)
            else:
                self._archiver.write_archive(archive_file_path, sub_dir_file_summary)

    def _split_file_summary_by_sub_dir(self, file_summary):
        dict_of_sub_dir_summaries = {}

        self._add_file_to_sub_dir_file_summary(
            file_summary.new_files, dict_of_sub_dir_summaries, lambda path: dict_of_sub_dir_summaries[path].new_files)

        self._add_file_to_sub_dir_file_summary(
            file_summary.updated_files,
            dict_of_sub_dir_summaries,
            lambda path: dict_of_sub_dir_summaries[path].updated_files)

        return dict_of_sub_dir_summaries

    def _add_file_to_sub_dir_file_summary(self, files, dict_of_sub_dir_summaries, summary_selector):
        for file in files:
            directory_rel_path = self._file_system_helper.file_directory(file.rel_path)
            if directory_rel_path not in dict_of_sub_dir_summaries:
                dict_of_sub_dir_summaries[directory_rel_path] = FilesStorageSummary(None)
            summary_selector(directory_rel_path).append(file)
