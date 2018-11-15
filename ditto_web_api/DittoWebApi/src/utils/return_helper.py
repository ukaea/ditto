def return_transfer_summary(files_transferred=0, files_updated=0, files_skipped=0, data_transferred=0, message=""):
    return {"message": message,
            "new files uploaded": files_transferred,
            "files updated": files_updated,
            "files skipped": files_skipped,
            "data transferred (bytes)": data_transferred}


def return_bucket_message(message, bucket_name=""):
    return {"message": message,
            "bucket": bucket_name}


def return_delete_file_helper(message, file_name, bucket_name):
    return {"message": message,
            "file": file_name,
            "bucket": bucket_name}
