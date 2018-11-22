from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.src.utils.bucket_helper import is_valid_bucket
from DittoWebApi.src.utils import messages


class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, storage_difference_processor, logger):
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._storage_difference_processor = storage_difference_processor
        self._logger = logger

    def _check_bucket_warning(self, bucket_name):
        self._logger.debug(f"About to check for warning to do with bucket name {bucket_name}")
        bucket_warning = None
        if not is_valid_bucket(bucket_name):
            bucket_warning = messages.bucket_breaks_s3_convention(bucket_name)
        elif not self._external_data_service.does_bucket_match_standard(bucket_name):
            bucket_warning = messages.bucket_breaks_config(bucket_name)
        elif not self._external_data_service.does_bucket_exist(bucket_name):
            bucket_warning = messages.bucket_not_exists(bucket_name)
        if bucket_warning is not None:
            self._logger.warning(bucket_warning)
            return bucket_warning
        self._logger.debug("No warnings found")
        return bucket_warning

    def retrieve_object_dicts(self, bucket_name, dir_path):
        bucket_warning = self._check_bucket_warning(bucket_name)
        if bucket_warning is not None:
            return {"message": bucket_warning, "objects": []}
        objects = self._external_data_service.get_objects(bucket_name, dir_path)
        object_dicts = [obj.to_dict() for obj in objects]
        return {"message": "objects returned successfully", "objects": object_dicts}

    def copy_dir(self, bucket_name, dir_path):
        bucket_warning = self._check_bucket_warning(bucket_name)
        if bucket_warning is not None:
            return return_transfer_summary(message=bucket_warning)
        files_in_directory = self._internal_data_service.find_files(dir_path)

        if not files_in_directory:
            warning = messages.no_files_found(dir_path)
            self._logger.warning(warning)
            return return_transfer_summary(message=warning)

        if self._external_data_service.does_dir_exist(bucket_name, dir_path):
            warning = messages.directory_exists(dir_path, len(files_in_directory))
            self._logger.warning(warning)
            return return_transfer_summary(message=warning, files_skipped=len(files_in_directory))

        file_summary = self._storage_difference_processor.return_difference_comparison([], files_in_directory)
        transfer_summary = self._external_data_service.perform_transfer(bucket_name, file_summary)
        return return_transfer_summary(**transfer_summary)

    def create_bucket(self, bucket_name):
        if not bucket_name:
            warning = messages.no_bucket_name()
            self._logger.warning(warning)
            return return_bucket_message(warning)

        if not self._external_data_service.does_bucket_match_standard(bucket_name):
            message = messages.bucket_breaks_config(bucket_name)
            self._logger.info(message)
            return return_bucket_message(message, bucket_name)

        if self._external_data_service.does_bucket_exist(bucket_name):
            warning = messages.bucket_already_exists(bucket_name)
            self._logger.warning(warning)
            return return_bucket_message(warning, bucket_name)

        if is_valid_bucket(bucket_name) is False:
            return return_bucket_message(messages.bucket_breaks_s3_convention(bucket_name), bucket_name)
        self._external_data_service.create_bucket(bucket_name)
        return return_bucket_message(messages.bucket_created(bucket_name), bucket_name)

    def try_delete_file(self, bucket_name, file_name):
        bucket_warning = self._check_bucket_warning(bucket_name)
        if bucket_warning is not None:
            return return_delete_file_helper(message=bucket_warning,
                                             file_name=file_name,
                                             bucket_name=bucket_name)

        if not self._external_data_service.does_object_exist(bucket_name, file_name):
            warning = messages.file_existence_warning(file_name, bucket_name)
            self._logger.warning(warning)
            return return_delete_file_helper(message=warning,
                                             file_name=file_name,
                                             bucket_name=bucket_name)
        self._external_data_service.delete_file(bucket_name, file_name)
        return return_delete_file_helper(message=messages.file_deleted(file_name, bucket_name),
                                         file_name=file_name,
                                         bucket_name=bucket_name)

    def copy_new(self, bucket_name, dir_path):
        bucket_warning = self._check_bucket_warning(bucket_name)
        if bucket_warning is not None:
            return return_transfer_summary(message=bucket_warning)
        directory = dir_path if dir_path else "root"
        files_in_directory = self._internal_data_service.find_files(dir_path)

        if not files_in_directory:
            warning = messages.no_files_found(directory)
            self._logger.warning(warning)
            return return_transfer_summary(message=warning)

        objects_already_in_bucket = self._external_data_service.get_objects(bucket_name, dir_path)
        if not objects_already_in_bucket:
            self._logger.debug(f"No files found in S3 bucket {bucket_name}, all files are new. "
                               f"About to perform transfer for all files in {directory}")

        files_summary = self._storage_difference_processor.return_difference_comparison(
            objects_already_in_bucket, files_in_directory
        )
        if not files_summary.new_files:
            message = messages.no_new_files(directory)
            self._logger.info(message)
            return return_transfer_summary(message=message,
                                           files_skipped=len(files_in_directory))
        transfer_summary = self._external_data_service.perform_transfer(bucket_name, files_summary)
        return return_transfer_summary(**transfer_summary)

    def copy_new_and_update(self, bucket_name, dir_path):
        bucket_warning = self._check_bucket_warning(bucket_name)
        if bucket_warning is not None:
            return return_transfer_summary(message=bucket_warning)

        directory = dir_path if dir_path else "root"
        files_in_directory = self._internal_data_service.find_files(dir_path)

        if not files_in_directory:
            warning = messages.no_files_found(directory)
            self._logger.warning(warning)
            return return_transfer_summary(message=warning)

        objects_already_in_bucket = self._external_data_service.get_objects(bucket_name, dir_path)

        if not objects_already_in_bucket:
            self._logger.debug(f"No files found in S3 bucket {bucket_name}, all files are new. "
                               f"About to perform transfer for all files in {directory}")

        files_summary = self._storage_difference_processor.return_difference_comparison(
            objects_already_in_bucket, files_in_directory, check_for_updates=True
        )

        if not files_summary.new_files and not files_summary.updated_files:
            message = messages.no_new_or_updates(directory)
            self._logger.info(message)
            return return_transfer_summary(message=message,
                                           files_skipped=len(files_summary.files_to_be_skipped))
        transfer_summary = self._external_data_service.perform_transfer(bucket_name, files_summary)
        return return_transfer_summary(**transfer_summary)
