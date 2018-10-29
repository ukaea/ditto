def str2bool(string):
    s = string.lower()
    if s == "true":
        return True
    if s == "false":
        return False
    raise ValueError("'%s' not recognised as a Boolean. Use 'True' or 'False' (case insensitive)." % string)