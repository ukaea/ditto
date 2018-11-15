from pathlib import PureWindowsPath


def to_posix(path):
    return PureWindowsPath(path).as_posix()
