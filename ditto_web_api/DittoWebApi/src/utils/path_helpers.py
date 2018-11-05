from pathlib import Path


def to_posix(path):
    return Path(path).as_posix()
