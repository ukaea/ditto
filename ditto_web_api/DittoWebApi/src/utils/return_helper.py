def return_dict(files_transferred=0, files_updated=0, files_skipped=0, data_transferred=0, message=""):
    return {"Message": message,
            "Files transferred": files_transferred,
            "Files updated": files_updated,
            "Files skipped": files_skipped,
            "Data transferred (bytes)": data_transferred}


def return_bucket_message(message, bucket_name=""):
    return {"Message": message,
            "Name of bucket attempted": bucket_name}


def return_delete_file_helper(message, file_name, bucket_name):
    return {"Message": message,
            "File attempted to delete": file_name,
            "Bucket containing file": bucket_name}
