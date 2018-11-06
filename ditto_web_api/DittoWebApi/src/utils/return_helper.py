def return_dict(files_transferred=0, files_updated=0, files_skipped=0, data_transferred=0, message=None):
    if message:
        return {"Message": message,
                "Files transferred": files_transferred,
                "Files updated": files_updated,
                "Files skipped": files_skipped,
                "Data transferred (bytes)": data_transferred}
    else:
        return {"Files transferred": files_transferred,
                "Files updated": files_updated,
                "Files skipped": files_skipped,
                "Data transferred (bytes)": data_transferred}
