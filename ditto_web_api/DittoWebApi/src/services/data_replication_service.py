class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, logger):
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._logger = logger

    def retrieve_object_dicts(self):
        self._logger.info("Going to find objects")
        buckets = self._external_data_service.get_buckets()
        objects = self._external_data_service.get_objects(buckets)
        object_dicts = [obj.to_dict() for obj in objects]
        self._logger.info("Found {} objects in {} buckets".format(len(objects), len(buckets)))
        return object_dicts

    def retrieve_list_of_files(self):
        self._logger.info("Finding files in local directory")
        return self._internal_data_service.find_files()

    def copy_dir(self):
        files_to_copy = self.retrieve_list_of_files()
        for processed_file in files_to_copy:
            self.upload_at_external(processed_file)

    def upload_at_external(self, processed_file):
        buckets = self._external_data_service.get_buckets()
        target_bucket = buckets[0]
        self._external_data_service.upload(processed_file, target_bucket)



