from minio.error import InvalidBucketError
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.src.utils import messages


class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, storage_difference_processor, logger):
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._storage_difference_processor = storage_difference_processor
        self._logger = logger

    def _check_bucket_warning(self, bucket_name):
        message = messages.bucket_existence_warning(bucket_name)
        self._logger.warning(message)
        return message

    def retrieve_object_dicts(self, bucket_name, dir_path):
        if not self._external_data_service.does_bucket_exist(bucket_name):
            return {"message": self._check_bucket_warning(bucket_name)}
        self._logger.info("Going to find objects from directory '{}' in bucket '{}'".format(dir_path, bucket_name))
        objects = self._external_data_service.get_objects(bucket_name, dir_path)
        object_dicts = [obj.to_dict() for obj in objects]
        self._logger.info("Found {} objects in '{}' directory of bucket '{}'".format(len(objects),
                                                                                     dir_path,
                                                                                     bucket_name))
        return object_dicts

    def copy_dir(self, bucket_name, dir_path):
        if not self._external_data_service.does_bucket_exist(bucket_name):
            return return_transfer_summary(message=self._check_bucket_warning(bucket_name))
        self._logger.debug("Copying for {}".format(dir_path))
        self._logger.info("Finding files in local directory")
        files_to_copy = self._internal_data_service.find_files(dir_path)
        if not files_to_copy:
            message = messages.no_files_found(dir_path)
            self._logger.warning(message)
            return return_transfer_summary(message=message)
        # route if files have been found
        if self._external_data_service.does_dir_exist(bucket_name, dir_path):
            skipped_files = len(files_to_copy)
            self._logger.warning(messages.directory_exists(dir_path, skipped_files))
            return return_transfer_summary(files_skipped=skipped_files,
                                           message=messages.directory_exists(dir_path, skipped_files))
        # route if directory doesn't already exist
        self._logger.info("About to copy {} files".format(len(files_to_copy)))
        data_transferred = 0
        for processed_file in files_to_copy:
            data_transferred += self._external_data_service.upload_file(bucket_name, processed_file)
        return return_transfer_summary(files_transferred=len(files_to_copy),
                                       data_transferred=data_transferred,
                                       message=messages.transfer_success())

    def create_bucket(self, bucket_name):
        if not bucket_name:
            self._logger.warning(messages.no_bucket_name())
            return return_bucket_message(messages.no_bucket_name())
        if not self._external_data_service.does_bucket_match_standard(bucket_name):
            self._logger.info(messages.bucket_breaks_config(bucket_name))
            return return_bucket_message(messages.bucket_breaks_config(bucket_name), bucket_name)
        try:
            if self._external_data_service.does_bucket_exist(bucket_name):
                self._logger.warning(messages.bucket_exists(bucket_name))
                return return_bucket_message(messages.bucket_exists(bucket_name), bucket_name)
        except InvalidBucketError:
            self._logger.warning(messages.bucket_breaks_s3_convention(bucket_name))
            return return_bucket_message(messages.bucket_breaks_s3_convention(bucket_name), bucket_name)
        self._external_data_service.create_bucket(bucket_name)
        self._logger.info(messages.bucket_created(bucket_name))
        return return_bucket_message(messages.bucket_created(bucket_name), bucket_name)

    def try_delete_file(self, bucket_name, file_name):
        if not self._external_data_service.does_bucket_exist(bucket_name):
            return return_delete_file_helper(message=self._check_bucket_warning(bucket_name),
                                             file_name=file_name,
                                             bucket_name=bucket_name)
        if not self._external_data_service.does_object_exist(bucket_name, file_name):
            self._logger.warning(messages.file_existence_warning(file_name, bucket_name))
            return return_delete_file_helper(message=messages.file_existence_warning(file_name, bucket_name),
                                             file_name=file_name,
                                             bucket_name=bucket_name)
        self._external_data_service.delete_file(bucket_name, file_name)
        message = messages.file_deleted(file_name, bucket_name)
        return return_delete_file_helper(message=message, file_name=file_name, bucket_name=bucket_name)

    def copy_new(self, bucket_name, dir_path):
        if not self._external_data_service.does_bucket_exist(bucket_name):
            return return_transfer_summary(message=self._check_bucket_warning(bucket_name))
        directory = dir_path if dir_path else "root"
        self._logger.info("Finding files in {}".format(directory))
        files_in_directory = self._internal_data_service.find_files(dir_path)
        if not files_in_directory:
            self._logger.warning(messages.no_files_found(directory))
            return return_transfer_summary(message=messages.no_files_found(directory))
        files_already_in_bucket = self._external_data_service.get_objects(bucket_name, dir_path)
        self._logger.info("Found {} files in {} comparing against files already in bucket {}".format(
            len(files_in_directory), directory, bucket_name))
        files_to_transfer = self._storage_difference_processor.return_new_files(files_already_in_bucket,
                                                                                files_in_directory)
        if not files_to_transfer:
            self._logger.warning(messages.no_new_files(directory))
            return return_transfer_summary(message=messages.no_new_files(directory),
                                           files_skipped=len(files_in_directory))
        self._logger.info("About to transfer {} new files from {} into bucket {}".format(len(files_to_transfer),
                                                                                         directory,
                                                                                         bucket_name))
        data_transferred = 0
        for file in files_to_transfer:
            data_transferred += self._external_data_service.upload_file(bucket_name, file)
        self._logger.info(messages.transfer_summary(len(files_to_transfer), directory, data_transferred))
        return return_transfer_summary(files_transferred=len(files_to_transfer),
                                       files_skipped=(len(files_in_directory)-len(files_to_transfer)),
                                       data_transferred=data_transferred,
                                       message=messages.transfer_success())
