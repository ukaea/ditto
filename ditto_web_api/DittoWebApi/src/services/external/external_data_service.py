import os
import dateutil.parser

from DittoWebApi.src.models.s3_object_information import S3ObjectInformation
from DittoWebApi.src.utils.file_system.path_helpers import to_posix
from DittoWebApi.src.utils.file_system.path_helpers import dir_path_as_prefix


class ExternalDataService:
    def __init__(self, configuration, logger, s3_adapter):
        self._logger = logger
        self._bucket_standard = configuration.bucket_standard
        self._s3_client = s3_adapter

    # Buckets

    def create_bucket(self, bucket_name):
        output = self._s3_client.make_bucket(bucket_name, location="")
        msg = f'Created bucket "{bucket_name}"' \
            if output is True \
            else f'Could not create bucket "{bucket_name}"'
        self._logger.debug(msg)
        return output

    def does_bucket_exist(self, bucket_name):
        bucket = self._s3_client.get_bucket(bucket_name)
        bucket_exists = bucket is not None
        msg = f'Bucket "{bucket_name}" does ' + ('' if bucket_exists else 'not ') + 'exist'
        self._logger.debug(msg)
        return bucket_exists

    def does_bucket_match_standard(self, bucket_name):
        length_of_bucket_standard = len(self._bucket_standard)
        return bucket_name[:(length_of_bucket_standard + 1)] == (self._bucket_standard + "-")

    # Directories

    def does_dir_exist(self, bucket_name, dir_path):
        bucket = self._s3_client.get_bucket(bucket_name)
        if bucket is None:
            self._logger.warning(
                f'Tried to find directory "{dir_path}" in non-existent bucket "{bucket_name}"'
            )
            return False
        prefix = None if dir_path is None else dir_path_as_prefix(dir_path)
        result_set = bucket.list(prefix=prefix)
        try:
            next(iter(result_set))
            return True
        except StopIteration:
            return False

    # Objects

    def get_objects(self, bucket_name, dir_path):
        self._logger.debug("Going to find objects from directory '{}' in bucket '{}'".format(dir_path, bucket_name))
        bucket = self._s3_client.get_bucket(bucket_name)
        if bucket is None:
            self._logger.warning(
                f'Tried to get objects from non-existent bucket "{bucket_name}"'
            )
            return []
        prefix = dir_path_as_prefix(dir_path)
        results_set = bucket.list(prefix=prefix)
        objects = [ExternalDataService._get_s3_object_information(boto_object)
                   for boto_object in results_set]
        self._logger.debug(
            f'Found {len(objects)} objects in bucket "{bucket_name}"'
        )
        return objects

    def does_object_exist(self, bucket_name, file_name):
        bucket = self._s3_client.get_bucket(bucket_name)
        if bucket is None:
            self._logger.warning(
                f'Tried to find object "{file_name}" in non-existent bucket "{bucket_name}"'
            )
            return False
        key = bucket.get_key(file_name)
        return key is not None

    def upload_file(self, bucket_name, file_information):
        bucket = self._s3_client.get_bucket(bucket_name)
        if bucket is None:
            return False
        object_name = to_posix(file_information.rel_path)
        key = bucket.get_key(object_name)
        key = bucket.new_key(key_name=object_name) if key is None else key
        key.set_contents_from_filename(file_information.abs_path)
        file_length = os.stat(file_information.abs_path).st_size
        self._logger.debug(
            f'File "{object_name}" uploaded, {file_length} bytes transferred'
        )
        return file_length

    def delete_file(self, bucket_name, file_rel_path):
        object_name = to_posix(file_rel_path)
        bucket = self._s3_client.get_bucket(bucket_name)
        if bucket is None:
            self._logger.warning(
                f'Tried to delete object "{object_name}" from non-existent bucket "{bucket_name}"'
            )
            return False
        key = bucket.get_key(object_name)
        if key is None:
            self._logger.warning(
                f'Tried to delete non-existent object "{object_name}" from bucket "{bucket_name}"'
            )
            return False
        key.delete()
        self._logger.debug(f'Deleted object "{object_name}" from bucket "{bucket_name}"')
        return True

    # Private methods

    @staticmethod
    def _get_s3_object_information(boto_object):
        return S3ObjectInformation.create(
            boto_object.name,
            boto_object.bucket.name,
            False,
            boto_object.size,
            boto_object.etag,
            dateutil.parser.parse(boto_object.last_modified)
        )

    def perform_transfer(self, bucket_name, new_files, files_to_update=[], files_to_skip=0):
        data_transferred = 0
        for file in new_files + files_to_update:
            data_transferred += self.upload_file(bucket_name, file)
        return {"message": "Transfer successful",
                "new_files_uploaded": len(new_files),
                "files_updated": len(files_to_update),
                "files_skipped": int(files_to_skip),
                "data_transferred": data_transferred}
