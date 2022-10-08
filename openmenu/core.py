import json
import warnings
from pathlib import Path
from collections import namedtuple
import importlib

# class DCC:
#     name = None
#     module = None
#     callback = None

# name: the name of the dcc, and also the name of the menu module
# name of module: a unique python module only available in that dcc
# callback: not sure if we need this
DCC = namedtuple('DCC', ['name', 'module'])


class DCCs:
    """DCCs supported by this module"""
    # dcc -> digital content creation (software)
    # dcc name = unique dcc module name

    BLENDER = DCC('blender', 'bpy')
    MAYA = DCC('maya', 'maya')  # pymel can be slow to import
    UNREAL = DCC('unreal', 'unreal')
    MAX = DCC('max', 'pymxs')
    KRITA = DCC('krita', 'krita')
    SUBSTANCE_DESIGNER = DCC('substance_designer', 'pysbs')
    SUBSTANCE_PAINTER = DCC('substance_painter', 'substance_painter')
    MARMOSET = DCC('marmoset', 'mset')

    ALL = [BLENDER, MAYA, UNREAL, KRITA, SUBSTANCE_PAINTER, MAX, MARMOSET]


def detect_dcc():
    for dcc in DCCs.ALL:
        try:
            __import__(dcc.module)
            print(f"OPENMENU: detected {dcc.name}")
            return dcc
        except ImportError:
            pass
    print("OPENMENU: no supported DCC detected")


def config_setup(path: (str, Path), dcc=None):
    """setup menu"""
    data = get_json_data(path) or get_yaml_data(path)
    return setup(data, dcc)


def setup(data, dcc=None):
    dcc = dcc or detect_dcc()
    module = importlib.import_module(f'openmenu.{dcc.name}')
    return module.setup_menu(data)


def get_json_data(config_path):
    path = str(config_path)
    if not path.lower().endswith('.json'):
        return

    with open(config_path) as file:
        data = json.load(file)
    return data


def get_yaml_data(config_path):
    path = str(config_path)
    if not path.lower().endswith('.yaml'):
        return

    import yaml

    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")
