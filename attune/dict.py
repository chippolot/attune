def get_dict_value(d, path, default=None):
    keys = path.split(".")
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d


def set_dict_value(d, path, value):
    keys = path.split(".")
    for key in keys[:-1]:
        if key not in d or not isinstance(d[key], dict):
            d[key] = {}
        d = d[key]
    if value is not None:
        d[keys[-1]] = value
    else:
        d.pop(keys[-1], None)
