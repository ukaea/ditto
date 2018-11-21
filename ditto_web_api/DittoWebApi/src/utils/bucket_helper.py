import re


def is_valid_bucket(bucket_name):
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False
    if '..' in bucket_name:
        return False
    match = re.compile('^[a-z0-9][a-z0-9\\.\\-]+[a-z0-9]$').match(bucket_name)
    if match is None or match.end() != len(bucket_name):
        return False
    return True
