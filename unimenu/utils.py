import json


def load_json(config_path):
    """get json data from a file path, return None if not json"""
    path = str(config_path)
    if not path.lower().endswith(".json"):
        return

    with open(config_path) as file:
        data = json.load(file)
    return data


def load_yaml(config_path):
    """get yaml data from a file path, return None if not yaml"""
    path = str(config_path)
    if not path.lower().endswith(".yaml"):
        return

    import yaml

    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data


def load_config(config_path):
    """get data from a JSON or YAML config"""
    return load_json(config_path) or load_yaml(config_path)


def getattr_recursive(obj, attr: str):
    """
    getattr but recursive, supports nested attributes
    attr: provide either 1 attribute, or multiple separated by a dot
    """
    attributes = attr.split(".")
    for attribute in attributes:
        obj = getattr(obj, attribute)
    return obj


def try_command(command, *args, **kwargs):
    """try to run a command, return None if it fails & print the traceback"""
    try:
        # check if string
        if isinstance(command, str):
            return exec(command)
        else:
            return command(*args, **kwargs)
    except Exception:
        import traceback
        traceback.print_exc()