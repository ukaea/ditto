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
    # Note should always use canonical paths to ensure correct results
    root_path_as_prefix = dir_path_as_prefix(root_path)
    directory_path_as_prefix = dir_path_as_prefix(directory_path)
    return directory_path_as_prefix.startswith(root_path_as_prefix)
