from minio.error import InvalidBucketError
from DittoWebApi.src.utils.return_helper import return_dict
from DittoWebApi.src.utils.return_helper import return_bucket_message
from DittoWebApi.src.utils.return_helper import return_delete_file_helper


class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, logger):
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._logger = logger

    def retrieve_object_dicts(self, bucket_name, dir_path):
        self._logger.info("Going to find objects from directory '{}' in bucket '{}'".format(dir_path, bucket_name))
        objects = self._external_data_service.get_objects([bucket_name], dir_path)
        object_dicts = [obj.to_dict() for obj in objects]
        self._logger.info("Found {} objects in '{}' directory of bucket '{}'".format(len(objects),
                                                                                     dir_path,
                                                                                     bucket_name))
        return object_dicts

    def copy_dir(self, bucket_name, dir_path):
        self._logger.debug("Copying for {}".format(dir_path))
        self._logger.info("Finding files in local directory")
        files_to_copy = self._internal_data_service.find_files(dir_path)
        if not files_to_copy:
            message = "No files found in directory or directory does not exist ({})".format(dir_path)
            self._logger.warning(message)
            return return_dict(message=message)
        # route if files have been found
        if self._external_data_service.does_dir_exist(bucket_name, dir_path):
            skipped_files = len(files_to_copy)
            message = "Directory already exists, {} files skipped".format(skipped_files)
            self._logger.warning(message)
            return return_dict(files_skipped=skipped_files, message=message)
        # route if directory doesn't already exist
        self._logger.info("About to copy {} files".format(len(files_to_copy)))
        data_transferred = 0
        for processed_file in files_to_copy:
            data_transferred += self._external_data_service.upload_file(bucket_name, processed_file)
        message = "Copied across {} files totaling {} bytes".format(len(files_to_copy), data_transferred)
        return return_dict(files_transferred=len(files_to_copy), data_transferred=data_transferred, message=message)

    def create_bucket(self, bucket_name):
        if not bucket_name:
            message = "No bucket name provided"
            self._logger.warning(message)
            return return_bucket_message(message)
        if not self._external_data_service.does_bucket_match_standard(bucket_name):
            message = "Bucket breaks local naming standard ({})".format(bucket_name)
            self._logger.info(message)
            return return_bucket_message(message, bucket_name)
        try:
            if self._external_data_service.does_bucket_exist(bucket_name):
                message = "Bucket already exists ({})".format(bucket_name)
                self._logger.warning(message)
                return return_bucket_message(message, bucket_name)
        except InvalidBucketError:
            message = "Bucket name breaks S3 ({})".format(bucket_name)
            self._logger.warning(message)
            return return_bucket_message(message, bucket_name)
        self._external_data_service.create_bucket(bucket_name)
        message = "Bucket Created ({})".format(bucket_name)
        self._logger.info(message)
        return return_bucket_message(message, bucket_name)

    def try_delete_file(self, bucket_name, file_name):
        if not self._external_data_service.does_object_exist(bucket_name, file_name):
            message = "File {} does not exist in bucket {}".format(file_name, bucket_name)
            self._logger.warning(message)
            return return_delete_file_helper(message, file_name, bucket_name)
        self._external_data_service.delete_file(bucket_name, file_name)
        message = "File {} successfully deleted from bucket {}".format(file_name, bucket_name)
        return return_delete_file_helper(message, file_name, bucket_name)

    def copy_new(self, bucket_name, dir_path):
        pass
