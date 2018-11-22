from DittoWebApi.src.utils.parse_strings import is_str_empty


def format_route_specification(name):
    if is_str_empty(name):
        raise ValueError("Route name must not be empty!")
    return r'/' + name + r'(|/)'
