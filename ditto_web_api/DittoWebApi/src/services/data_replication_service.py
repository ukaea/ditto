from DittoWebApi.src.utils.return_helper import return_dict


class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, logger):
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._logger = logger

    def retrieve_object_dicts(self, dir_path):
        self._logger.info("Going to find objects")
        buckets = self._external_data_service.get_buckets()
        objects = self._external_data_service.get_objects(buckets, dir_path)
        object_dicts = [obj.to_dict() for obj in objects]
        self._logger.info("Found {} objects in {} buckets".format(len(objects), len(buckets)))
        return object_dicts

    def copy_dir(self, dir_path):
        self._logger.debug("Copying for {}".format(dir_path))
        self._logger.info("Finding files in local directory")
        files_to_copy = self._internal_data_service.find_files(dir_path)
        if not files_to_copy:
            message = "No files found in directory or directory does not exist ({})".format(dir_path)
            self._logger.warning(message)
            return return_dict(message=message)
        # route if files have been found
        buckets = self._external_data_service.get_buckets()
        target_bucket = buckets[0]
        if self._external_data_service.does_dir_exist(dir_path, target_bucket.name):
            skipped_files = len(files_to_copy)
            message = "Directory already exists, {} files skipped".format(skipped_files)
            self._logger.warning(message)
            return return_dict(files_skipped=skipped_files, message=message)
        # route if directory doesn't already exist
        self._logger.info("About to copy {} files".format(len(files_to_copy)))
        data_transferred = 0
        for processed_file in files_to_copy:
            data_transferred += self._external_data_service.upload_file(processed_file, target_bucket)
        message = "Copied across {} files totaling {} bytes".format(len(files_to_copy), data_transferred)
        return return_dict(files_transferred=len(files_to_copy), data_transferred=data_transferred, message=message)

    def create_bucket(self, bucket_name):
        if not bucket_name:
            message = "No bucket name provided"
            return message
        if not self._external_data_service.valid_bucket(bucket_name):
            message = "Bucket name breaks naming standard"
            return message
        if self._external_data_service.does_bucket_exist(bucket_name):
            message = "Bucket already exists"
            return message
        self._external_data_service.create_bucket(bucket_name)
        return "Bucket created!"
