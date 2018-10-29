class DataReplicationService:
    def __init__(self, external_data_service, internal_data_service, logger):
        self.external_data_service = external_data_service
        self.internal_data_service = internal_data_service
        self.logger = logger
