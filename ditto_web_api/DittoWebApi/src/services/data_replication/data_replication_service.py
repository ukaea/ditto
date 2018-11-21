from minio.error import InvalidBucketError
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.src.utils.bucket_helper import is_valid_bucket
from DittoWebApi.src.models.bucket_warning import BucketWarning
from DittoWebApi.src.models.file_storage_summary import FilesStorageSummary
from DittoWebApi.src.utils import messages


class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, storage_difference_processor, logger):
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._storage_difference_processor = storage_difference_processor
        self._logger = logger

    def _check_bucket_warnings(self, bucket_name):
        bucket_warning = BucketWarning()
        if not is_valid_bucket(bucket_name):
            bucket_warning.message = messages.bucket_breaks_s3_convention(bucket_name)
        elif not self._external_data_service.does_bucket_match_standard(bucket_name):
            bucket_warning.message = messages.bucket_breaks_config(bucket_name)
        elif not self._external_data_service.does_bucket_exist(bucket_name):
            bucket_warning.message = messages.bucket_not_exists(bucket_name)
        if bucket_warning.message != "":
            bucket_warning.is_warning_found = True
            self._logger.warning(bucket_warning.message)
        return bucket_warning

    def retrieve_object_dicts(self, bucket_name, dir_path):
        bucket_warnings = self._check_bucket_warnings(bucket_name)
        if bucket_warnings.is_warning_found is True:
            return {"message": bucket_warnings.message, "objects": []}
        self._logger.info("Going to find objects from directory '{}' in bucket '{}'".format(dir_path, bucket_name))
        objects = self._external_data_service.get_objects(bucket_name, dir_path)
        object_dicts = [obj.to_dict() for obj in objects]
        return {"message": "objects returned successfully", "objects": object_dicts}

    def copy_dir(self, bucket_name, dir_path):
        warnings = self._check_bucket_warnings(bucket_name)

        if warnings.is_warning_found is True:
            return return_transfer_summary(message=warnings.message)
        files_summary = FilesStorageSummary(self._internal_data_service.find_files(dir_path))

        if not files_summary.files_in_directory:
            self._logger.warning(messages.no_files_found(dir_path))
            return return_transfer_summary(message=messages.no_files_found(dir_path))

        if self._external_data_service.does_dir_exist(bucket_name, dir_path):
            self._logger.warning(messages.directory_exists(dir_path, len(files_summary.files_in_directory)))
            return return_transfer_summary(message=messages.directory_exists(dir_path,
                                                                             len(files_summary.files_in_directory)),
                                           files_skipped=len(files_summary.files_to_be_skipped()))
        return return_transfer_summary(**self._external_data_service.perform_transfer(bucket_name, files_summary))

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
        bucket_warnings = self._check_bucket_warnings(bucket_name)
        if bucket_warnings.is_warning_found:
            return return_delete_file_helper(message=bucket_warnings.message,
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
        bucket_warnings = self._check_bucket_warnings(bucket_name)

        if bucket_warnings.is_warning_found:
            return return_transfer_summary(message=bucket_warnings.message)
        directory = dir_path if dir_path else "root"
        files_summary = FilesStorageSummary(self._internal_data_service.find_files(dir_path))

        if not files_summary.files_in_directory:
            self._logger.warning(messages.no_files_found(directory))
            return return_transfer_summary(message=messages.no_files_found(directory))
        objects_already_in_bucket = self._external_data_service.get_objects(bucket_name, dir_path)
        completed_files_summary = self._storage_difference_processor.return_difference_comparison(
            objects_already_in_bucket, files_summary
        )
        if not completed_files_summary.new_files:
            self._logger.warning(messages.no_new_files(directory))
            return return_transfer_summary(message=messages.no_new_files(directory),
                                           files_skipped=len(completed_files_summary.files_to_be_skipped()))
        return return_transfer_summary(**self._external_data_service.perform_transfer(bucket_name,
                                                                                      completed_files_summary))

    def copy_new_and_update(self, bucket_name, dir_path):
        bucket_warnings = self._check_bucket_warnings(bucket_name)
        if bucket_warnings.is_warning_found:
            return return_transfer_summary(message=bucket_warnings.message)
        directory = dir_path if dir_path else "root"
        objects_already_in_bucket = self._external_data_service.get_objects(bucket_name, dir_path)
        files_summary = FilesStorageSummary(self._internal_data_service.find_files(dir_path))

        if not files_summary.files_in_directory:
            self._logger.warning(messages.no_files_found(directory))
            return return_transfer_summary(message=messages.no_files_found(directory))
        completed_files_summary = self._storage_difference_processor.return_difference_comparison(
            objects_already_in_bucket, files_summary, check_for_updates=True
        )
        if not completed_files_summary.new_files and not completed_files_summary.updated_files:
            self._logger.warning(messages.no_new_or_updates(directory))
            return return_transfer_summary(message=messages.no_new_or_updates(directory),
                                           files_skipped=len(completed_files_summary.files_to_be_skipped()))
        return return_transfer_summary(**self._external_data_service.perform_transfer(bucket_name,
                                                                                      completed_files_summary))
