# pylint: disable=R0201
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.utils.file_system.path_helpers import to_posix
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary


class StorageDifferenceProcessor:
    def __init__(self, logger):
        self._file_system_helper = FileSystemHelper()
        self._logger = logger

    def return_difference_comparison(self, objects_in_bucket, files_in_directory, check_for_updates=False):
        self._logger.debug("Comparing objects in directory with those already in bucket")
        file_summary = FilesStorageSummary(files_in_directory)
        dict_of_files = self.file_information_to_dict(objects_in_bucket, files_in_directory)
        file_summary.new_files = [file_information for
                                  file_information in
                                  files_in_directory if
                                  dict_of_files[to_posix(file_information.rel_path)] is None]
        self._logger.debug(f"{len(file_summary.new_files)} files are new")
        if check_for_updates is False:
            return file_summary
        file_summary.updated_files = [file_information for
                                      file_information in
                                      file_summary.files_in_directory if
                                      dict_of_files[to_posix(file_information.rel_path)] is not None
                                      and
                                      self.has_file_changed(
                                          dict_of_files[to_posix(file_information.rel_path)],
                                          file_information)]
        self._logger.debug(f"{len(file_summary.updated_files)} files need updating")
        return file_summary

    @staticmethod
    def are_the_same_file(s3_object, file_information):
        s3_object_name = s3_object.object_name
        return to_posix(file_information.rel_path) == to_posix(s3_object_name)

    def has_file_changed(self, s3_object, file_information):
        return s3_object.last_modified < self._file_system_helper.last_modified(file_information.abs_path)

    @staticmethod
    def file_information_to_dict(objects_in_bucket, files_in_directory):
        file_dict = {to_posix(file.rel_path): None for file in files_in_directory}
        for s3_object in objects_in_bucket:
            if to_posix(s3_object.object_name) in file_dict:
                file_dict[to_posix(s3_object.object_name)] = s3_object
        return file_dict
