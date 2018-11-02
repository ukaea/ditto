def str2bool(string):
    lower_str = string.lower()
    if lower_str == "true":
        return True
    if lower_str == "false":
        return False
    raise ValueError("'{}' not recognised as a Boolean. Use 'True' or 'False' (case insensitive)." .format(string))
