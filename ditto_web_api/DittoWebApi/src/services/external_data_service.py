from minio import Minio


class ExternalDataService:
    def __init__(self, configuration):
        self.s3_client = Minio(configuration.s3_url,
                               configuration.s3_access_key,
                               configuration.s3_secret_key,
                               configuration.s3_use_secure)
