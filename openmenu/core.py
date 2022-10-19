import json
import warnings
from pathlib import Path
from collections import namedtuple
import importlib
import pkgutil
import contextlib
from typing import Union


# name: the name of the dcc, and also the name of the menu module
# name of module: a unique python module only available in that dcc
# callback: not sure if we need this
DCC = namedtuple('DCC', ['name', 'module'])


class DCCs:
    """DCCs supported by this module"""
    # dcc -> digital content creation (software)

    BLENDER = DCC('blender', 'bpy')
    MAYA = DCC('maya', 'maya')  # pymel can be slow to import
    UNREAL = DCC('unreal', 'unreal')
    MAX = DCC('max', 'pymxs')
    KRITA = DCC('krita', 'krita')
    SUBSTANCE_DESIGNER = DCC('substance_designer', 'pysbs')
    SUBSTANCE_PAINTER = DCC('substance_painter', 'substance_painter')
    MARMOSET = DCC('marmoset', 'mset')

    ALL = [BLENDER, MAYA, UNREAL, KRITA, SUBSTANCE_PAINTER, MAX, MARMOSET]


def detect_dcc() -> DCC:
    """detect which dcc is currently running"""
    for dcc in DCCs.ALL:
        with contextlib.suppress(ImportError):
            __import__(dcc.module)
            print(f"OPENMENU: detected {dcc.name}")
            return dcc
    warnings.warn("OPENMENU: no supported DCC detected")


def config_setup(path: Union[str, Path], dcc=None):
    """setup menu in dcc from a json or yaml config file"""
    data = get_json_data(path) or get_yaml_data(path)
    return setup(data, dcc)


def setup(data, dcc=None):
    """run setup_menu() on the dcc submodule"""
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
    """remove the create menu"""
    raise NotImplementedError("not yet implemented")


def getattr_recursive(obj, attr):
    """
    getattr but recursive, supports nested attributes
    provide multiple attributes separated by a dot
    """
    attributes = attr.split('.')
    for attribute in attributes:
        obj = getattr(obj, attribute)
    return obj


def module_setup(parent_module_name, parent_menu_name='', menu_name="", function_name='main', dcc=None):
    """
    Create a menu from a folder with modules,
    automatically keep your menu up to date with all tools in that folder

    note: ensure the folder is importable and in your environment path

    Args:
    parent_module: the module that contains all tools. e.g.:
                   cool_tools
                   ├─ __init__.py   (import cool_tools)
                   ├─ tool1.py      (import cool_tools.tool1)
                   └─ tool2.py      (import cool_tools.tool2)
    menu_name: optional kwars to overwrite the name of the menu to create, defaults to module name
    function_name: the function name to run on the module, e.g.: 'run', defaults to 'main'
                   if empty, call the module directly
    dcc: the dcc that contains the menu. if None, will try to detect dcc

    """

    parent_module = importlib.import_module(parent_module_name)

    # create dict for every module in the folder
    # label: the name of the module
    # callback: the function to run

    # todo support recursive folders -> auto create submenus

    items = []
    for module_finder, submodule_name, ispkg in pkgutil.iter_modules(parent_module.__path__):

        # skip private modules
        if submodule_name.startswith('_'):
            continue

        # to prevent issues with late binding
        # https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension
        # first arg might be self, e.g. operator wrapped in blender
        def callback(self=None, _submodule_name=submodule_name, _function_name=function_name, *args, **kwargs):

            # only import the module after clicking in the menu
            # so failed module imports don't break the menu setup
            submodule = module_finder.find_spec(_submodule_name).loader.load_module()

            # run the user-provided function on the module, or call the module directly
            if _function_name:
                function = getattr_recursive(submodule, _function_name)
                function()
            else:
                submodule()

        submodule_dict = {
            'label': submodule_name,
            'command': callback,
        }
        items.append(submodule_dict)

    data = {}
    if parent_menu_name:
        data['parent'] = parent_menu_name
    data['items'] = [{
        'label': menu_name or parent_module.__name__,
        'items': items
    }]

    # use the generated dict to set up the menu
    return setup(data, dcc)


