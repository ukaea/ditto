from pathlib import PureWindowsPath
from DittoWebApi.src.utils.parse_strings import is_str_empty


def to_posix(path):
    return PureWindowsPath(path).as_posix()


def dir_path_as_prefix(dir_path):
    if is_str_empty(dir_path):
        return None
    prefix = to_posix(dir_path)
    return prefix \
        if prefix[-1] == "/" \
        else prefix + "/"


def is_sub_dir_of_root(directory_path=None, root_path=None):
    return directory_path.startswith(root_path)
