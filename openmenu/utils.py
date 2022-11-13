import json


def get_json_data(config_path):
    """get json data from a file path, return None if not json"""
    path = str(config_path)
    if not path.lower().endswith('.json'):
        return

    with open(config_path) as file:
        data = json.load(file)
    return data


def get_yaml_data(config_path):
    """get yaml data from a file path, return None if not yaml"""
    path = str(config_path)
    if not path.lower().endswith('.yaml'):
        return

    import yaml

    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data


def getattr_recursive(obj, attr: str):
    """
    getattr but recursive, supports nested attributes
    attr: provide either 1 attribute, or multiple separated by a dot
    """
    attributes = attr.split('.')
    for attribute in attributes:
        obj = getattr(obj, attribute)
    return obj
