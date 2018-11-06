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

    def get_internal_files(self, dir_path):
        self._logger.info("Finding files in local directory")
        return self._internal_data_service.find_files(dir_path)

    def copy_dir(self, dir_path):
        self._logger.debug("Copying for {}".format(dir_path))
        files_to_copy = self.get_internal_files(dir_path)
        if len(files_to_copy) == 0:
            message = "No files found in directory or directory does not exist ({})".format(dir_path)
            self._logger.warning(message)
            return message
        # route if files have been found
        buckets = self._external_data_service.get_buckets()
        target_bucket = buckets[0]
        if self._external_data_service.does_dir_exists(dir_path, target_bucket.name):
            message = "Directory already exists"
            self._logger.warning(message)
            return message
        # route if directory doesn't already exist
        self._logger.info("About to copy {} files".format(len(files_to_copy)))
        data_transferred = 0
        for processed_file in files_to_copy:
            data_transferred += self._external_data_service.upload(processed_file, target_bucket)
        message = "Copied across {} files totaling {} bytes".format(len(files_to_copy), data_transferred)
        return message
