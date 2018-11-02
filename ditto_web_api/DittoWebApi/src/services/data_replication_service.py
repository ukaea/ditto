
class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, logger):
        self._external_data_service = external_data_service
        self._internal_data_service = internal_data_service
        self._logger = logger

    def retrieve_objects(self):
        self._logger.info("Going to find objects")
        objects = self._external_data_service.get_objects()
        self._logger.info("Found {} objects".format(len(objects)))
        return objects
