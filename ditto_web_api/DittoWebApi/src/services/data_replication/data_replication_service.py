from DittoWebApi.src.services.data_replication.bucket_validator import BucketValidator
from DittoWebApi.src.services.data_replication.storage_difference_processor import StorageDifferenceProcessor
from DittoWebApi.src.utils import messages
from DittoWebApi.src.utils.bucket_helper import is_valid_bucket
from DittoWebApi.src.utils.file_system.files_system_helpers import FileSystemHelper
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.src.utils.return_helper import return_delete_file_helper
from DittoWebApi.src.utils.return_helper import return_transfer_summary
from DittoWebApi.src.utils.return_helper import return_list_present_helper
from DittoWebApi.src.utils.return_status import StatusCodes


class DataReplicationService:
    def __init__(self,
                 bucket_settings_service,
                 bucket_validator,
                 external_data_service,
                 internal_data_service,
                 logger,
                 storage_difference_processor):
        self._bucket_settings_service = bucket_settings_service
        self._bucket_validator = bucket_validator
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._storage_difference_processor = storage_difference_processor
        self._logger = logger

    def retrieve_object_dicts(self, bucket_name, dir_path):
        self._logger.debug("Called list-present handler")
        bucket_warning = self._bucket_validator.check_bucket(bucket_name)
        if bucket_warning is not None:
            return return_list_present_helper(message=bucket_warning.message, objects=[], status=bucket_warning.status)
        objects = self._external_data_service.get_objects(bucket_name, dir_path)
        object_dicts = [obj.to_dict() for obj in objects]
        if not object_dicts:
            return return_list_present_helper(
                message=f"no objects in directory {dir_path} in bucket {bucket_name}",
                objects=[],
                status=StatusCodes.Okay)
        return return_list_present_helper(message="objects returned successfully",
                                          objects=object_dicts,
                                          status=StatusCodes.Okay)

    def copy_dir(self, bucket_name, dir_path):
        self._logger.debug("Called copy-dir handler")

        bucket_warning = self._bucket_validator.check_bucket(bucket_name)
        if bucket_warning is not None:
            return return_transfer_summary(message=bucket_warning.message, status=bucket_warning.status)

        data_root_dir = self._bucket_settings_service.bucket_data_root_directory(bucket_name)
        files_in_directory = self._internal_data_service.find_files(data_root_dir, dir_path)

        directory = dir_path if dir_path else "root"

        if not files_in_directory:
            warning = messages.no_files_found(directory)
            self._logger.warning(warning)
            return return_transfer_summary(message=warning, status=StatusCodes.Not_found)

        if self._external_data_service.does_dir_exist(bucket_name, dir_path):
            warning = messages.directory_exists(directory, len(files_in_directory))
            self._logger.warning(warning)
            return return_transfer_summary(
                message=warning, files_skipped=len(files_in_directory))

        file_summary = self._storage_difference_processor.return_difference_comparison([], files_in_directory)
        transfer_summary = self._external_data_service.perform_transfer(bucket_name, file_summary)
        archive_root_dir = self._bucket_settings_service.bucket_archive_root_directory(bucket_name)
        self._internal_data_service.archive_file_transfer(bucket_name, file_summary, archive_root_dir)
        return return_transfer_summary(**transfer_summary)

    def create_bucket(self, bucket_name, groups, archive_root_dir, data_root_dir):
        self._logger.debug("Called create-bucket handler")
        if not bucket_name:
            warning = messages.no_bucket_name()
            self._logger.warning(warning)
            return return_bucket_message(warning, status=StatusCodes.Bad_request)

        if not self._external_data_service.does_bucket_match_standard(bucket_name):
            message = messages.bucket_breaks_config(bucket_name)
            self._logger.info(message)
            return return_bucket_message(message, bucket_name, status=StatusCodes.Bad_request)

        if self._external_data_service.does_bucket_exist(bucket_name) or \
                self._bucket_settings_service.is_bucket_recognised(bucket_name):
            warning = messages.bucket_already_exists(bucket_name)
            self._logger.warning(warning)
            return return_bucket_message(warning, bucket_name, status=StatusCodes.Bad_request)

        if is_valid_bucket(bucket_name) is False:
            return return_bucket_message(
                messages.bucket_breaks_s3_convention(bucket_name), bucket_name, status=StatusCodes.Bad_request)
        self._external_data_service.create_bucket(bucket_name)
        self._bucket_settings_service.add_bucket(bucket_name, groups, archive_root_dir, data_root_dir)
        return return_bucket_message(messages.bucket_created(bucket_name), bucket_name)

    def try_delete_file(self, bucket_name, file_rel_path):
        self._logger.debug("Called delete-file handler")
        bucket_warning = self._bucket_validator.check_bucket(bucket_name)
        if bucket_warning is not None:
            return return_delete_file_helper(message=bucket_warning.message,
                                             file_rel_path=file_rel_path,
                                             bucket_name=bucket_name,
                                             status=bucket_warning.status)

        if not self._external_data_service.does_object_exist(bucket_name, file_rel_path):
            warning = messages.file_existence_warning(file_rel_path, bucket_name)
            self._logger.warning(warning)
            return return_delete_file_helper(message=warning,
                                             file_rel_path=file_rel_path,
                                             bucket_name=bucket_name,
                                             status=StatusCodes.Not_found)
        self._external_data_service.delete_file(bucket_name, file_rel_path)
        msg = messages.file_deleted(file_rel_path, bucket_name)
        action_summary = return_delete_file_helper(message=msg, file_rel_path=file_rel_path, bucket_name=bucket_name)
        return action_summary

    def copy_new(self, bucket_name, dir_path):
        self._logger.debug("Called copy new handler")
        bucket_warning = self._bucket_validator.check_bucket(bucket_name)
        if bucket_warning is not None:
            return return_transfer_summary(message=bucket_warning.message, status=bucket_warning.status)
        directory = dir_path if dir_path else "root"
        data_root_dir = self._bucket_settings_service.bucket_data_root_directory(bucket_name)
        files_in_directory = self._internal_data_service.find_files(data_root_dir, dir_path)

        if not files_in_directory:
            warning = messages.no_files_found(directory)
            self._logger.warning(warning)
            return return_transfer_summary(message=warning, status=StatusCodes.Not_found)

        objects_already_in_bucket = self._external_data_service.get_objects(bucket_name, dir_path)
        files_summary = self._storage_difference_processor.return_difference_comparison(
            objects_already_in_bucket, files_in_directory
        )
        if not files_summary.new_files:
            message = messages.no_new_files(directory)
            self._logger.info(message)
            return return_transfer_summary(message=message,
                                           files_skipped=len(files_in_directory))
        transfer_summary = self._external_data_service.perform_transfer(bucket_name, files_summary)
        archive_root_dir = self._bucket_settings_service.bucket_archive_root_directory(bucket_name)
        self._internal_data_service.archive_file_transfer(bucket_name, files_summary, archive_root_dir)
        return return_transfer_summary(**transfer_summary)

    def copy_new_and_update(self, bucket_name, dir_path):
        self._logger.debug("Called copy-update handler")
        bucket_warning = self._bucket_validator.check_bucket(bucket_name)
        if bucket_warning is not None:
            return return_transfer_summary(message=bucket_warning.message, status=bucket_warning.status)

        directory = dir_path if dir_path else "root"
        data_root_dir = self._bucket_settings_service.bucket_data_root_directory(bucket_name)
        files_in_directory = self._internal_data_service.find_files(data_root_dir, dir_path)

        if not files_in_directory:
            warning = messages.no_files_found(directory)
            self._logger.warning(warning)
            return return_transfer_summary(message=warning, status=StatusCodes.Not_found)

        objects_already_in_bucket = self._external_data_service.get_objects(bucket_name, dir_path)
        files_summary = self._storage_difference_processor.return_difference_comparison(
            objects_already_in_bucket, files_in_directory, check_for_updates=True)

        if not files_summary.new_files and not files_summary.updated_files:
            message = messages.no_new_or_updates(directory)
            self._logger.info(message)
            return return_transfer_summary(message=message,
                                           files_skipped=len(files_summary.files_to_be_skipped()))
        transfer_summary = self._external_data_service.perform_transfer(bucket_name, files_summary)
        archive_root_dir = self._bucket_settings_service.bucket_archive_root_directory(bucket_name)
        self._internal_data_service.archive_file_transfer(bucket_name, files_summary, archive_root_dir)
        return return_transfer_summary(**transfer_summary)


def build_standard_data_replication_service(bucket_settings_service,
                                            external_data_service,
                                            internal_data_service,
                                            logger):
    bucket_validator = BucketValidator(external_data_service, logger)
    storage_difference_processor = StorageDifferenceProcessor(FileSystemHelper(), logger)
    data_replication_service = DataReplicationService(bucket_settings_service,
                                                      bucket_validator,
                                                      external_data_service,
                                                      internal_data_service,
                                                      logger,
                                                      storage_difference_processor)
    return data_replication_service
