def return_transfer_summary(new_files_uploaded=0, files_updated=0, files_skipped=0, data_transferred=0, message=""):
    return {"message": message,
            "new files uploaded": new_files_uploaded,
            "files updated": files_updated,
            "files skipped": files_skipped,
            "data transferred (bytes)": data_transferred}


def return_bucket_message(message, bucket_name=""):
    return {"message": message,
            "bucket": bucket_name}


def return_delete_file_helper(message, file_rel_path, bucket_name):
    return {"message": message,
            "file": file_rel_path,
            "bucket": bucket_name}
