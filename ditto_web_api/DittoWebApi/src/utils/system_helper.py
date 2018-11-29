import time
from datetime import datetime


def current_time():
    return time.time()


def current_time_in_utc():
    time_stamp = current_time()
    return datetime.utcfromtimestamp(time_stamp)
