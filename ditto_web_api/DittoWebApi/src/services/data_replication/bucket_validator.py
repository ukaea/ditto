from DittoWebApi.src.utils import messages
from DittoWebApi.src.utils.bucket_helper import is_valid_bucket
from DittoWebApi.src.utils.bucket_warning import BucketWarning
from DittoWebApi.src.utils.return_status import StatusCodes


# pylint: disable=too-few-public-methods
class BucketValidator:
    def __init__(self, external_data_service, logger):
        self._external_data_service = external_data_service
        self._logger = logger

    def check_bucket(self, bucket_name):
        self._logger.debug(f"About to check for warning to do with bucket name {bucket_name}")
        bucket_warning = None

        if not is_valid_bucket(bucket_name):
            bucket_warning = BucketWarning(messages.bucket_breaks_s3_convention(bucket_name), StatusCodes.Bad_request)

        elif not self._external_data_service.does_bucket_match_standard(bucket_name):
            bucket_warning = BucketWarning(messages.bucket_breaks_config(bucket_name), StatusCodes.Bad_request)

        elif not self._external_data_service.does_bucket_exist(bucket_name):
            bucket_warning = BucketWarning(messages.bucket_not_exists(bucket_name), StatusCodes.Not_found)

        if bucket_warning is not None:
            self._logger.warning(bucket_warning)
            return bucket_warning

        self._logger.debug("No bucket related warnings found")
        return None
