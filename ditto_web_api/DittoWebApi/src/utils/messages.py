def bucket_existence_warning(bucket_name):
    return "Warning, bucket {} does not exist in the S3 storage".format(bucket_name)


def no_files_found(dir_path):
    return "No files found in directory or directory does not exist ({})".format(dir_path)


def no_new_files(dir_path):
    return "No new files found in directory ({})".format(dir_path)


def transfer_success():
    return "Transfer successful"


def transfer_summary(files_to_tansfer, directory, data_transferred):
    return "Transfer successful, copied {} new files from {} totalling {} bytes".format(files_to_tansfer,
                                                                                        directory,
                                                                                        data_transferred)


def transfer_summary_with_updates(new_files, files_to_update, directory, data_transferred):
    return "Transfer successful, copied {} new files and updated {} files from {} totalling {} bytes".format(
        new_files, files_to_update, directory, data_transferred
    )


def file_deleted(file_name, bucket_name):
    return "File {} successfully deleted from bucket {}".format(file_name, bucket_name)


def bucket_created(bucket_name):
    return "Bucket Created ({})".format(bucket_name)


def file_existence_warning(file_name, bucket_name):
    return "File {} does not exist in bucket {}".format(file_name, bucket_name)


def no_bucket_name():
    return "No bucket name provided"


def bucket_breaks_config(bucket_name):
    return "Bucket breaks local naming standard ({})".format(bucket_name)


def bucket_breaks_s3_convention(bucket_name):
    return "Bucket name breaks S3 naming convention ({})".format(bucket_name)


def directory_exists(directory, skipped_files):
    return "Directory {} already exists on S3, {} files skipped".format(directory, skipped_files)


def bucket_already_exists(bucket_name):
    return "Warning, bucket already exists ({})".format(bucket_name)


def bucket_not_exists(bucket_name):
    return "Warning, bucket does not exist ({})".format(bucket_name)


def no_new_or_updates(directory):
    return "No new or updated files found in directory ({})".format(directory)
